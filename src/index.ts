import express from "express";

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", (_req, res) => {
  res.json({
    message: "Hello World",
    version: "1.0.0",
    environment: process.env.ENVIRONMENT || "unknown",
    timestamp: new Date().toISOString(),
  });
});
//health check endpoint
app.get("/healthz", (_req, res) => {
  res.status(200).json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
