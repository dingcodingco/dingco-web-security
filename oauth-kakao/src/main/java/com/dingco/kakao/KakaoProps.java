package com.dingco.kakao;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * application.yml 의 kakao.* 설정.
 * 학생은 카카오 개발자 콘솔에서 발급받은 본인 키만 채워 넣으면 된다.
 */
@ConfigurationProperties(prefix = "kakao")
public record KakaoProps(
        String clientId,     // REST API 키
        String clientSecret, // 카카오 로그인 > 보안 > client_secret
        String redirectUri   // http://localhost:8080/social/login/kakao
) {
    /** 사용자를 보낼 카카오 인가(authorize) URL */
    public String authorizeUrl() {
        return "https://kauth.kakao.com/oauth/authorize"
                + "?client_id=" + clientId
                + "&response_type=code"
                + "&redirect_uri=" + redirectUri;
    }
}
