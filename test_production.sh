#!/usr/bin/env bash
# Script test production nhanh bằng curl cho domain day12.quockhanh020924.id.vn

DOMAIN="${TARGET_URL:-https://day12.quockhanh020924.id.vn}"
API_KEY="${1:-$APP_API_KEY}"

echo "=================================================="
echo "🚀 Testing Production Domain: ${DOMAIN}"
echo "=================================================="

echo -e "\n1. Testing GET /health..."
curl -s -i "${DOMAIN}/health"

echo -e "\n\n2. Testing GET /ready..."
curl -s -i "${DOMAIN}/ready"

echo -e "\n\n3. Testing POST /ask không có API Key (Kỳ vọng: 401 Unauthorized)..."
curl -s -i -X POST "${DOMAIN}/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Test unauthorized"}'

if [ -n "$API_KEY" ]; then
  echo -e "\n\n4. Testing POST /ask hợp lệ với X-API-Key..."
  curl -s -i -X POST "${DOMAIN}/ask" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: ${API_KEY}" \
    -d '{"question":"Tóm tắt các bước deploy production"}'

  echo -e "\n\n5. Testing POST /ask câu hỏi quá dài (Kỳ vọng: 413 Payload Too Large)..."
  LONG_TEXT=$(printf 'A%.0s' {1..2500})
  curl -s -i -X POST "${DOMAIN}/ask" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: ${API_KEY}" \
    -d "{\"question\":\"${LONG_TEXT}\"}"
else
  echo -e "\n\n⚠️ Chưa nhập API Key. Sử dụng: ./test_production.sh <YOUR_API_KEY>"
fi

echo -e "\n=================================================="
