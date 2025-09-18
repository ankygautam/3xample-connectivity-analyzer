import asyncio
import httpx
import json
import csv
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
CSV_FILE = "connectivity_test_results.csv"

# Utility to save result to CSV
def save_to_csv(endpoint, result):
    timestamp = datetime.now().isoformat()
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, endpoint, json.dumps(result)])

# ----------- Async Test Functions ----------- #
async def test_ping(client):
    data = {"host": "google.com"}
    r = await client.post(f"{BASE_URL}/ping", json=data)
    result = r.json()
    print("---- PING ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/ping", result)

async def test_traceroute(client):
    data = {"host": "google.com"}
    r = await client.post(f"{BASE_URL}/traceroute", json=data)
    result = r.json()
    print("---- TRACEROUTE ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/traceroute", result)

async def test_dns(client):
    data = {"domain": "google.com"}
    r = await client.post(f"{BASE_URL}/dns", json=data)
    result = r.json()
    print("---- DNS ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/dns", result)

async def test_speedtest(client):
    r = await client.get(f"{BASE_URL}/speedtest")
    result = r.json()
    print("---- SPEEDTEST ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/speedtest", result)

async def test_predict(client):
    data = {"features": [5.1, 3.5, 1.4]}  # adjust for your model
    r = await client.post(f"{BASE_URL}/predict", json=data)
    result = r.json()
    print("---- PREDICT ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/predict", result)

async def test_history(client):
    r = await client.get(f"{BASE_URL}/history?limit=5")
    result = r.json()
    print("---- HISTORY ----")
    print(json.dumps(result, indent=2))
    save_to_csv("/history", result)

# ----------- Main Async Runner ----------- #
async def main():
    # Add CSV header if file doesn't exist
    try:
        with open(CSV_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "endpoint", "result"])
    except FileExistsError:
        pass

    async with httpx.AsyncClient() as client:
        await asyncio.gather(
            test_ping(client),
            test_traceroute(client),
            test_dns(client),
            test_speedtest(client),
            test_predict(client),
            test_history(client)
        )

if __name__ == "__main__":
    asyncio.run(main())
