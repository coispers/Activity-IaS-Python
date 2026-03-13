import sys

from client_helper import file_request, login_and_get_token

success = False

try:
    token = login_and_get_token("adminCed", "admin123")
    status, body = file_request(
        "http://localhost:3001/file-request-v1?name=doesnotexist.txt&user=adminCed",
        token,
    )

    print("Status:", status)
    print("Response:", body)

    if status == 404:
        success = True
    else:
        print("Validation error: expected 404 for missing file.")
except Exception as err:
    print("Request error:", err)

if not success:
    sys.exit(1)
