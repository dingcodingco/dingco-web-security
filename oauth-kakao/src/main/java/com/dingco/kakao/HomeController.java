package com.dingco.kakao;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 홈 페이지 — "Social Login (카카오)" 버튼 하나.
 * 버튼은 카카오 인가 URL 로 이동시키는 단순한 링크다.
 */
@RestController
public class HomeController {

    private final KakaoProps props;

    public HomeController(KakaoProps props) {
        this.props = props;
    }

    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    public String home() {
        return """
            <html><head><meta charset="utf-8"><title>딩코딩코웹 - 카카오 로그인</title><style>
              body{font-family:-apple-system,'Apple SD Gothic Neo',sans-serif;background:#0f1115;color:#e7e9ee;
                   display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
              .card{background:#1a1d24;padding:48px 56px;border-radius:16px;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,.4)}
              h1{margin:0 0 8px;font-size:24px}.sub{color:#9aa0ac;margin-bottom:28px}
              a.btn{display:inline-block;background:#FEE500;color:#191600;text-decoration:none;font-weight:700;
                    padding:14px 26px;border-radius:10px;font-size:16px}
              .url{margin-top:22px;color:#6b7280;font-size:12px;max-width:520px;word-break:break-all}
            </style></head><body><div class="card">
              <h1>딩코딩코웹</h1>
              <div class="sub">카카오 계정으로 로그인해보세요</div>
              <a class="btn" href="%s">🟡 Social Login (카카오)</a>
              <div class="url">버튼이 이동시키는 주소:<br>%s</div>
            </div></body></html>
            """.formatted(props.authorizeUrl(), props.authorizeUrl());
    }
}
