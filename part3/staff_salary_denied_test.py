import json
import sys

from client_helper import file_request, login_and_get_token

success = False

try:
    token = login_and_get_token("employeeStyl", "employee123")
    status, body = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=employeeStyl",
        token,
    )
    print("Status:", status)
    print("Response:", body)

    try:
        data = json.loads(body)
        if status == 403 and data.get("requiredRole") == "manager":
            success = True
        else:
            print("Validation error: denial response does not match policy.")
    except json.JSONDecodeError:
        print("Validation error: denial response is not valid JSON.")
except Exception as err:
    print("Unexpected error:", err)

if not success:
    sys.exit(1)
