package com.dingco.kakao;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

/**
 * 딩코딩코웹 — 카카오 OAuth 소셜 로그인 체험 (Client 역할)
 *
 * 강의 "OAuth 체험" 의 어플리케이션 코드. authorization_code 흐름을 직접 다뤄본다.
 *  1) 홈(/)의 "Social Login" 버튼 → 카카오 인가 화면으로 이동
 *  2) 로그인/동의 후 카카오가 /social/login/kakao?code=... 로 리다이렉트
 *  3) 그 code 로 카카오 토큰 엔드포인트에 access_token 을 요청(교환)
 *  4) access_token 으로 카카오 사용자 정보를 가져와 화면에 표시
 *
 * Resource Server = 카카오 / Client = 딩코딩코웹(이 앱) / Resource Owner = 로그인하는 유저
 */
@SpringBootApplication
@EnableConfigurationProperties(KakaoProps.class)
public class KakaoOAuthApplication {
    public static void main(String[] args) {
        SpringApplication.run(KakaoOAuthApplication.class, args);
    }
}
