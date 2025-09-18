# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import socket
import speedtest

app = FastAPI(title="Connectivity Analyzer API")

# ----------- Request Models ----------- #
class PingRequest(BaseModel):
    host: str

class DNSRequest(BaseModel):
    domain: str


# ----------- Endpoints ----------- #

# Ping a host
@app.post("/ping")
def ping_host(req: PingRequest):
    try:
        result = subprocess.run(
            ["ping", "-c", "4", req.host],  # "-c 4" = send 4 packets (Linux/Mac)
            capture_output=True, text=True, check=True
        )
        return {"host": req.host, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "details": e.stderr}


# Traceroute
@app.post("/traceroute")
def traceroute(req: PingRequest):
    try:
        result = subprocess.run(
            ["traceroute", req.host],
            capture_output=True, text=True, check=True
        )
        return {"host": req.host, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "details": e.stderr}


# DNS Lookup
@app.post("/dns")
def dns_lookup(req: DNSRequest):
    try:
        ip = socket.gethostbyname(req.domain)
        return {"domain": req.domain, "ip": ip}
    except socket.gaierror:
        return {"error": f"Unable to resolve {req.domain}"}


# Speedtest
@app.get("/speedtest")
def run_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        return {
            "ping_ms": ping,
            "download_mbps": round(download, 2),
            "upload_mbps": round(upload, 2)
        }
    except Exception as e:
        return {"error": str(e)}
