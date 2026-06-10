package com.dingco.oauth;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Client(딩코딩코웹)의 redirect_uri 역할.
 * 인가 서버가 로그인 성공 후 ?code=... 를 붙여 이 주소로 리다이렉트한다.
 * 받은 authorization_code 를 화면에 보여줘서, 다음 단계(토큰 교환)에 쓰도록 한다.
 */
@RestController
public class CallbackController {

    @GetMapping(value = "/callback", produces = MediaType.TEXT_HTML_VALUE)
    public String callback(@RequestParam(required = false) String code,
                           @RequestParam(required = false) String error) {
        if (error != null) {
            return "<h2>인가 실패: " + escape(error) + "</h2>";
        }
        return """
            <html><head><meta charset="utf-8"><style>
              body{font-family:-apple-system,'Apple SD Gothic Neo',sans-serif;background:#0f1115;color:#e7e9ee;
                   display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
              .card{background:#1a1d24;padding:40px 48px;border-radius:16px;max-width:680px;box-shadow:0 8px 40px rgba(0,0,0,.4)}
              h1{margin:0 0 6px;font-size:22px}.sub{color:#9aa0ac;margin-bottom:22px}
              .label{color:#9aa0ac;font-size:13px;margin-bottom:6px}
              code{display:block;background:#2a2f3a;color:#7ee787;padding:14px 16px;border-radius:8px;
                   word-break:break-all;font-size:15px}
              .next{margin-top:22px;color:#9aa0ac;font-size:13.5px;line-height:1.6}
              .next b{color:#79c0ff}
            </style></head><body><div class="card">
              <h1>✅ 인가 성공 — authorization_code 발급</h1>
              <div class="sub">딩코딩코웹(Client) 이 인가 서버로부터 1회용 코드를 받았습니다.</div>
              <div class="label">authorization_code</div>
              <code>%s</code>
              <div class="next">이제 이 코드를 <b>client_secret</b> 과 함께 <b>/oauth2/token</b> 에 보내면<br>
              <b>access_token</b> 으로 교환됩니다. (다음 단계: 터미널에서 curl)</div>
            </div></body></html>
            """.formatted(escape(code));
    }

    private static String escape(String s) {
        return s == null ? "" : s.replace("<", "&lt;").replace(">", "&gt;");
    }
}
