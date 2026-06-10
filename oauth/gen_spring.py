# -*- coding: utf-8 -*-
import html, os
def term(title, lines, fname):
    body=[]
    for ln in lines:
        cls='cmd' if ln.startswith('$ ') else ('ok' if ln.startswith(('▶','✅','#')) else 'out')
        body.append(f'<div class="{cls}">{html.escape(ln) if ln else "&nbsp;"}</div>')
    h=f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    body{{margin:0;background:#1e2128;font-family:'SF Mono',Menlo,Consolas,monospace}}
    .win{{margin:22px;border-radius:12px;overflow:hidden;box-shadow:0 16px 50px rgba(0,0,0,.5);max-width:900px}}
    .bar{{background:#343a46;height:38px;display:flex;align-items:center;padding:0 14px;gap:8px}}
    .dot{{width:13px;height:13px;border-radius:50%}}.r{{background:#ff5f57}}.y{{background:#febc2e}}.g{{background:#28c840}}
    .ttl{{color:#aab2c0;font-size:13px;margin-left:12px}}
    .scr{{background:#1b1e25;padding:18px 20px;font-size:14px;line-height:1.55}}
    .cmd{{color:#7ee787}}.out{{color:#d6dae2;white-space:pre-wrap}}.ok{{color:#79c0ff}}
    </style></head><body><div class="win"><div class="bar">
    <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
    <div class="ttl">{html.escape(title)}</div></div><div class="scr">{''.join(body)}</div></div></body></html>'''
    open(fname,'w').write(h)

os.makedirs('out', exist_ok=True)

term("① Spring OAuth2 인가 서버 — 프로젝트 구조 & 핵심 코드", [
 "$ tree oauth-spring",
 "oauth-spring",
 " ├─ build.gradle              # spring-security-oauth2-authorization-server",
 " ├─ settings.gradle",
 " └─ src/main",
 "     ├─ java/com/dingco/oauth",
 "     │   ├─ OAuthDemoApplication.java",
 "     │   ├─ AuthorizationServerConfig.java   # 핵심 설정",
 "     │   └─ CallbackController.java",
 "     └─ resources/application.yml            # port 9000",
 "",
 "# AuthorizationServerConfig.java — Client(딩코딩코웹) 등록",
 "RegisteredClient.withId(UUID.randomUUID().toString())",
 "    .clientId(\"dingco-web\")",
 "    .clientSecret(encoder.encode(\"dingco-secret\"))",
 "    .authorizationGrantType(AUTHORIZATION_CODE)",
 "    .redirectUri(\"http://127.0.0.1:9000/callback\")",
 "    .scope(OPENID).scope(PROFILE).build();",
], "out/sp1_code.html")

term("② 인가 서버 실행 — gradle bootRun", [
 "$ ./gradlew bootRun",
 "  .   ____          _            __ _ _",
 " /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\",
 "( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\",
 " \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )",
 "  '  |____| .__|_| |_|_| |_\\__, | / / / /",
 " =========|_|==============|___/=/_/_/_/",
 " :: Spring Boot ::                (v3.3.5)",
 "",
 "INFO --- OAuthDemoApplication : Starting OAuthDemoApplication using Java 21.0.2",
 "INFO --- TomcatWebServer      : Tomcat started on port 9000 (http)",
 "INFO --- OAuthDemoApplication : Started OAuthDemoApplication in 2.525 seconds",
 "",
 "✅ 인가 서버 가동 — http://127.0.0.1:9000",
], "out/sp2_run.html")

term("⑤ authorization_code → access_token 교환 (POST /oauth2/token)", [
 "$ curl -X POST http://127.0.0.1:9000/oauth2/token \\",
 "     -u dingco-web:dingco-secret \\",
 "     -d grant_type=authorization_code \\",
 "     -d code=YfbBAmDat_lgAQTApEyuwTxwUvKy1B2mEqYCyZ04BES6... \\",
 "     -d redirect_uri=http://127.0.0.1:9000/callback",
 "",
 "{",
 '  "access_token": "eyJraWQiOiI4MTIxZGU3Mi00ZGEz...0VOlaGYZWgA",  # JWT',
 '  "refresh_token": "XKrjKClA_dc78UDT7_QbWeZLVM6t...7YpY",',
 '  "scope": "openid profile",',
 '  "id_token": "eyJraWQiOiI4MTIxZGU3Mi00ZGEz...P6P0OQ0EQ",  # OIDC',
 '  "token_type": "Bearer",',
 '  "expires_in": 299',
 "}",
 "",
 "✅ 액세스 토큰 발급 완료 — 이 토큰으로 보호된 리소스를 호출한다",
], "out/sp3_token.html")
print("generated sp1/sp2/sp3 html")
