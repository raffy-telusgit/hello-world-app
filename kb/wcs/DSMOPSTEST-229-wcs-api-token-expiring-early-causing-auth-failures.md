---
title: WCS API token expiring early causing auth failures
jira_ref: DSMOPSTEST-229
category: wcs
last_seen: 2026-08-25
---
## Symptom
A WCS integration began returning `401 Unauthorized` errors on API calls approximately 10 minutes into a session, well before the documented 1-hour token lifetime. A batch job running for 45+ minutes was failing partway through due to these premature authentication failures.

## Root cause
The token issued by the WCS auth service had the `exp` claim set correctly for a 1-hour lifetime. However, the batch host's local clock was drifting approximately 50 minutes fast due to an NTP synchronization issue. As a result, the client itself incorrectly believed the token had already expired and began rejecting it early, even though the server would have accepted the token as valid.

## Fix
1. Corrected the NTP configuration on the batch host (`<env>`).
2. Confirmed clock drift was reduced to under 1 second after the fix.
3. Re-ran the batch job end to end (~52 minutes) with no authentication failures observed.

## Notes
- This was a client-side clock issue, not a server-side token issuance problem. The WCS auth service was behaving correctly throughout.
- As a longer-term hardening measure, adding a clock-skew tolerance of a few minutes to the WCS client's token validation logic is recommended. This has been filed as a separate follow-up item.
- Any long-running batch jobs relying on WCS API tokens should ensure NTP is correctly configured and monitored on their host environments to prevent recurrence.
