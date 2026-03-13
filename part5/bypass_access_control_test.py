import json
import sys

from client_helper import file_request, login_and_get_token

success = False

try:
    # Staff tries to access manager-only salary file.
    staff_token = login_and_get_token("employeeStyl", "employee123")
    status, body = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=employeeStyl",
        staff_token,
    )

    print("Status:", status)
    print("Response:", body)

    data = json.loads(body)
    if status == 403 and data.get("error") == "Access denied":
        print("Result: BYPASS BLOCKED")
        success = True
    else:
        print("Result: VULNERABLE - access control bypass succeeded")
except Exception as err:
    print("Unexpected error:", err)

if not success:
    sys.exit(1)
