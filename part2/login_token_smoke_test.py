import sys

from client_helper import login_and_get_token

success = False

try:
    token = login_and_get_token("adminCed", "admin123")
    print("Token acquired:", token[:24] + "...")
    success = True
except Exception as err:
    print("Login/token error:", err)

if not success:
    sys.exit(1)
