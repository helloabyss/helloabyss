import { loadConfig } from './config';
import { buildServer } from './server';

const config = loadConfig();
const app = buildServer({ config });

app.listen({ port: config.port, host: config.host }).catch((e) => {
  app.log.error(e);
  process.exit(1);
});
