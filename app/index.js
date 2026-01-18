const express = require("express");
const client = require("prom-client");

const app = express();
const register = new client.Registry();

// Collect default system metrics
client.collectDefaultMetrics({ register });

// Custom counter
const httpRequestsTotal = new client.Counter({
  name: "http_requests_total",
  help: "Total number of HTTP requests"
});
register.registerMetric(httpRequestsTotal);

// Health check
app.get("/health", (req, res) => {
  res.status(200).send("OK");
});

// Prometheus metrics endpoint
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

// Sample app endpoint
app.get("/", (req, res) => {
  httpRequestsTotal.inc();
  res.send("Hello from Node.js application");
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Node app listening on port ${PORT}`);
});
