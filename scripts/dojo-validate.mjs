import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import YAML from 'yaml';
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';

const root = process.cwd();
const configPath = path.join(root, 'agentdojo', 'dojo.config.yaml');
const schemaPath = path.join(root, 'agentdojo', 'dojo.schema.json');

function fail(msg, details) {
  console.error(`dojo:validate failed: ${msg}`);
  if (details) console.error(details);
  process.exit(1);
}

if (!fs.existsSync(configPath)) fail(`missing config at ${configPath}`);
if (!fs.existsSync(schemaPath)) fail(`missing schema at ${schemaPath}`);

const configRaw = fs.readFileSync(configPath, 'utf8');
const schemaRaw = fs.readFileSync(schemaPath, 'utf8');

let config;
let schema;

try {
  config = YAML.parse(configRaw);
} catch (err) {
  fail('invalid YAML in dojo.config.yaml', err instanceof Error ? err.message : String(err));
}

try {
  schema = JSON.parse(schemaRaw);
} catch (err) {
  fail('invalid JSON in dojo.schema.json', err instanceof Error ? err.message : String(err));
}

const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);
const validate = ajv.compile(schema);
const ok = validate(config);

if (!ok) {
  const errs = (validate.errors ?? []).map(e => `${e.instancePath || '/'} ${e.message}`).join('\n');
  fail('schema validation errors', errs);
}

if (config?.learning?.inherit_profile) {
  const p = config.profile;
  const exists = !!config.learning_profiles?.[p];
  if (!exists) fail(`profile '${p}' not found in learning_profiles`);
}

console.log('dojo:validate OK');
