import json
import sys

from client_helper import file_request, login_and_get_token

success = False

try:
    token = login_and_get_token("adminCed", "admin123")
    status, body = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=adminCed",
        token,
    )
    print("Status:", status)
    print("Response:", body)

    data = json.loads(body)
    if (
        status == 200
        and data.get("encrypted") is True
        and data.get("role") == "manager"
    ):
        success = True
    else:
        print("Validation error: expected encrypted manager access with valid token.")
except Exception as err:
    print("Request error:", err)

if not success:
    sys.exit(1)
