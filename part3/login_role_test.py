import json
import sys
import urllib.error
import urllib.request

url = "http://localhost:3000/login-request-v1"
payload = {"username": "adminCed", "password": "admin123"}

request_data = json.dumps(payload).encode("utf-8")
request_obj = urllib.request.Request(
    url,
    data=request_data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

success = False

try:
    with urllib.request.urlopen(request_obj) as response:
        body = response.read().decode("utf-8", errors="replace")
        print("Status:", response.status)
        print("Response:", body)

        data = json.loads(body)
        if response.status == 200 and data.get("role") == "manager":
            success = True
        else:
            print("Validation error: expected role manager for adminCed.")
except urllib.error.HTTPError as err:
    print("HTTP error:", err.code)
    print("Response:", err.read().decode("utf-8", errors="replace"))
except urllib.error.URLError as err:
    print("Request error:", err.reason)
except Exception as err:
    print("Unexpected error:", err)

if not success:
    sys.exit(1)
