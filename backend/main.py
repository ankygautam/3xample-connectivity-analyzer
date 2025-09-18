# backend/main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI(
    title="3xample Connectivity Analyzer",
    description="Async API to test network connectivity: ping, DNS, traceroute, and speedtest",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =======================
# Pydantic Models
# =======================

class PingResult(BaseModel):
    host: str
    result: str

class DNSResult(BaseModel):
    host: str
    ip_addresses: List[str]

class TracerouteResult(BaseModel):
    host: str
    hops: List[str]

class SpeedTestResult(BaseModel):
    download_mbps: float
    upload_mbps: float
    ping_ms: float

# =======================
# Async Endpoint Functions (Placeholders)
# =======================

async def run_ping(host: str) -> str:
    # Replace with your actual ping logic
    await asyncio.sleep(0.1)
    return f"Ping to {host} successful"

async def run_dns(host: str) -> List[str]:
    await asyncio.sleep(0.1)
    return ["192.168.1.1"]

async def run_traceroute(host: str) -> List[str]:
    await asyncio.sleep(0.1)
    return ["192.168.1.1", "10.0.0.1", host]

async def run_speedtest() -> dict:
    await asyncio.sleep(0.1)
    return {"download_mbps": 100.5, "upload_mbps": 50.2, "ping_ms": 15.3}

# =======================
# API Endpoints
# =======================

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Redirect to /docs for API documentation"}

@app.get("/ping", response_model=PingResult, summary="Ping a host", description="Returns ping result for a given host")
async def ping(host: str = Query(..., description="Hostname or IP to ping")):
    result = await run_ping(host)
    return PingResult(host=host, result=result)

@app.get("/dns", response_model=DNSResult, summary="Resolve DNS for a host", description="Returns IP addresses for the given host")
async def dns(host: str = Query(..., description="Hostname to resolve")):
    ips = await run_dns(host)
    return DNSResult(host=host, ip_addresses=ips)

@app.get("/traceroute", response_model=TracerouteResult, summary="Traceroute to a host", description="Returns list of hops to reach the host")
async def traceroute(host: str = Query(..., description="Hostname or IP to trace")):
    hops = await run_traceroute(host)
    return TracerouteResult(host=host, hops=hops)

@app.get("/speedtest", response_model=SpeedTestResult, summary="Run internet speed test", description="Returns download, upload speed and ping")
async def speedtest():
    result = await run_speedtest()
    return SpeedTestResult(**result)

# =======================
# To run locally:
# uvicorn backend.main:app --reload
# =======================
