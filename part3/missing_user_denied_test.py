import json
import sys
import urllib.request

from client_helper import login_and_get_token

success = False

try:
    token = login_and_get_token("adminCed", "admin123")

    # This endpoint is now token-driven; missing user is acceptable when token is valid.
    request_obj = urllib.request.Request(
        "http://localhost:3001/file-request-v1?name=salary.xlsx",
        method="GET",
    )
    request_obj.add_header("X-Access-Token", token)

    with urllib.request.urlopen(request_obj) as response:
        body = response.read().decode("utf-8", errors="replace")
        print("Status:", response.status)
        print("Response:", body)

        data = json.loads(body)
        if (
            response.status == 200
            and data.get("encrypted") is True
            and data.get("user") == "adminCed"
        ):
            success = True
        else:
            print(
                "Validation error: token-based request without user did not behave as expected."
            )
except Exception as err:
    print("Unexpected error:", err)

if not success:
    sys.exit(1)
