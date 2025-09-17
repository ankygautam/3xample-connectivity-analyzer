import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_ping():
    data = {"host": "google.com"}
    r = requests.post(f"{BASE_URL}/ping", json=data)
    print("---- PING ----")
    print(json.dumps(r.json(), indent=2))

def test_traceroute():
    data = {"host": "google.com"}
    r = requests.post(f"{BASE_URL}/traceroute", json=data)
    print("---- TRACEROUTE ----")
    print(json.dumps(r.json(), indent=2))

def test_dns():
    data = {"domain": "google.com"}
    r = requests.post(f"{BASE_URL}/dns", json=data)
    print("---- DNS ----")
    print(json.dumps(r.json(), indent=2))

def test_speedtest():
    r = requests.get(f"{BASE_URL}/speedtest")
    print("---- SPEEDTEST ----")
    print(json.dumps(r.json(), indent=2))

def test_predict():
    data = {"features": [5.1, 3.5, 1.4]}  # replace with valid features for your model
    r = requests.post(f"{BASE_URL}/predict", json=data)
    print("---- PREDICT ----")
    print(json.dumps(r.json(), indent=2))

def test_history():
    r = requests.get(f"{BASE_URL}/history?limit=5")
    print("---- HISTORY ----")
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    test_ping()
    test_traceroute()
    test_dns()
    test_speedtest()
    test_predict()
    test_history()
