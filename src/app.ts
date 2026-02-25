import Fastify from 'fastify';
import { configPlugin } from './config.js';

export async function buildApp() {
  const app = Fastify({
    logger: {
      level: process.env.LOG_LEVEL ?? 'info'
    }
  });

  await app.register(configPlugin);

  app.addHook('onRequest', async (request) => {
    request.log.info({ method: request.method, url: request.url }, 'incoming request');
  });

  app.get('/health', async () => ({ status: 'ok' }));

  app.get('/version', async () => ({
    name: app.config.APP_NAME,
    version: app.config.APP_VERSION,
    env: app.config.NODE_ENV
  }));

  app.get('/v03/ping', async () => ({
    message: 'pong',
    v: '0.3'
  }));

  app.setErrorHandler((error, request, reply) => {
    request.log.error({ err: error }, 'request failed');
    reply.status(error.statusCode ?? 500).send({
      error: 'Internal Server Error',
      message: error.message
    });
  });

  return app;
}
