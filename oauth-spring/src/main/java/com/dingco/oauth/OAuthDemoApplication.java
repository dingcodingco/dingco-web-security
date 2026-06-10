package com.dingco.oauth;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 딩코딩코웹 OAuth 체험 데모.
 *
 * 하나의 Spring Boot 앱이 OAuth2 인가 서버(Authorization Server) 역할을 한다.
 * 강의의 OAuth 흐름(authorization_code → access_token)을 로컬에서 그대로 돌려볼 수 있다.
 *
 *  - Resource Owner(유저)      : dingco / 1234 로 로그인
 *  - Client(딩코딩코웹)         : client_id=dingco-web, client_secret=dingco-secret
 *  - Resource Server(인가 서버) : 이 앱 (http://127.0.0.1:9000)
 */
@SpringBootApplication
public class OAuthDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(OAuthDemoApplication.class, args);
    }
}
