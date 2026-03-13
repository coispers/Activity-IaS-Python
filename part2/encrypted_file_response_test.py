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
    encrypted_flag = data.get("encrypted") is True
    algorithm_ok = data.get("algorithm") == "Fernet"
    no_plaintext = "Confidential salary data" not in body

    if status == 200 and encrypted_flag and algorithm_ok and no_plaintext:
        success = True
    else:
        print("Validation error: encryption checks failed.")
except Exception as err:
    print("Request error:", err)

if not success:
    sys.exit(1)
