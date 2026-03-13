import json
import sys

from client_helper import file_request, login_and_get_token

success = False

try:
    token = login_and_get_token("employeeStyl", "employee123")
    status, body = file_request(
        "http://localhost:3001/file-request-v1?name=meetingNotes.txt&user=employeeStyl",
        token,
    )
    print("Status:", status)
    print("Response:", body)

    data = json.loads(body)
    if status == 200 and data.get("encrypted") is True and data.get("role") == "staff":
        success = True
    else:
        print("Validation error: staff access response does not match policy.")
except Exception as err:
    print("Unexpected error:", err)

if not success:
    sys.exit(1)
