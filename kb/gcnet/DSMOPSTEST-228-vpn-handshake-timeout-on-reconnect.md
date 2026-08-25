---
title: VPN handshake timeout on reconnect
jira_ref: DSMOPSTEST-228
category: gcnet
last_seen: 2026-08-25
---
## Symptom
Users on the VPN client report intermittent handshake timeouts (`ERR_HANDSHAKE_TIMEOUT_408`) when reconnecting after a network switch (e.g. Wi-Fi to wired, or waking from sleep). Client logs show the error repeated 3–4 times before eventually succeeding, or failing outright after 5 retries.

## Root cause
When a client reconnects after a network change, it retries the handshake before the previous session has been fully torn down on the server side. This causes the new handshake attempt to collide with stale session state on the VPN concentrator, resulting in a burst of half-open handshake attempts and repeated timeout errors.

## Fix
Two configuration changes were made and deployed to the VPN concentrator:

1. **Client reconnect retry delay**: Increased the backoff floor so the client waits at least **2 seconds** before its first retry attempt, giving the server sufficient time to clean up the old session.
2. **Server-side stale session cleanup interval**: Reduced from **10 seconds** to **2 seconds**, so stale sessions are cleared more quickly after a disconnect.

Post-deployment testing covered Wi-Fi-to-wired and sleep/wake reconnect scenarios over a 30-minute window with no timeouts observed.

## Notes
- Monitor for recurrence over the following week after deployment.
- If timeouts reappear, consider further tuning the backoff floor or stale session cleanup interval.
- The root cause is a race condition between client retry speed and server session teardown; both levers (client delay and server cleanup speed) should be considered together when adjusting thresholds.
