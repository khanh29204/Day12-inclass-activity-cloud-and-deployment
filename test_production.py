#!/usr/bin/env python3
"""
Script test production cho deployment AI Agent.
Domain mặc định: https://day12.quockhanh020924.id.vn

Sử dụng:
    python test_production.py --api-key YOUR_API_KEY
    python test_production.py --url https://day12.quockhanh020924.id.vn --api-key YOUR_API_KEY
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_DOMAIN = "https://day12.quockhanh020924.id.vn"


def make_request(url: str, method: str = "GET", headers: dict = None, data: dict = None):
    if headers is None:
        headers = {}
    
    encoded_data = None
    if data is not None:
        encoded_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status_code = resp.status
            response_body = resp.read().decode("utf-8")
            try:
                parsed_json = json.loads(response_body)
            except Exception:
                parsed_json = response_body
            return status_code, parsed_json
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            parsed_json = json.loads(body)
        except Exception:
            parsed_json = body
        return e.code, parsed_json
    except Exception as e:
        return 0, str(e)


def run_tests(base_url: str, api_key: str):
    base_url = base_url.rstrip("/")
    print(f"🚀 Bắt đầu test Production cho: {base_url}\n" + "=" * 60)

    passed = 0
    total = 0

    def assert_test(name: str, condition: bool, details: str = ""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"  ✅ [PASS] {name}")
        else:
            print(f"  ❌ [FAIL] {name}")
            if details:
                print(f"     -> {details}")

    # Test 1: GET /health
    print("\n1. Test GET /health:")
    status, body = make_request(f"{base_url}/health")
    assert_test("Status code is 200", status == 200, f"Got status {status}")
    assert_test(
        "Response status is 'ok'",
        isinstance(body, dict) and body.get("status") == "ok",
        f"Got body: {body}"
    )

    # Test 2: GET /ready
    print("\n2. Test GET /ready:")
    status, body = make_request(f"{base_url}/ready")
    assert_test("Status code is 200", status == 200, f"Got status {status}")
    assert_test(
        "Response status is 'ready'",
        isinstance(body, dict) and body.get("status") == "ready",
        f"Got body: {body}"
    )

    # Test 3: POST /ask thiếu API key (Expect 401)
    print("\n3. Test POST /ask thiếu X-API-Key (Unauthorized guard):")
    status, body = make_request(
        f"{base_url}/ask",
        method="POST",
        data={"question": "Test missing key"}
    )
    assert_test("Status code is 401", status == 401, f"Got status {status}")

    # Test 4: POST /ask với sai API key (Expect 401)
    print("\n4. Test POST /ask sai X-API-Key:")
    status, body = make_request(
        f"{base_url}/ask",
        method="POST",
        headers={"X-API-Key": "invalid-key-xyz-123"},
        data={"question": "Test wrong key"}
    )
    assert_test("Status code is 401", status == 401, f"Got status {status}")

    # Test 5: POST /ask hợp lệ với X-API-Key
    print("\n5. Test POST /ask hợp lệ:")
    if not api_key:
        print("  ⚠️  Bỏ qua (chưa truyền --api-key hoặc chưa set APP_API_KEY)")
    else:
        status, body = make_request(
            f"{base_url}/ask",
            method="POST",
            headers={"X-API-Key": api_key},
            data={"question": "Tóm tắt checklist deployment cloud cho AI agent"}
        )
        assert_test("Status code is 200", status == 200, f"Got status {status}, body: {body}")
        assert_test(
            "Trả về câu trả lời hợp lệ",
            isinstance(body, dict) and "answer" in body and "request_id" in body,
            f"Got body: {body}"
        )

    # Test 6: POST /ask vượt quá độ dài tối đa (Cost guard - Expect 413)
    print("\n6. Test POST /ask câu hỏi quá dài (Cost guard 413):")
    if not api_key:
        print("  ⚠️  Bỏ qua (chưa truyền --api-key hoặc chưa set APP_API_KEY)")
    else:
        long_question = "A" * 2500
        status, body = make_request(
            f"{base_url}/ask",
            method="POST",
            headers={"X-API-Key": api_key},
            data={"question": long_question}
        )
        assert_test("Status code is 413", status == 413, f"Got status {status}, body: {body}")

    print("\n" + "=" * 60)
    print(f"📊 Kết quả: {passed}/{total} tests passed.")
    
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test production deployment AI Agent")
    parser.add_argument(
        "--url",
        default=os.environ.get("TARGET_URL", DEFAULT_DOMAIN),
        help=f"Target URL (Mặc định: {DEFAULT_DOMAIN})"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("APP_API_KEY", ""),
        help="API Key gửi qua header X-API-Key"
    )

    args = parser.parse_args()
    
    if not args.api_key:
        print("💡 Gợi ý: Bạn có thể truyền --api-key YOUR_KEY để chạy đầy đủ các test case gửi request.")
    
    run_tests(args.url, args.api_key)
