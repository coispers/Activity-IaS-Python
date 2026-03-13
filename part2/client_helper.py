import json
import urllib.error
import urllib.request


def login_and_get_token(username: str, password: str) -> str:
    url = "http://localhost:3000/login-request-v1"
    payload = {"username": username, "password": password}
    body = json.dumps(payload).encode("utf-8")

    request_obj = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request_obj) as response:
        response_body = response.read().decode("utf-8", errors="replace")
        data = json.loads(response_body)
        token = data.get("accessToken")
        if not token:
            raise ValueError("Login succeeded but access token is missing")
        return token


def file_request(url: str, token: str):
    request_obj = urllib.request.Request(url, method="GET")
    request_obj.add_header("X-Access-Token", token)

    try:
        with urllib.request.urlopen(request_obj) as response:
            body = response.read().decode("utf-8", errors="replace")
            return response.status, body
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        return err.code, body
