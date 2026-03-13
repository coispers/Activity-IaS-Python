import json
import sys

from client_helper import file_request

success = False

status, body = file_request(
    "http://localhost:3001/file-request-v1?name=salary.xlsx&user=adminCed"
)
print("Status:", status)
print("Response:", body)

try:
    data = json.loads(body)
    if status == 401 and data.get("error") == "Missing access token":
        success = True
    else:
        print("Validation error: expected missing-token 401 response.")
except json.JSONDecodeError:
    print("Validation error: response is not valid JSON.")

if not success:
    sys.exit(1)
