package com.dingco.oauth;

import org.springframework.security.oauth2.core.endpoint.OAuth2ParameterNames;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.security.Principal;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * 동의(consent) 화면 — 카카오의 "딩코딩코웹이 회원님의 정보에 접근하려고 합니다" 화면에 해당.
 * 사용자가 어떤 권한(scope)을 Client(딩코딩코웹)에 허용할지 동의한다.
 */
@Controller
public class ConsentController {

    private static final Map<String, String> SCOPE_DESC = new LinkedHashMap<>() {{
        put("openid", "로그인 식별 (OpenID)");
        put("profile", "프로필 정보 (닉네임 등)");
        put("read", "내 데이터 읽기");
    }};

    @GetMapping("/oauth2/consent")
    @ResponseBody
    public String consent(Principal principal,
                          @RequestParam(OAuth2ParameterNames.CLIENT_ID) String clientId,
                          @RequestParam(OAuth2ParameterNames.SCOPE) String scope,
                          @RequestParam(OAuth2ParameterNames.STATE) String state) {
        StringBuilder rows = new StringBuilder();
        for (String s : scope.split(" ")) {
            if (s.isBlank()) continue;
            String desc = SCOPE_DESC.getOrDefault(s, s);
            rows.append("""
                <label class="scope"><input type="checkbox" name="scope" value="%s" checked>
                  <span><b>%s</b><br><small>%s</small></span></label>
                """.formatted(s, s, desc));
        }
        return """
            <html><head><meta charset="utf-8"><title>동의하고 계속하기</title><style>
              body{font-family:-apple-system,'Apple SD Gothic Neo',sans-serif;background:#0f1115;color:#e7e9ee;
                   display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
              .card{background:#1a1d24;padding:36px 40px;border-radius:16px;width:420px;box-shadow:0 8px 40px rgba(0,0,0,.4)}
              h1{font-size:20px;margin:0 0 4px}.sub{color:#9aa0ac;font-size:14px;margin-bottom:22px}
              .app{color:#FEE500;font-weight:700}
              .scope{display:flex;gap:12px;align-items:flex-start;background:#22262f;padding:14px 16px;
                     border-radius:10px;margin-bottom:10px}
              .scope small{color:#9aa0ac}
              button{width:100%%;margin-top:14px;background:#FEE500;color:#191600;border:0;font-weight:700;
                     padding:14px;border-radius:10px;font-size:15px;cursor:pointer}
            </style></head><body><div class="card">
              <h1><span class="app">딩코딩코웹</span> 이 회원님의 정보에 접근하려고 합니다</h1>
              <div class="sub">%s 님, 아래 권한에 동의하면 로그인이 완료됩니다.</div>
              <form method="post" action="/oauth2/authorize">
                <input type="hidden" name="client_id" value="%s">
                <input type="hidden" name="state" value="%s">
                %s
                <button type="submit">동의하고 계속하기</button>
              </form>
            </div></body></html>
            """.formatted(principal.getName(), clientId, state, rows.toString());
    }
}
