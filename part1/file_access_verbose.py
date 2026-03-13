import http.client
import json
import sys

host = "localhost"
port = 3001
path = "/file-request-v1?name=salary.xlsx"

conn = http.client.HTTPConnection(host, port, timeout=5)
conn.set_debuglevel(1)  # prints raw request/response details

headers = {
    "User-Agent": "python-http.client",
    "Accept": "*/*",
}

success = False

try:
    print("> GET", path, "HTTP/1.1")
    for k, v in headers.items():
        print(f"> {k}: {v}")

    conn.request("GET", path, headers=headers)
    res = conn.getresponse()

    print(f"< HTTP/1.1 {res.status} {res.reason}")
    for k, v in res.getheaders():
        print(f"< {k}: {v}")

    body = res.read().decode("utf-8", errors="replace")
    print("\nBody:", body)

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        payload = {}

    if res.status == 200 and payload.get("encrypted"):
        success = True
    elif res.status == 401 and payload.get("error") == "Missing access token":
        print("Note: hardened mode is active and unauthorized access is blocked.")
        success = True
    elif res.status != 200:
        print(f"Validation error: expected status 200, got {res.status}.")
    else:
        print("Validation error: response is not encrypted.")
except ConnectionRefusedError:
    print("Request error: could not connect to file server on localhost:3001")
except http.client.HTTPException as err:
    print(f"HTTP client error: {err}")
except OSError as err:
    print(f"Network error: {err}")
except Exception as err:
    print(f"Unexpected error: {err}")
finally:
    conn.close()

if not success:
    sys.exit(1)
