# backend/main.py
from fastapi.responses import RedirectResponse

from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import socket
import speedtest
import os
import pickle
import sqlite3
from datetime import datetime

app = FastAPI(title="Connectivity Analyzer + ML API + Logging")

# ----------- Paths & ML Model Loading ----------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "rf_model.pkl")
DB_PATH = os.path.join(BASE_DIR, "connectivity_logs.db")

# Load ML model
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("ML model loaded successfully.")
except FileNotFoundError:
    model = None
    print("Warning: ML model not found at", MODEL_PATH)

# ----------- Database Setup ----------- #
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS connectivity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    target TEXT,
    output TEXT,
    timestamp TEXT
)
""")
conn.commit()

# ----------- Request Models ----------- #
class PingRequest(BaseModel):
    host: str

class DNSRequest(BaseModel):
    domain: str

class PredictRequest(BaseModel):
    features: list  # Example: [1.2, 3.4, 5.6]

# ----------- Utility: log results ----------- #
def log_result(type_: str, target: str, output: str):
    cursor.execute(
        "INSERT INTO connectivity_log (type, target, output, timestamp) VALUES (?, ?, ?, ?)",
        (type_, target, output, datetime.now().isoformat())
    )
    conn.commit()

# ----------- Endpoints ----------- #

# ML Prediction
@app.get("/")
async def redirect_root():
    return RedirectResponse(url="/docs")

@app.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        return {"error": "ML model not loaded."}
    try:
        prediction = model.predict([req.features])
        return {"prediction": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}

# Ping
@app.post("/ping")
def ping_host(req: PingRequest):
    try:
        result = subprocess.run(
            ["ping", "-c", "4", req.host],
            capture_output=True, text=True, check=True
        )
        output = result.stdout
        log_result("ping", req.host, output)
        return {"host": req.host, "output": output}
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
        output = result.stdout
        log_result("traceroute", req.host, output)
        return {"host": req.host, "output": output}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "details": e.stderr}

# DNS Lookup
@app.post("/dns")
def dns_lookup(req: DNSRequest):
    try:
        ip = socket.gethostbyname(req.domain)
        log_result("dns", req.domain, ip)
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
        ping_val = st.results.ping
        output = f"Ping: {ping_val}ms, Download: {download:.2f}Mbps, Upload: {upload:.2f}Mbps"
        log_result("speedtest", "self", output)
        return {
            "ping_ms": ping_val,
            "download_mbps": round(download, 2),
            "upload_mbps": round(upload, 2)
        }
    except Exception as e:
        return {"error": str(e)}

# Retrieve history
@app.get("/history")
def get_history(limit: int = 10):
    cursor.execute(
        "SELECT type, target, output, timestamp FROM connectivity_log ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    history = [{"type": t, "target": tgt, "output": out, "timestamp": ts} for t, tgt, out, ts in rows]
    return {"history": history}
