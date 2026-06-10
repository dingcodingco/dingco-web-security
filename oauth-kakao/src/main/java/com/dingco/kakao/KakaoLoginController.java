package com.dingco.kakao;

import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

import java.util.Map;

/**
 * 카카오가 로그인/동의 후 redirect_uri 로 돌려보내는 콜백.
 * 받은 authorization_code 로 access_token 을 "직접" 교환하고, 사용자 정보까지 가져온다.
 *
 *   code ─▶ POST https://kauth.kakao.com/oauth/token   (access_token 발급)
 *   access_token ─▶ GET https://kapi.kakao.com/v2/user/me  (사용자 정보)
 */
@RestController
public class KakaoLoginController {

    private final KakaoProps props;
    private final RestClient rest = RestClient.create();

    public KakaoLoginController(KakaoProps props) {
        this.props = props;
    }

    @GetMapping(value = "/social/login/kakao", produces = MediaType.TEXT_HTML_VALUE)
    public String callback(@RequestParam(required = false) String code,
                           @RequestParam(required = false) String error) {
        if (error != null || code == null) {
            return page("로그인 실패", "error", "error = " + error);
        }

        // 1) authorization_code → access_token 교환
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("grant_type", "authorization_code");
        form.add("client_id", props.clientId());
        form.add("client_secret", props.clientSecret());
        form.add("redirect_uri", props.redirectUri());
        form.add("code", code);

        Map<?, ?> token = rest.post()
                .uri("https://kauth.kakao.com/oauth/token")
                .contentType(MediaType.APPLICATION_FORM_URLENCODED)
                .body(form)
                .retrieve()
                .body(Map.class);

        String accessToken = token == null ? null : String.valueOf(token.get("access_token"));

        // 2) access_token 으로 카카오 사용자 정보 조회
        Map<?, ?> me = rest.get()
                .uri("https://kapi.kakao.com/v2/user/me")
                .header("Authorization", "Bearer " + accessToken)
                .retrieve()
                .body(Map.class);

        return page("로그인 성공 🎉",
                "authorization_code → access_token 교환 완료",
                "받은 code: " + code + "\n\naccess_token: " + accessToken + "\n\n카카오 유저정보: " + me);
    }

    private String page(String title, String sub, String body) {
        return """
            <html><head><meta charset="utf-8"><style>
              body{font-family:-apple-system,'Apple SD Gothic Neo',sans-serif;background:#0f1115;color:#e7e9ee;
                   display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
              .card{background:#1a1d24;padding:40px 48px;border-radius:16px;max-width:720px;box-shadow:0 8px 40px rgba(0,0,0,.4)}
              h1{margin:0 0 6px}.sub{color:#9aa0ac;margin-bottom:18px}
              pre{background:#2a2f3a;color:#7ee787;padding:16px;border-radius:8px;white-space:pre-wrap;word-break:break-all;font-size:13px}
            </style></head><body><div class="card"><h1>%s</h1><div class="sub">%s</div><pre>%s</pre></div></body></html>
            """.formatted(title, sub, body == null ? "" : body.replace("<", "&lt;"));
    }
}
