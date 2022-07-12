import * as Sentry from "@sentry/browser";
import { BrowserTracing } from "@sentry/tracing";
import 'htmx.org'

Sentry.init({
  dsn: "https://d413ae5654b842748652994a328ff719@o1314735.ingest.sentry.io/6565784",
  integrations: [new BrowserTracing()],

  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 1.0,
});

window.htmx = require('htmx.org');