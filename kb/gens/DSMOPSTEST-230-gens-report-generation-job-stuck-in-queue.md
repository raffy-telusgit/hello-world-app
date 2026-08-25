---
title: GENS report generation job stuck in queue
jira_ref: DSMOPSTEST-230
category: gens
last_seen: 2026-08-25
---
## Symptom
A nightly GENS report generation job entered the queue at its scheduled time but was never picked up by a worker. The job remained in a "queued" state for over 3 hours, resulting in the report not being delivered.

## Root cause
A typo was introduced in a recent configuration change to the scheduler. The job was published with the routing key `report.nightly.gen` instead of the correct key `report.nightly.gens`. Because none of the workers were subscribed to the incorrect routing key, all 4 workers remained alive and idle but never received the job. The mismatch between the published routing key and the workers' subscribed queues caused the job to sit indefinitely in the queue broker without being consumed.

## Fix
1. Corrected the routing key in the scheduler configuration from `report.nightly.gen` back to `report.nightly.gens`.
2. Manually re-queued the affected job, which was picked up by a worker and completed successfully within 4 minutes, delivering the report as expected.

## Notes
- A monitoring alert was added to fire if any queued job remains in the "queued" state for longer than 15 minutes without being picked up by a worker. This will ensure similar routing mismatches or queue broker issues are detected promptly rather than going unnoticed for hours.
- When making configuration changes that affect routing keys, verify that the keys in the scheduler config exactly match the keys that workers are subscribed to before deploying.
