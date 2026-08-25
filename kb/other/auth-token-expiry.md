# Auth Token Expiry Errors

**Symptom:** Users intermittently get 401 Unauthorized errors, often clustered a fixed
amount of time after logging in, rather than being tied to a specific action.

**Cause:** The client is not refreshing its auth token before it expires, or the service's
token validation is using a clock-skewed or overly short expiry window.

**Fix:**
1. Confirm the token's `exp` claim and compare it against when the 401s start appearing —
   if they line up, this is a refresh-timing issue, not a validation bug.
2. Check that the client refreshes the token proactively (e.g. at 80% of its lifetime)
   rather than waiting for a 401 and retrying reactively.
3. If server-side validation is the culprit, check for clock skew between the auth
   issuer and the validating service — small skew plus a short expiry window can cause
   tokens to be rejected before their nominal expiry.
4. As a mitigation while investigating, temporarily extend the token lifetime slightly
   longer than the client's refresh interval to add headroom.
