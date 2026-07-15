// Demo admin endpoints with intentional security issues, added to exercise the
// PR security review. NOT meant to be merged.
import { exec } from "child_process";
import express from "express";

// Hardcoded production credentials committed to source control.
const DB_PASSWORD = "Pr0d-Db-P@ssw0rd-2024";
const ADMIN_API_KEY = "ak-live-9f8e7d6c5b4a3210deadbeefcafef00d";

export const adminRouter = express.Router();

// Command injection: the user-controlled `host` is interpolated straight into a
// shell command with no validation or escaping.
adminRouter.get("/diagnostics/ping", (req, res) => {
  const host = String(req.query.host);
  exec(`ping -c 1 ${host}`, (error, stdout) => {
    if (error) {
      res.status(500).json({ error: error.message });
      return;
    }
    res.json({ output: stdout });
  });
});

// No authentication, and it reflects hardcoded secrets back to any caller.
adminRouter.get("/config", (_req, res) => {
  res.json({
    dbPassword: DB_PASSWORD,
    adminApiKey: ADMIN_API_KEY,
  });
});
