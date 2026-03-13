import json
import sys

from client_helper import file_request, login_and_get_token

success = False

try:
    token = login_and_get_token("adminCed", "admin123")
    status, body = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=employeeStyl",
        token,
    )
    print("Status:", status)
    print("Response:", body)

    data = json.loads(body)
    if status == 403 and data.get("error") == "User identity mismatch":
        success = True
    else:
        print("Validation error: expected user identity mismatch denial.")
except Exception as err:
    print("Request error:", err)

if not success:
    sys.exit(1)
