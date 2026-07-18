import os
import sys
import json
from urllib import request, error

PORT = int(os.environ.get("TEST_PORT", "8002"))
BASE = f"http://127.0.0.1:{PORT}"

def post_json(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(BASE + path, data=data, headers={"Content-Type":"application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=5) as resp:
            return resp.status, json.load(resp)
    except error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
        except:
            body = e.read().decode()
        return e.code, body
    except error.URLError as e:
        print(f"Connection error: {e.reason}")
        sys.exit(2)
    except Exception as e:
        print(f"Request error: {e}")
        sys.exit(2)

def get_json(path):
    req = request.Request(BASE + path, method="GET")
    try:
        with request.urlopen(req, timeout=5) as resp:
            return resp.status, json.load(resp)
    except error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
        except:
            body = e.read().decode()
        return e.code, body
    except error.URLError as e:
        print(f"Connection error: {e.reason}")
        sys.exit(2)
    except Exception as e:
        print(f"Request error: {e}")
        sys.exit(2)

def main():
    print("Testing /analyze...")
    status, body = post_json("/analyze", {"content":"This is a test. One. Two."})
    if status != 200 or not isinstance(body, dict) or "key_points" not in body:
        print("/analyze failed:", status, body)
        sys.exit(1)
    print("/analyze OK")

    print("Testing /progress POST...")
    payload = {"user_id":"testuser","topic":"testing","score":42}
    status, body = post_json("/progress", payload)
    if status != 200 or not isinstance(body, dict) or body.get("status") != "saved":
        print("/progress POST failed:", status, body)
        sys.exit(1)
    print("/progress POST OK")

    print("Testing /progress GET...")
    status, body = get_json(f"/progress/{payload['user_id']}")
    if status != 200 or not isinstance(body, list) or not any(item[0] == payload['user_id'] for item in body):
        print("/progress GET failed:", status, body)
        sys.exit(1)
    print("/progress GET OK")

    print("All tests passed.")

if __name__ == '__main__':
    main()
