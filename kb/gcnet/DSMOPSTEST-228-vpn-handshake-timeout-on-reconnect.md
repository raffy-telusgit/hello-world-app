---
title: VPN handshake timeout on reconnect
jira_ref: DSMOPSTEST-228
category: gcnet
last_seen: 2026-08-25
---
## Symptom
Users on the VPN client report intermittent handshake timeouts (`ERR_HANDSHAKE_TIMEOUT_408`) when reconnecting after a network switch (e.g. Wi-Fi to wired, or waking from sleep). Client logs show the error repeated 3–4 times before eventually succeeding, or failing outright after 5 retries.

## Root cause
When a client reconnects after a network change, it retries the handshake before the previous session is fully torn down on the server side. This causes the new handshake attempt to collide with stale session state on the VPN concentrator, resulting in a burst of half-open handshake attempts and repeated timeout errors.

## Fix
Two configuration changes were made and deployed to the VPN concentrator:

1. **Increased the client-side reconnect retry delay backoff floor** to a minimum of 2 seconds before the first retry, giving the server sufficient time to clean up the old session before a new handshake is attempted.
2. **Reduced the server-side stale session cleanup interval** from 10 seconds to 2 seconds, so that orphaned sessions are cleared more quickly and do not block incoming reconnect attempts.

Changes were tested across Wi-Fi-to-wired and sleep/wake reconnect scenarios for 30 minutes with no timeouts observed.

## Notes
- Monitoring for recurrence is recommended for at least one week following deployment.
- If timeouts reappear, consider further tuning the backoff floor or stale session cleanup interval.
- This issue is most likely to surface in environments where clients frequently switch network interfaces or resume from sleep.
