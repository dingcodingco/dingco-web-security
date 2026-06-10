#!/usr/bin/env bash
#
# verify.sh — 로컬 HTTPS 실습이 "정상 동작" 하는지 자동으로 검증한다.
#
# 사전 조건: ./gen-cert.sh 실행 + docker compose up -d 로 컨테이너 기동.
set -uo pipefail
cd "$(dirname "$0")"

PASS=0; FAIL=0
ok()   { echo "  ✅ $1"; PASS=$((PASS+1)); }
bad()  { echo "  ❌ $1"; FAIL=$((FAIL+1)); }

echo "=== 1) 인증서 파일 존재 확인 ==="
if [[ -f certs/dingco-ssl.crt && -f certs/dingco-ssl.key ]]; then
  ok "dingco-ssl.crt / dingco-ssl.key 존재"
else
  bad "인증서가 없다. 먼저 ./gen-cert.sh 를 실행하세요."
fi

echo "=== 2) HTTP(80) 응답 확인 ==="
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q 200; then
  ok "http://localhost → 200 OK"
else
  bad "http://localhost 응답 실패 (docker compose up -d 했는지 확인)"
fi

echo "=== 3) HTTPS(443) 응답 확인 (자체서명이라 -k 로 신뢰검사 우회) ==="
BODY=$(curl -sk https://localhost)
if echo "$BODY" | grep -q "딩코랩스"; then
  ok "https://localhost → 본문에 '딩코랩스' 포함 (HTTPS 정상 동작)"
else
  bad "HTTPS 본문 확인 실패"
fi

echo "=== 4) 인증서 주체/발급자 = 자체서명(O=dingco, CN=localhost) 확인 ==="
INFO=$(echo | openssl s_client -connect localhost:443 -servername localhost 2>/dev/null \
        | openssl x509 -noout -subject -issuer 2>/dev/null)
echo "$INFO" | sed 's/^/     /'
if echo "$INFO" | grep -q "CN *= *localhost" && echo "$INFO" | grep -q "O *= *dingco"; then
  ok "subject/issuer 가 우리가 만든 자체서명 인증서와 일치"
else
  bad "인증서 정보 불일치"
fi

echo "=== 5) 신뢰검사(-k 없이) 시 거부되는지 = 브라우저 경고 재현 ==="
if curl -s https://localhost >/dev/null 2>&1; then
  bad "신뢰검사를 통과해버렸다 (자체서명이면 거부돼야 정상)"
else
  ok "curl(신뢰검사) 거부됨 → '신뢰할 수 없는 인증서' 경고가 나는 것이 정상"
fi

echo
echo "──────────────────────────────"
echo "  통과 $PASS / 실패 $FAIL"
echo "──────────────────────────────"
[[ $FAIL -eq 0 ]]
