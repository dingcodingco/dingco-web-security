# 딩코딩코웹 OAuth 체험 — Spring Authorization Server

강의 4주차 "OAuth 체험" 실습 소스. 하나의 Spring Boot 앱이 **OAuth2 인가 서버**가 되어,
`authorization_code → access_token` 플로우를 로컬에서 그대로 돌려본다.

- Resource Owner(유저): `dingco` / `1234`
- Client(딩코딩코웹): `client_id=dingco-web`, `client_secret=dingco-secret`
- 인가 서버: http://127.0.0.1:9000

## 실행
```bash
./gradlew bootRun          # 포트 9000
```

## 플로우 체험
1. 브라우저에서 인가 요청:
   `http://127.0.0.1:9000/oauth2/authorize?response_type=code&client_id=dingco-web&redirect_uri=http://127.0.0.1:9000/callback&scope=openid%20profile`
2. `dingco / 1234` 로그인 → `/callback?code=...` 로 **authorization_code** 발급
3. 코드를 토큰으로 교환:
```bash
curl -X POST http://127.0.0.1:9000/oauth2/token \
  -u dingco-web:dingco-secret \
  -d grant_type=authorization_code \
  -d code=<위에서 받은 code> \
  -d redirect_uri=http://127.0.0.1:9000/callback
```
→ `access_token`(JWT) · `id_token`(OIDC) · `refresh_token` 발급

## 스택
Java 21 · Spring Boot 3.3 · Spring Security OAuth2 Authorization Server 1.3
