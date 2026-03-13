import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from flask import Flask, request, jsonify

app = Flask(__name__)
users = {"adminCed": "admin123", "employeeStyl": "employee123"}
roles = {"adminCed": "manager", "employeeStyl": "staff"}
INTER_SERVICE_SECRET = os.getenv("INTER_SERVICE_SECRET", "change-this-shared-secret")


def create_access_token(username: str, role: str, ttl_seconds: int = 300) -> str:
    payload = {
        "user": username,
        "role": role,
        "exp": int(time.time()) + ttl_seconds,
        "jti": secrets.token_hex(16),
    }
    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    payload_b64 = (
        base64.urlsafe_b64encode(payload_json.encode("utf-8"))
        .decode("utf-8")
        .rstrip("=")
    )
    signature = hmac.new(
        INTER_SERVICE_SECRET.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload_b64}.{signature}"


@app.route("/login-request-v1", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data["username"]
    password = data["password"]
    if username in users and users[username] == password:
        role = roles[username]
        token = create_access_token(username, role)
        return jsonify(
            {
                "status": "success",
                "user": username,
                "role": role,
                "accessToken": token,
                "tokenType": "HMAC-SHA256",
                "expiresInSeconds": 300,
            }
        )
    return jsonify({"status": "fail"}), 401


app.run(port=3000)
