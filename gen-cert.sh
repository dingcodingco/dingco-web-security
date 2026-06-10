#!/usr/bin/env bash
#
# gen-cert.sh — openssl 로 자체서명(self-signed) SSL 인증서를 만든다.
#
# 기존 강의(goorm)에서 배운 2단계를 그대로 로컬에서 재현한다.
#   1) 개인키(private key) + 인증요청서(CSR) 생성
#   2) 그 CSR 을 "내 개인키로 직접 서명" 해서 인증서(.crt) 발급 = 자체서명
#
# CA(공인 인증기관)가 서명한 게 아니라 내가 나를 서명했기 때문에,
# 브라우저는 "신뢰할 수 없는 인증서"라고 경고한다. 그게 정상이고, 그걸 배우는 게 목표다.
set -euo pipefail
cd "$(dirname "$0")"

CERT_DIR="certs"
mkdir -p "$CERT_DIR"

echo "▶ 1단계: 개인키(dingco-ssl.key) + 인증요청서(dingco-ssl.csr) 생성"
openssl req -new \
  -newkey rsa:2048 -nodes \
  -keyout "$CERT_DIR/dingco-ssl.key" \
  -out    "$CERT_DIR/dingco-ssl.csr" \
  -config san.cnf

echo "▶ 2단계: CSR 을 내 개인키로 자체서명 → 인증서(dingco-ssl.crt) 발급 (유효기간 365일)"
openssl x509 -req -days 365 \
  -in      "$CERT_DIR/dingco-ssl.csr" \
  -signkey "$CERT_DIR/dingco-ssl.key" \
  -out     "$CERT_DIR/dingco-ssl.crt" \
  -extfile san.cnf -extensions v3_ext

echo
echo "✅ 인증서 생성 완료:"
ls -1 "$CERT_DIR"
echo
echo "▶ 발급된 인증서 정보 (자체서명이라 subject == issuer):"
openssl x509 -in "$CERT_DIR/dingco-ssl.crt" -noout -subject -issuer
