# Database Connection Timeout

**Symptom:** Requests to the app start timing out or returning 500s, and logs show
connection timeouts to the database rather than application errors.

**Cause:** Most commonly the Serverless VPC Connector (`hello-world-vpc`) is saturated,
or the Cloud Run service scaled up faster than the database's max-connections limit.

**Fix:**
1. Check the VPC connector's throughput metrics in Cloud Monitoring — if it's near its
   configured max instances, request a quota increase or reduce connector min/max bounds.
2. Check the Cloud Run service's `max_instance_count` (currently 3 per environment) against
   the database's max connection pool — each instance holds its own pool, so scaling out
   can exhaust connections faster than expected.
3. As a short-term mitigation, lower `max_instance_count` on the affected Cloud Run
   environment to reduce concurrent connections while the root cause is investigated.
4. Verify egress is set to `ALL_TRAFFIC` on the VPC access config so traffic is actually
   routed through the connector rather than timing out on a misrouted path.
