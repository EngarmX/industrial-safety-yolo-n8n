import requests

# Your live cloud webhook link
url = "https://n8n.srv1459174.hstgr.cloud/webhook-test/safety-violation"

# Simple test payload
data = {
    "event": "Manual Ping Test",
    "status": "Testing connection from Python"
}

print("Firing test request to n8n cloud...")
try:
    response = requests.post(url, json=data, timeout=5)
    print(f"Response Code: {response.status_code}")
    print(f"Response Text: {response.text}")
except Exception as e:
    print(f"Connection failed! Error: {e}")