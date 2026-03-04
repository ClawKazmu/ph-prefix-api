"""PH Mobile Prefix API - Lookup Philippine mobile number networks."""

from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict
import time
from collections import defaultdict

app = FastAPI(
    title="PH Mobile Prefix API",
    description="Lookup Globe/Smart/DITO network from Philippine mobile number prefixes",
    version="1.0.0"
)

# CORS - allow all origins for public API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    duration = (datetime.utcnow() - start_time).total_seconds()
    # Get client IP (may be behind proxy)
    client_ip = request.client.host if request.client else "unknown"
    log_line = f"{start_time.isoformat()} - {client_ip} - {request.method} {request.url.path} - {response.status_code} - {duration:.3f}s"
    print(log_line)
    return response

# Load prefix data
def load_prefixes() -> Dict[str, str]:
    import json
    with open("data/prefixes.json", "r") as f:
        return json.load(f)

PREFIX_DATA = load_prefixes()
LAST_UPDATED = "2025-03-05"  # Update when data changes

# Simple in-memory rate limiter: {ip: [timestamp1, timestamp2, ...]}
rate_limit_store = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 100

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    window_start = now - 60
    # Clean old entries
    rate_limit_store[ip] = [t for t in rate_limit_store[ip] if t > window_start]
    # Check count
    if len(rate_limit_store[ip]) >= MAX_REQUESTS_PER_MINUTE:
        return True
    rate_limit_store[ip].append(now)
    return False

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/v1/lookup")
async def lookup(request: Request, number: str = Query(..., description="11-digit mobile number starting with 09")):
    """
    Lookup mobile network by prefix.

    - **number**: 11-digit Philippine mobile number (e.g., 09171234567)

    Returns network, note about MNP, and last updated date.
    """
    # Get client IP (trust X-Forwarded-For if behind proxy like Railway)
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0].strip()
    if is_rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "retry_after": 60}
        )

    # Validate input
    if not number.isdigit():
        raise HTTPException(status_code=400, detail="Number must be digits only")
    if len(number) != 11:
        raise HTTPException(status_code=400, detail="Number must be exactly 11 digits")
    if not (number.startswith("09") or number.startswith("08")):
        raise HTTPException(status_code=400, detail="Number must start with 09 (Globe/Smart) or 08 (DITO)")

    prefix = number[:4]
    network = PREFIX_DATA.get(prefix)

    if not network:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Prefix not found",
                "prefix": prefix,
                "suggestion": "This prefix may be new or unregistered. Contact support to update the database."
            }
        )

    return {
        "number": number,
        "prefix": prefix,
        "network": network,
        "note": "May be affected by Mobile Number Portability (MNP)",
        "last_updated": LAST_UPDATED
    }

@app.get("/api/v1/prefix/{prefix}")
async def lookup_prefix(request: Request, prefix: str):
    """Lookup network by 4-digit prefix only (e.g., 0917)."""
    # Rate limiting
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0].strip()
    if is_rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "retry_after": 60}
        )

    if not prefix.isdigit() or len(prefix) != 4:
        raise HTTPException(status_code=400, detail="Prefix must be 4 digits")
    if not (prefix.startswith("09") or prefix.startswith("08")):
        raise HTTPException(status_code=400, detail="Prefix must start with 09 (Globe/Smart) or 08 (DITO)")

    network = PREFIX_DATA.get(prefix)
    if not network:
        return JSONResponse(
            status_code=404,
            content={"error": "Prefix not found"}
        )
    return {"prefix": prefix, "network": network}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
