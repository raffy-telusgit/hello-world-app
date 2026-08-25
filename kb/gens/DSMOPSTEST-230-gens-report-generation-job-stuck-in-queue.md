---
title: GENS report generation job stuck in queue
jira_ref: DSMOPSTEST-230
category: gens
last_seen: 2026-08-25
---
## Symptom
A nightly GENS report generation job entered the queue at its scheduled time but was never picked up by a worker. The job remained in a "queued" state for over 3 hours, resulting in the report not being delivered.

## Root cause
All workers in the GENS worker pool (4 workers) were alive and idle — the issue was not a worker crash. The root cause was a routing key mismatch introduced by a configuration change the previous week. The job was published with the routing key `report.nightly.gen` (missing the trailing `s`), while workers were subscribed to `report.nightly.gens`. Because no worker was listening on the incorrect key, the job sat in the queue indefinitely with no consumer to pick it up.

## Fix
1. Corrected the routing key in the scheduler configuration from `report.nightly.gen` back to `report.nightly.gens` to match the workers' subscribed queues.
2. Manually re-queued the affected job, which was picked up and completed successfully within 4 minutes, delivering the report as expected.

## Notes
A monitoring alert was added to fire if any queued job remains in the "queued" state for longer than 15 minutes without being picked up. This ensures that routing mismatches or similar queue delivery failures are detected promptly rather than going unnoticed for hours.
