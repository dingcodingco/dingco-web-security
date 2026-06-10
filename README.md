# 로컬에서 SSL 인증서 발급 + HTTPS 실습 (goorm 대체)

기존 강의는 goorm IDE(클라우드)에서 nginx 를 띄우고 SSL 을 적용했지만,
goorm 서비스가 종료되어 **내 컴퓨터(로컬)에서 Docker 로 동일하게** 실습한다.

흐름은 예전과 같다:
**nginx 웹서버를 띄운다 → openssl 로 자체서명 인증서를 만든다 → nginx 에 SSL 을 적용한다 → HTTPS 로 접속한다 → (자체서명이라) 브라우저가 경고한다.**

## 준비물
- Docker Desktop (실행 중이어야 함) — `docker --version` 으로 확인
- openssl, curl (macOS/대부분 리눅스 기본 내장)

## 실행 순서

```bash
# 1) 자체서명 인증서 발급 (개인키+CSR → 자체서명 .crt)
./gen-cert.sh

# 2) nginx 웹서버 기동 (80, 443 포트)
docker compose up -d

# 3) 동작 확인
#    - 브라우저에서 https://localhost 접속 → "신뢰할 수 없음" 경고 후 진행하면 페이지가 뜸
#    - 터미널 자동 검증:
./verify.sh

# 4) 정리
docker compose down
```

## 폴더 구조
```
web-security-to-new/
├─ san.cnf             # 인증서 입력값 + SAN(localhost) 설정
├─ gen-cert.sh         # openssl 2단계로 자체서명 인증서 발급 → certs/ 에 생성
├─ certs/              # (생성물) dingco-ssl.key / .csr / .crt
├─ nginx/default.conf  # nginx HTTPS(443) 설정
├─ html/index.html     # 실습 확인용 정적 페이지
├─ docker-compose.yml  # nginx:alpine 컨테이너 정의
└─ verify.sh           # 정상 동작 자동 검증 (5개 체크)
```

## 검증 결과 (실제 실행 확인됨)
- `http://localhost` → **200 OK**
- `https://localhost` → 페이지 정상 반환 (HTTPS 동작)
- 인증서 subject == issuer (`O=dingco, CN=localhost`) → **자체서명** 확인
- 신뢰검사 시 `curl: (60) SSL certificate problem: self signed certificate` → 브라우저 "신뢰할 수 없는 인증서" 경고와 동일 (정상)

## 포트 충돌 시
443/80 이 이미 사용 중이면 `docker-compose.yml` 의 ports 를
`"8443:443"`, `"8080:80"` 로 바꾸고 `https://localhost:8443` 로 접속한다.

## CA 가 서명한 "진짜" 인증서로 초록 자물쇠를 보고 싶다면
- 공개 도메인 + 무료 인증서: **Let's Encrypt** (certbot)
- 로컬 개발에서 신뢰되는 인증서: **mkcert** (로컬 CA 를 OS 신뢰 저장소에 등록)
