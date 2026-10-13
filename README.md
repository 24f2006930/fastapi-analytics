# FastAPI Event Analytics

Stateless FastAPI endpoint that authenticates requests with `X-API-Key`, aggregates event batches dynamically, and allows cross-origin requests for browser-based verification.

## Repository description

Stateless FastAPI analytics API with API-key authentication, event revenue aggregation, top-user calculation, and permissive CORS for grader verification.

## Live endpoint

After deployment, use `https://YOUR-SERVICE.onrender.com/analytics`.

## Endpoint

`POST /analytics`

Required header:

```text
X-API-Key: <assigned API key>
```

Example request:

```json
{
  "events": [
    {"user": "alice", "amount": 42.5, "ts": 1700000000},
    {"user": "bob", "amount": -5, "ts": 1700000001}
  ]
}
```

The response includes the configured student email, total event count, distinct user count, sum of positive amounts only, and the user with the largest positive-amount total.

Missing or incorrect API keys return HTTP 401. Results are computed from each request; no event data is stored between requests.

## CORS

Allows cross-origin `POST` and preflight requests, including the `X-API-Key` and `Content-Type` headers.

## Deploy on Render

Create a Render Blueprint from this repository using `render.yaml`. Verify `STUDENT_EMAIL` matches the email shown by your assignment. The assigned API key is configured as `ANALYTICS_API_KEY`.

## Test

```bash
curl -i -X POST "https://YOUR-SERVICE.onrender.com/analytics" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_ASSIGNED_KEY" \
  -d '{"events":[{"user":"alice","amount":42.5,"ts":1700000000},{"user":"bob","amount":-5,"ts":1700000001}]}'
```
