from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
from typing import List, Optional
import asyncio
import subprocess
import socket
import json
import speedtest
import datetime
import pickle

# ---------------- App ---------------- #
app = FastAPI(title="Connectivity Analyzer API", version="1.0")

# ---------------- Pydantic Models ---------------- #
class PredictRequest(BaseModel):
    features: conlist(float, min_items=3, max_items=3)  # exactly 3 features

class PredictResponse(BaseModel):
    prediction: List[str]

class PingRequest(BaseModel):
    host: str

class PingResponse(BaseModel):
    host: str
    output: str

class DNSRequest(BaseModel):
    domain: str

class DNSResponse(BaseModel):
    domain: str
    ip: str

class TracerouteRequest(BaseModel):
    host: str

class TracerouteResponse(BaseModel):
    host: str
    output: str

class SpeedtestResponse(BaseModel):
    ping_ms: float
    download_mbps: float
    upload_mbps: float

# ---------------- Load ML Model ---------------- #
try:
    with open("rf_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("ML model loaded successfully.")
except Exception as e:
    model = None
    print("Failed to load ML model:", e)

# ---------------- Utility Functions ---------------- #
async def run_cmd(cmd: List[str]) -> str:
    """Run shell command asynchronously and return output"""
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if stderr:
        return stderr.decode()
    return stdout.decode()

# ---------------- Endpoints ---------------- #
@app.post("/predict", response_model=PredictResponse)
async def predict(data: PredictRequest):
    if not model:
        raise HTTPException(status_code=500, detail="ML model not loaded")
    prediction = model.predict([data.features])
    return {"prediction": prediction.tolist()}

@app.post("/ping", response_model=PingResponse)
async def ping(data: PingRequest):
    try:
        output = await run_cmd(["ping", "-c", "4", data.host])
    except Exception as e:
        output = str(e)
    return {"host": data.host, "output": output}

@app.post("/dns", response_model=DNSResponse)
async def dns(data: DNSRequest):
    try:
        ip = socket.gethostbyname(data.domain)
    except Exception as e:
        ip = f"Error: {e}"
    return {"domain": data.domain, "ip": ip}

@app.post("/traceroute", response_model=TracerouteResponse)
async def traceroute(data: TracerouteRequest):
    try:
        output = await run_cmd(["traceroute", data.host])
    except Exception as e:
        output = str(e)
    return {"host": data.host, "output": output}

@app.get("/speedtest", response_model=SpeedtestResponse)
async def speedtest_endpoint():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1e6  # Mbps
        upload = st.upload() / 1e6      # Mbps
        ping_ms = st.results.ping
    except Exception as e:
        download = upload = ping_ms = 0
    return {"ping_ms": ping_ms, "download_mbps": download, "upload_mbps": upload}

@app.get("/history")
async def history(limit: Optional[int] = 5):
    # Implement your DB read logic here (currently dummy)
    return {"history": []}
