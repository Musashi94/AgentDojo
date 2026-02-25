import fp from 'fastify-plugin';
import fastifyEnv from '@fastify/env';
import { FastifyInstance } from 'fastify';

const schema = {
  type: 'object',
  required: ['PORT', 'APP_NAME', 'APP_VERSION', 'LOG_LEVEL'],
  properties: {
    NODE_ENV: { type: 'string', default: 'development' },
    PORT: { type: 'number', default: 3000 },
    APP_NAME: { type: 'string', default: 'backend-v0.3' },
    APP_VERSION: { type: 'string', default: '0.3.0' },
    LOG_LEVEL: { type: 'string', default: 'info' }
  }
} as const;

declare module 'fastify' {
  interface FastifyInstance {
    config: {
      NODE_ENV: string;
      PORT: number;
      APP_NAME: string;
      APP_VERSION: string;
      LOG_LEVEL: string;
    };
  }
}

export const configPlugin = fp(async (app: FastifyInstance) => {
  await app.register(fastifyEnv, {
    confKey: 'config',
    schema,
    dotenv: true,
    data: process.env
  });
});
