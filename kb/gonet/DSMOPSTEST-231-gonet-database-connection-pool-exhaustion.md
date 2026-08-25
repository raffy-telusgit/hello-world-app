---
title: GONET database connection pool exhaustion
jira_ref: DSMOPSTEST-231
category: gonet
last_seen: 2026-08-25
---
## Symptom
A service started returning HTTP 500 errors under moderate load. Application logs showed `connection pool exhausted, timed out waiting for connection` errors, correlated with a spike in concurrent requests during a batch import operation.

## Root cause
The batch import process was opening a new database connection per record instead of reusing connections from the shared pool. This caused the batch job to exhaust the connection pool on its own during high-volume imports. The pool maximum was configured at 20 connections, and all 20 were consumed approximately 90 seconds before the first 500 errors appeared. The pool size was not undersized for normal traffic; the issue was specific to the batch import's connection handling behavior.

## Fix
1. Patched the batch import process to use the shared connection pool instead of opening ad-hoc per-record connections.
2. Added an explicit connection-per-batch cap to prevent any single batch job from monopolizing the pool.
3. Increased the connection pool maximum from 20 to 30 as an additional safety margin.

After applying the fix, the same import volume that triggered the incident was re-run and pool usage remained below 8/20 throughout.

## Notes
The pool size was not the primary issue; the fix to the batch import's connection reuse behavior is the critical change. The pool size increase is a precautionary measure. Monitor pool utilization if similar batch workloads are introduced in the future to ensure the cap and pool size remain appropriate.
