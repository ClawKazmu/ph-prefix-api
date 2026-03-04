# PH Mobile Prefix API

A simple, fast API to identify Philippine mobile networks (Globe, Smart, DITO) from phone number prefixes.

## Features

- Lookup by full 11-digit number or 4-digit prefix
- Up-to-date prefix list (2025)
- Rate limiting (100 req/min)
- CORS enabled
- Health check endpoint
- Deploy-ready (Railway, Render)

## Quick Start

### Live Demo (Hosted)

The API is live on Railway:

- **Base URL:** `https://ph-prefix-api.up.railway.app`
- **Health:** `https://ph-prefix-api.up.railway.app/health`
- **Lookup:** `https://ph-prefix-api.up.railway.app/api/v1/lookup?number=09171234567`
- **Docs:** `https://ph-prefix-api.up.railway.app/docs` (Swagger UI)

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python -m app.main
# or
uvicorn app.main:app --reload
```

Server starts at `http://localhost:8000`

### API Docs

Interactive docs: `http://localhost:8000/docs` (Swagger UI)

## API Endpoints

### GET /health

Health check.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-03-05T05:30:00"
}
```

### GET /api/v1/lookup?number=09171234567

Lookup network by full mobile number.

**Parameters:**
- `number` (query, required): 11-digit number starting with **09** (Globe/Smart) or **08** (DITO)

**Success Response (200):**
```json
{
  "number": "09171234567",
  "prefix": "0917",
  "network": "Globe/TM",
  "note": "May be affected by Mobile Number Portability (MNP)",
  "last_updated": "2025-03-05"
}
```

**Error Responses:**
- 400: Invalid input (not 11 digits, not starting with 09 or 08)
- 404: Prefix not in database
- 429: Rate limit exceeded

### GET /api/v1/prefix/{prefix}

Lookup network by 4-digit prefix only.

**Parameters:**
- `prefix` (path, required): 4-digit prefix starting with **09** (Globe/Smart) or **08** (DITO)

Example: `/api/v1/prefix/0917` or `/api/v1/prefix/0895`

**Response (200):**
```json
{
  "prefix": "0917",
  "network": "Globe/TM"
}
```

### GET /stats

Internal usage statistics (in-memory, resets on restart). Returns:

- `total_requests`: total count
- `uptime_seconds`: how long the server has been running
- `requests_by_endpoint`: dict of endpoint → count
- `top_prefixes`: list of `[prefix, count]` most queried prefixes
- `unique_ips_estimate`: approximate unique IPs seen
- `status_codes`: dict of HTTP status → count

**Example:**
```json
{
  "total_requests": 1234,
  "uptime_seconds": 3600,
  "requests_by_endpoint": {"/api/v1/lookup": 1000, "/api/v1/prefix/0917": 200, ...},
  "top_prefixes": [["0917", 500], ["0991", 300], ...],
  "unique_ips_estimate": 45,
  "status_codes": {200: 1200, 404: 30, 429: 4}
}
```

## Pricing Tiers

| Tier | Requests/month | Price | Features |
|------|----------------|-------|----------|
| Free | 100 | ₱0 | Basic lookup, no SLA |
| Starter | 10,000 | ₱300/month | Standard SLA, email support |
| Business | 100,000 | ₱1,000/month | Priority SLA, 99.9% uptime |
| Enterprise | Unlimited | Custom | On-premise option, dedicated support |

## Data Source

Prefix data compiled from official NTC releases, telco announcements, and reputable tech sources. Updated quarterly.

**Last Updated:** 2025-03-05

## Limitations

- This API uses **prefix-based lookup only**. It does **not** verify actual network via Mobile Number Portability (MNP).
- For MNP-verified lookup, use CheckMobi's service ($0.002/req).

## Deployment

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and link project
railway login
railway init
railway add

# Deploy
railway up
```

### Render

1. Create new Web Service
2. Connect GitHub repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment: Python 3.11

## License

MIT
