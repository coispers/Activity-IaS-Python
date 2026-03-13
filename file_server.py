import base64
import hashlib
import hmac
import json
import os
import time

from cryptography.fernet import Fernet
from flask import Flask, request, jsonify

app = Flask(__name__)
files = {
    "salary.xlsx": "Confidential salary data",
    "meetingNotes.txt": "Meeting notes",
}
user_roles = {"adminCed": "manager", "employeeStyl": "staff"}
file_access_policy = {"salary.xlsx": "manager", "meetingNotes.txt": "staff"}
INTER_SERVICE_SECRET = os.getenv("INTER_SERVICE_SECRET", "change-this-shared-secret")
used_token_ids: dict[str, int] = {}


def build_fernet_key(secret: str) -> bytes:
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


ENCRYPTION_SECRET = os.getenv("FILE_SERVER_SECRET", "change-this-in-production")
cipher = Fernet(build_fernet_key(ENCRYPTION_SECRET))


def verify_access_token(token: str):
    try:
        payload_b64, provided_signature = token.split(".", 1)
    except ValueError:
        return None, "Invalid token format"

    expected_signature = hmac.new(
        INTER_SERVICE_SECRET.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(provided_signature, expected_signature):
        return None, "Invalid token signature"

    padding = "=" * (-len(payload_b64) % 4)
    try:
        payload_json = base64.urlsafe_b64decode(
            (payload_b64 + padding).encode("utf-8")
        ).decode("utf-8")
        payload = json.loads(payload_json)
    except Exception:
        return None, "Invalid token payload"

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        return None, "Token expired"

    return payload, None


def cleanup_used_tokens(now_ts: int) -> None:
    expired_ids = [token_id for token_id, exp in used_token_ids.items() if exp < now_ts]
    for token_id in expired_ids:
        used_token_ids.pop(token_id, None)


@app.route("/file-request-v1", methods=["GET"])
def get_file():
    filename = request.args.get("name")
    requested_user = request.args.get("user")
    token = request.headers.get("X-Access-Token") or request.args.get("token")

    if not token:
        return jsonify({"error": "Missing access token"}), 401

    token_payload, token_error = verify_access_token(token)
    if token_error:
        return jsonify({"error": token_error}), 401

    now_ts = int(time.time())
    cleanup_used_tokens(now_ts)

    username = token_payload.get("user")
    role = token_payload.get("role")
    token_id = token_payload.get("jti")
    token_exp = token_payload.get("exp")

    if not isinstance(token_id, str) or not token_id:
        return jsonify({"error": "Invalid token identifier"}), 401

    if token_id in used_token_ids:
        return jsonify({"error": "Replay token detected"}), 401

    if requested_user and requested_user != username:
        return jsonify({"error": "User identity mismatch"}), 403

    expected_role = user_roles.get(username)
    if expected_role is None:
        return jsonify({"error": "Unknown user"}), 403

    if role != expected_role:
        return jsonify({"error": "Invalid token role claim"}), 403

    file_content = files.get(filename)
    if file_content is None:
        return jsonify({"file": "Not Found"}), 404

    required_role = file_access_policy.get(filename)
    if required_role is None:
        return jsonify({"error": "No policy defined for file"}), 403

    if role != required_role:
        return jsonify({"error": "Access denied", "requiredRole": required_role}), 403

    used_token_ids[token_id] = token_exp

    encrypted_content = cipher.encrypt(file_content.encode("utf-8")).decode("utf-8")
    return jsonify(
        {
            "file": encrypted_content,
            "encrypted": True,
            "algorithm": "Fernet",
            "user": username,
            "role": role,
        }
    )


app.run(port=3001)
