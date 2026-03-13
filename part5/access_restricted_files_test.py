import json
import sys

from client_helper import file_request, login_and_get_token

success = True

try:
    # Attempt 1: no token should be denied.
    status1, body1 = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=adminCed"
    )
    print("No token status:", status1)
    print("No token response:", body1)
    data1 = json.loads(body1)
    if not (status1 == 401 and data1.get("error") == "Missing access token"):
        print("Result: VULNERABLE - restricted file accessible without token")
        success = False

    # Attempt 2: token identity mismatch should be denied.
    manager_token = login_and_get_token("adminCed", "admin123")
    status2, body2 = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=employeeStyl",
        manager_token,
    )
    print("Mismatch status:", status2)
    print("Mismatch response:", body2)
    data2 = json.loads(body2)
    if not (status2 == 403 and data2.get("error") == "User identity mismatch"):
        print("Result: VULNERABLE - user mismatch accepted")
        success = False

    if success:
        print("Result: RESTRICTED FILE ACCESS BLOCKED")
except Exception as err:
    print("Unexpected error:", err)
    success = False

if not success:
    sys.exit(1)
