import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { buildApp } from '../src/app.js';

describe('backend v0.3', () => {
  const oldEnv = { ...process.env };

  beforeAll(() => {
    process.env.PORT = '3000';
    process.env.APP_NAME = 'backend-v0.3';
    process.env.APP_VERSION = '0.3.0';
    process.env.NODE_ENV = 'test';
    process.env.LOG_LEVEL = 'silent';
  });

  afterAll(() => {
    process.env = oldEnv;
  });

  it('GET /health', async () => {
    const app = await buildApp();
    const res = await app.inject({ method: 'GET', url: '/health' });
    expect(res.statusCode).toBe(200);
    expect(res.json()).toEqual({ status: 'ok' });
    await app.close();
  });

  it('GET /version', async () => {
    const app = await buildApp();
    const res = await app.inject({ method: 'GET', url: '/version' });
    expect(res.statusCode).toBe(200);
    expect(res.json()).toEqual({
      name: 'backend-v0.3',
      version: '0.3.0',
      env: 'test'
    });
    await app.close();
  });

  it('GET /v03/ping', async () => {
    const app = await buildApp();
    const res = await app.inject({ method: 'GET', url: '/v03/ping' });
    expect(res.statusCode).toBe(200);
    expect(res.json()).toEqual({ message: 'pong', v: '0.3' });
    await app.close();
  });
});
