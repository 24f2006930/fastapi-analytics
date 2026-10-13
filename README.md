# FastAPI Event Analytics

A stateless FastAPI service that authenticates requests using an API key, dynamically aggregates event batches, and supports cross-origin requests for browser-based verification. Deployed on Render.

**Live endpoint:** https://fastapi-analytics-e4ao.onrender.com/analytics

## Endpoint

### `POST /analytics`

Accepts a batch of events and returns aggregate statistics.

**Required header:**

```text
X-API-Key: <assigned API key>
```

**Example request:**

```json
{
  "events": [
    {"user": "alice", "amount": 42.5, "ts": 1700000000},
    {"user": "bob", "amount": -5, "ts": 1700000001},
    {"user": "alice", "amount": 10, "ts": 1700000002}
  ]
}
```

**Example response:**

```json
{
  "email": "24f2006930@ds.study.iitm.ac.in",
  "total_events": 3,
  "unique_users": 2,
  "revenue": 52.5,
  "top_user": "alice"
}
```

The results are computed dynamically from each request.

## Aggregation Rules

- **`total_events`** — total number of events in the submitted batch.
- **`unique_users`** — number of distinct user values.
- **`revenue`** — sum of positive event amounts only; zero and negative amounts are excluded.
- **`top_user`** — user with the highest total of positive event amounts.
- **`email`** — configured student email address.

## Authentication

Requests must include the assigned API key in the `X-API-Key` header.

- Missing API key: HTTP `401 Unauthorized`.
- Incorrect API key: HTTP `401 Unauthorized`.
- Correct API key: request is processed and aggregate results are returned.

The endpoint does not store event batches between requests.

## CORS

Cross-origin requests are enabled with a wildcard origin policy (`Access-Control-Allow-Origin: *`) to support browser-based verification. The API permits `POST` requests and the `Content-Type` and `X-API-Key` headers.

## Deployment

The service is deployed on Render using a Blueprint configuration in `render.yaml`.

Configuration uses:

- `STUDENT_EMAIL` — student email address.
- `ANALYTICS_API_KEY` — assigned API key.

## Testing

### 1. Test missing-key rejection

```bash
curl -i -X POST "https://fastapi-analytics-e4ao.onrender.com/analytics" \
  -H "Content-Type: application/json" \
  -d '{"events":[]}'
```

Expected: HTTP `401 Unauthorized`.

### 2. Test valid authentication and aggregation

Set `YOUR_ASSIGNED_KEY` to the assigned API key before running:

```bash
curl -i -X POST "https://fastapi-analytics-e4ao.onrender.com/analytics" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_ASSIGNED_KEY" \
  -d '{"events":[{"user":"alice","amount":42.5,"ts":1700000000},{"user":"bob","amount":-5,"ts":1700000001},{"user":"alice","amount":10,"ts":1700000002}]}'
```

Expected: HTTP `200 OK`, with `total_events` equal to `3`, `unique_users` equal to `2`, `revenue` equal to `52.5`, and `top_user` equal to `"alice"`.
