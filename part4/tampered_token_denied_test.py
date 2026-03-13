import json
import sys

from client_helper import file_request, login_and_get_token

success = False

try:
    token = login_and_get_token("adminCed", "admin123")
    tampered = token[:-1] + ("0" if token[-1] != "0" else "1")
    status, body = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=adminCed",
        tampered,
    )
    print("Status:", status)
    print("Response:", body)

    data = json.loads(body)
    if status == 401 and data.get("error") == "Invalid token signature":
        success = True
    else:
        print("Validation error: expected invalid-signature denial.")
except Exception as err:
    print("Request error:", err)

if not success:
    sys.exit(1)
