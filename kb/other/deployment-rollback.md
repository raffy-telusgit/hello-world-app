# Deployment Rollback Steps

**Symptom:** A Cloud Deploy release to `staging` or `prod` is causing errors (5xx spikes,
failed health checks) immediately after promotion.

**Cause:** A bad image was promoted, or a config/env var change broke startup.

**Fix:**
1. Open the Cloud Deploy pipeline `hello-world-pipeline` in the GCP Console.
2. Find the last known-good rollout for the affected target (`staging` or `prod`).
3. Use "Rollback" on that target to redeploy the previous successful release — this does
   not require a new build, it just re-promotes the prior image.
4. Confirm `GET /healthz` returns `200 {"status": "ok"}` on the affected Cloud Run service
   before considering the rollback complete.
5. File a follow-up issue referencing the bad release so the root cause gets fixed before
   the next promotion attempt.
