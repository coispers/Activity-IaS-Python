import json
import urllib.request

url = "http://localhost:3000/login-request-v1"
payload = {"username": "adminCed", "password": "admin123"}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(req) as res:
    body = res.read().decode("utf-8")
    print("Status:", res.status)
    print("Response:", body)
