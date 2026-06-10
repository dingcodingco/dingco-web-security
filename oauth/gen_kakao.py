# -*- coding: utf-8 -*-
import html, os
def term(title, lines, fname):
    body=[]
    for ln in lines:
        cls='cmd' if ln.startswith('$ ') else ('ok' if ln.startswith(('▶','✅','#','//')) else 'out')
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

term("① 카카오 로그인 스프링 프로젝트 — 구조 & 핵심 코드", [
 "$ tree oauth-kakao",
 "oauth-kakao",
 " ├─ build.gradle",
 " └─ src/main",
 "     ├─ java/com/dingco/kakao",
 "     │   ├─ KakaoOAuthApplication.java",
 "     │   ├─ HomeController.java         // Social Login 버튼",
 "     │   ├─ KakaoLoginController.java   // code → access_token 교환",
 "     │   └─ KakaoProps.java             // kakao.client-id / secret",
 "     └─ resources/application.yml",
 "",
 "// KakaoLoginController — 받은 code 로 토큰을 직접 교환",
 'form.add("grant_type", "authorization_code");',
 'form.add("client_id", props.clientId());',
 'form.add("client_secret", props.clientSecret());',
 'form.add("code", code);',
 'var token = rest.post()',
 '    .uri("https://kauth.kakao.com/oauth/token")',
 '    .body(form).retrieve().body(Map.class);   // → access_token',
], "out/kakao1_code.html")

term("② 카카오 키 설정 후 서버 실행 — gradle bootRun", [
 "# application.yml 에 내 카카오 키 입력",
 "kakao:",
 "  client-id: 37976827a762741f03d100493fc1a281   # REST API 키",
 "  client-secret: ****************                # client_secret",
 "  redirect-uri: http://localhost:8080/social/login/kakao",
 "",
 "$ ./gradlew bootRun",
 " :: Spring Boot ::                (v3.3.5)",
 "INFO --- KakaoOAuthApplication : Starting KakaoOAuthApplication using Java 21.0.2",
 "INFO --- TomcatWebServer      : Tomcat started on port 8080 (http)",
 "INFO --- KakaoOAuthApplication : Started KakaoOAuthApplication in 0.7 seconds",
 "",
 "✅ http://localhost:8080 접속 → Social Login 버튼 클릭!",
], "out/kakao2_run.html")
print("generated kakao1/kakao2")
