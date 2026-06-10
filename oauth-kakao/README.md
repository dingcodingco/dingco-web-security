# 딩코딩코웹 — 카카오 OAuth 로그인 체험 (Spring)

강의 "OAuth 체험" 의 어플리케이션 코드. `authorization_code` 흐름을 **직접** 다뤄본다.

- Resource Server = 카카오 / Client = 딩코딩코웹(이 앱) / Resource Owner = 로그인하는 유저
- 포트 8080, Spring Boot 3.3 · Java 21 (Spring Security 없이 web 만으로 수동 구현)

## 1) 카카오 키 설정
[카카오 개발자 콘솔](https://developers.kakao.com)에서 앱을 만들고 카카오 로그인을 켠 뒤,
Redirect URI 에 `http://localhost:8080/social/login/kakao` 를 등록한다.
그리고 `src/main/resources/application.yml` 에 본인 키를 입력:

```yaml
kakao:
  client-id: <REST API 키>
  client-secret: <카카오 로그인 > 보안 > Client Secret>
  redirect-uri: http://localhost:8080/social/login/kakao
```
(또는 환경변수 `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET` 로 주입)

## 2) 실행
```bash
./gradlew bootRun     # 포트 8080
```
`http://localhost:8080` 접속 → **Social Login (카카오)** 버튼 클릭

## 흐름
1. 버튼 → `https://kauth.kakao.com/oauth/authorize?client_id=...&response_type=code&redirect_uri=...`
2. 카카오 로그인/동의 → `/social/login/kakao?code=...` 로 리다이렉트
3. `KakaoLoginController` 가 `code` 로 `POST https://kauth.kakao.com/oauth/token` → **access_token** 교환
4. `access_token` 으로 `GET https://kapi.kakao.com/v2/user/me` → 사용자 정보 표시

> 카카오 키는 **본인 것**이 필요합니다. 카카오 계정·앱 등록 없이 OAuth 흐름만 보고 싶다면 옆 폴더 `oauth-spring`(자체 인가서버) 을 사용하세요.
