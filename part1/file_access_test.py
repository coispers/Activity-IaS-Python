import json
import sys
import urllib.error
import urllib.request

url = "http://localhost:3001/file-request-v1?name=salary.xlsx"
success = False

try:
    with urllib.request.urlopen(url) as res:
        body = res.read().decode("utf-8")
        print("Status:", res.status)
        print("Response:", body)

        try:
            payload = json.loads(body)
            if payload.get("encrypted"):
                print("Note: file payload is encrypted as expected.")
                success = True
            else:
                print("Validation error: response is not encrypted.")
        except json.JSONDecodeError:
            print("Validation error: response body is not valid JSON.")
except urllib.error.HTTPError as err:
    error_body = err.read().decode("utf-8", errors="replace")
    print("HTTP error:", err.code)
    print("Response:", error_body)
    try:
        payload = json.loads(error_body)
        if err.code == 401 and payload.get("error") == "Missing access token":
            print("Note: hardened mode is active and unauthorized access is blocked.")
            success = True
    except json.JSONDecodeError:
        pass
except urllib.error.URLError as err:
    print("Request error:", err.reason)
except Exception as err:
    print("Unexpected error:", err)

if not success:
    sys.exit(1)
