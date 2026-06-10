package com.dingco.oauth;

import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

import java.util.Base64;
import java.util.Map;

/**
 * Client(딩코딩코웹)의 redirect_uri.
 * 동의까지 마치면 인가 서버가 ?code=... 로 이 주소로 돌려보낸다.
 * 받은 authorization_code 로 (1) access_token 을 교환하고 (2) 그 토큰으로 사용자 정보까지 가져와 한 화면에 보여준다.
 *   — 카카오 실습의 "access_token 화면 / 유저정보로 회원가입" 단계와 동일한 흐름.
 */
@RestController
public class CallbackController {

    private static final String BASE = "http://127.0.0.1:9000";
    private static final String REDIRECT_URI = BASE + "/callback";
    private final RestClient rest = RestClient.create();

    @GetMapping(value = "/callback", produces = MediaType.TEXT_HTML_VALUE)
    public String callback(@RequestParam(required = false) String code,
                           @RequestParam(required = false) String error) {
        if (error != null || code == null) {
            return "<h2>인가 실패: " + (error == null ? "code 없음" : error.replace("<", "&lt;")) + "</h2>";
        }

        // 1) authorization_code → access_token 교환 (Client 인증: dingco-web / dingco-secret)
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("grant_type", "authorization_code");
        form.add("code", code);
        form.add("redirect_uri", REDIRECT_URI);
        String basic = Base64.getEncoder().encodeToString("dingco-web:dingco-secret".getBytes());

        Map<?, ?> token = rest.post().uri(BASE + "/oauth2/token")
                .header("Authorization", "Basic " + basic)
                .contentType(MediaType.APPLICATION_FORM_URLENCODED)
                .body(form).retrieve().body(Map.class);
        String accessToken = token == null ? null : String.valueOf(token.get("access_token"));
        String idToken = token == null ? null : String.valueOf(token.get("id_token"));

        // 2) 사용자 정보 — OIDC id_token 의 payload(클레임)를 디코드해 확인
        //    (카카오 실습의 "access_token 으로 유저 정보 가져오기" 단계에 해당)
        String userinfo = decodeJwtPayload(idToken);

        return """
            <html><head><meta charset="utf-8"><style>
              body{font-family:-apple-system,'Apple SD Gothic Neo',sans-serif;background:#0f1115;color:#e7e9ee;
                   display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
              .card{background:#1a1d24;padding:36px 44px;border-radius:16px;max-width:680px;box-shadow:0 8px 40px rgba(0,0,0,.4)}
              h1{margin:0 0 16px;font-size:22px}
              .label{color:#9aa0ac;font-size:13px;margin:14px 0 6px}
              code{display:block;background:#2a2f3a;color:#7ee787;padding:12px 14px;border-radius:8px;
                   word-break:break-all;font-size:13px}
              .ok{color:#79c0ff}
            </style></head><body><div class="card">
              <h1>🎉 로그인 성공!</h1>
              <div class="label">① 받은 authorization_code</div><code>%s</code>
              <div class="label">② 교환한 access_token</div><code>%s</code>
              <div class="label">③ 사용자 정보 (id_token 클레임)</div><code>%s</code>
            </div></body></html>
            """.formatted(code, accessToken, userinfo.replace("<", "&lt;"));
    }

    /** JWT(id_token)의 payload 부분을 base64url 디코드해 사람이 읽을 수 있게 반환 */
    private String decodeJwtPayload(String jwt) {
        if (jwt == null || !jwt.contains(".")) return "(없음)";
        try {
            String[] parts = jwt.split("\\.");
            return new String(Base64.getUrlDecoder().decode(parts[1]));
        } catch (Exception e) {
            return "(디코드 실패)";
        }
    }
}
