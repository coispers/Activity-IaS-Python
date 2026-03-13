import sys

from client_helper import file_request, login_and_get_token

success = True

try:
    # Replay test: use the same token twice for the same privileged request.
    token = login_and_get_token("adminCed", "admin123")

    status1, body1 = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=adminCed",
        token,
    )
    print("First use status:", status1)
    print("First use response:", body1)

    status2, body2 = file_request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx&user=adminCed",
        token,
    )
    print("Replay use status:", status2)
    print("Replay use response:", body2)

    if status1 == 200 and status2 == 200:
        print("Result: VULNERABLE - replay token accepted")
        success = False
    elif status1 == 200 and status2 in (401, 403):
        print("Result: REPLAY BLOCKED")
    else:
        print("Result: Unexpected behavior during replay test")
        success = False
except Exception as err:
    print("Unexpected error:", err)
    success = False

if not success:
    sys.exit(1)
