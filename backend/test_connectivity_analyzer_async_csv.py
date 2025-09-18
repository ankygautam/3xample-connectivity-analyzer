import asyncio
import httpx
import json
import csv
import os
from datetime import datetime

# Use environment variable if set, otherwise fallback
BASE_URL = os.environ.get("CONNECTIVITY_API_URL", "http://127.0.0.1:8000")
CSV_FILE = "connectivity_test_results.csv"
MAX_OUTPUT_LEN = 200  # truncate long outputs

# ----------- CSV Logging ----------- #
def save_to_csv(endpoint, target, result):
    timestamp = datetime.now().isoformat()
    output_str = json.dumps(result)
    if len(output_str) > MAX_OUTPUT_LEN:
        output_str = output_str[:MAX_OUTPUT_LEN] + "..."
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, endpoint, target, output_str])

# ----------- Async Test Functions ----------- #
async def test_ping(client):
    target = "google.com"
    data = {"host": target}
    try:
        r = await client.post(f"{BASE_URL}/ping", json=data, timeout=30.0)
        result = r.json()
        if not result:
            result = {"error": "Ping endpoint returned empty response"}
    except Exception as e:
        result = {"error": str(e)}
    print("---- PING ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/ping", target, result)

async def test_traceroute(client):
    target = "google.com"
    data = {"host": target}
    result = {}
    try:
        r = await client.post(f"{BASE_URL}/traceroute", json=data, timeout=60.0)
        result = r.json()
        if not result:
            result = {"error": "Traceroute endpoint returned empty response"}
    except Exception as e:
        result = {"error": str(e)}
    print("---- TRACEROUTE ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/traceroute", target, result)

async def test_dns(client):
    target = "google.com"
    data = {"domain": target}
    try:
        r = await client.post(f"{BASE_URL}/dns", json=data, timeout=30.0)
        result = r.json()
        if not result:
            result = {"error": "DNS endpoint returned empty response"}
    except Exception as e:
        result = {"error": str(e)}
    print("---- DNS ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/dns", target, result)

async def test_speedtest(client):
    target = "self"
    try:
        r = await client.get(f"{BASE_URL}/speedtest", timeout=60.0)
        result = r.json()
        if not result:
            result = {"error": "Speedtest endpoint returned empty response"}
    except Exception as e:
        result = {"error": str(e)}
    print("---- SPEEDTEST ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/speedtest", target, result)

async def test_predict(client):
    target = "features"
    data = {"features": [5.1, 3.5, 1.4]}  # match your RF model features
    try:
        r = await client.post(f"{BASE_URL}/predict", json=data, timeout=30.0)
        result = r.json()
    except Exception as e:
        result = {"error": str(e)}
    print("---- PREDICT ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/predict", target, result)

async def test_history(client):
    target = "last5"
    try:
        r = await client.get(f"{BASE_URL}/history?limit=5", timeout=30.0)
        result = r.json()
    except Exception as e:
        result = {"error": str(e)}
    print("---- HISTORY ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/history", target, result)

# ----------- Main Async Runner ----------- #
async def main():
    # Add CSV header if file doesn't exist
    try:
        with open(CSV_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "endpoint", "target", "output"])
    except FileExistsError:
        pass

    timeout = httpx.Timeout(60.0)  # overall timeout
    async with httpx.AsyncClient(timeout=timeout) as client:
        await asyncio.gather(
            test_ping(client),
            test_dns(client),
            test_speedtest(client),
            test_predict(client),
            test_history(client),
            test_traceroute(client),
        )

if __name__ == "__main__":
    asyncio.run(main())
