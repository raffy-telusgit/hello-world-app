---
title: WCS API token expiring early causing auth failures
jira_ref: DSMOPSTEST-229
category: wcs
last_seen: 2026-08-25
---
## Symptom
WCS API integration throws `401 Unauthorized` errors approximately 10 minutes into a session, well before the documented 1-hour token lifetime. Long-running batch jobs (45+ minutes) fail partway through due to premature authentication failures.

## Root cause
The token issued by the WCS auth service had the `exp` claim set correctly for a 1-hour lifetime. However, the batch host running the WCS client had a significant local clock drift — approximately 50 minutes fast — caused by an NTP sync issue. As a result, the client itself evaluated the token as expired and began rejecting it early, even though the server would have accepted it for the remainder of the valid window.

## Fix
1. Corrected the NTP configuration on the affected batch host.
2. Confirmed clock drift is now under 1 second.
3. Re-ran the batch job end to end (~52 minutes) with no authentication failures.

## Notes
- This issue is entirely client-side; the WCS auth service was issuing tokens correctly.
- As a longer-term hardening measure, adding a clock-skew tolerance of a few minutes to the WCS client's token validation logic is recommended. This has been filed as a separate follow-up item.
- Any host running long-lived batch jobs against WCS should have NTP synchronization verified as part of environment health checks.
