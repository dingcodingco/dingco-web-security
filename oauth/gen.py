# -*- coding: utf-8 -*-
# 토글 20 OAuth 흐름 다이어그램 재제작 (스코르타파딩클럽 → 딩코딩코웹, sparta@→dingco@, scopa.com→dingco.com)
import html, os

W, H = 660, 500
# 박스 좌표 (x,y,w,h)
BOX = {
    'O': (24, 214, 130, 76),   # Resource Owner (유저)  - green
    'C': (486, 28, 150, 76),   # Client (딩코딩코웹)     - red
    'S': (486, 396, 150, 76),  # Resource Server (페북) - blue
}
BOXLABEL = {
    'O': 'Resource<br>Owner<br>(유저)',
    'C': 'Client<br>(딩코딩코웹)',
    'S': 'Resource<br>Server<br>(페이스북)',
}
BOXCLS = {'O': 'owner', 'C': 'client', 'S': 'server'}

def center(b):
    x, y, w, h = BOX[b]; return (x + w / 2, y + h / 2)

# 연결 포트 (선이 닿는 박스 가장자리 지점)
PORT = {
    'O': {'right': (154, 252), 'bottom': (89, 290), 'top': (89, 214)},
    'C': {'left': (486, 64), 'bottom': (561, 104), 'leftlow': (486, 90)},
    'S': {'left': (486, 434), 'top': (561, 396), 'lefttop': (486, 410)},
}

def box_div(b):
    x, y, w, h = BOX[b]
    return (f'<div class="box {BOXCLS[b]}" style="left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;">{BOXLABEL[b]}</div>')

def label_div(cx, cy, lines, w=270):
    body = '<br>'.join(lines)
    return (f'<div class="lbl" style="left:{cx - w/2}px;top:{cy}px;width:{w}px;">'
            f'{body}</div>')

def line_svg(p1, p2, arrow=True):
    mk = ' marker-end="url(#ah)"' if arrow else ''
    return f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}"{mk}/>'

def circle_num(cx, cy, n):
    return (f'<circle cx="{cx}" cy="{cy}" r="17" class="numc"/>'
            f'<text x="{cx}" y="{cy+5}" class="numt">{n}</text>')

def render(spec):
    svg = [f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">',
           '<defs><marker id="ah" markerWidth="11" markerHeight="11" refX="8" refY="4" '
           'orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="#3a3f4a"/></marker></defs>']
    divs = [box_div('O'), box_div('C'), box_div('S')]
    # arrows
    for a in spec.get('arrows', []):
        svg.append(line_svg(a['p1'], a['p2']))
        if 'num' in a:
            mx = (a['p1'][0] + a['p2'][0]) / 2; my = (a['p1'][1] + a['p2'][1]) / 2
            nx, ny = a.get('numxy', (mx, my))
            svg.append(circle_num(nx, ny, a['num']))
    # labels
    for l in spec.get('labels', []):
        divs.append(label_div(l['x'], l['y'], l['lines'], l.get('w', 270)))
    # big labeled circles (numbered-flow diagram)
    for c in spec.get('bcircles', []):
        d = c['r'] * 2
        divs.append(f'<div class="bc" style="left:{c["x"]-c["r"]}px;top:{c["y"]-c["r"]}px;'
                    f'width:{d}px;height:{d}px;">{"<br>".join(c["lines"])}</div>')
        bx, by = c['badge']
        divs.append(f'<div class="badge" style="left:{bx}px;top:{by}px;">{c["num"]}</div>')
    # number badges for labels
    for l in spec.get('labels', []):
        if 'badge' in l:
            bx, by = l['badge']
            divs.append(f'<div class="badge" style="left:{bx}px;top:{by}px;">{l["num"]}</div>')
    # overlay
    ov = spec.get('overlay')
    if ov == 'X':
        svg.append('<path d="M150,300 L330,440 M330,300 L150,440" stroke="#e8281e" '
                   'stroke-width="34" stroke-linecap="round"/>')
    elif ov == 'O':
        svg.append('<circle cx="150" cy="90" r="58" fill="none" stroke="#9bc36a" stroke-width="18"/>')
    elif ov == '?':
        svg.append('<text x="120" y="95" class="qm">?</text>')
    svg.append('</svg>')
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
            'body{margin:0}'
            f'.canvas{{position:relative;width:{W}px;height:{H}px;background:#fff;'
            "font-family:'Apple SD Gothic Neo','Malgun Gothic',sans-serif}"
            '.box{position:absolute;display:flex;align-items:center;justify-content:center;'
            'text-align:center;font-size:15px;line-height:1.35;border-radius:3px;color:#222}'
            '.owner{background:#e7f1dd;border:2px solid #8cb96a}'
            '.client{background:#f7dcdc;border:2px solid #d98c8c}'
            '.server{background:#dce7f8;border:2px solid #8ca8d9}'
            '.lbl{position:absolute;background:#fff;border:1.5px solid #555;'
            'padding:9px 12px;font-size:13.5px;line-height:1.5;text-align:center;'
            'box-sizing:border-box;border-radius:2px}'
            '.code{color:#d23; background:#fbeeee; font-family:Menlo,monospace; font-size:12.5px}'
            'line{stroke:#3a3f4a;stroke-width:2}'
            '.numc{fill:#efe7f7;stroke:#9b7fc4;stroke-width:1.5}'
            '.numt{fill:#5b4a86;font-size:15px;font-weight:700;text-anchor:middle}'
            '.qm{fill:#e8281e;font-size:70px;font-weight:800}'
            '.bc{position:absolute;border-radius:50%;background:#fff;border:1.6px solid #555;'
            'display:flex;align-items:center;justify-content:center;text-align:center;'
            'font-size:12.5px;line-height:1.4;box-sizing:border-box}'
            '.badge{position:absolute;width:30px;height:30px;border-radius:50%;'
            'background:#efe7f7;border:1.5px solid #9b7fc4;color:#5b4a86;font-weight:700;'
            'display:flex;align-items:center;justify-content:center;font-size:14px}'
            '</style></head><body><div class="canvas">'
            + ''.join(svg) + ''.join(divs) + '</div></body></html>')

def code(s):
    return f'<span class="code">{html.escape(s)}</span>'

P = PORT
# ---- 다이어그램 정의 (img01~img21) ----
specs = {}
specs[1] = {}  # 박스만

specs[2] = {'overlay': 'X',
    'arrows': [{'p1': P['O']['right'], 'p2': P['C']['left']},
               {'p1': P['C']['bottom'], 'p2': P['S']['top']}],
    'labels': [{'x': 250, 'y': 120, 'lines': ['소셜 로그인 할래요', code('user_email=dingco@gmail.com'), code('password=jisdofjdio')]},
               {'x': 470, 'y': 250, 'lines': ['소셜 로그인 할래요', code('user_email=dingco@gmail.com'), code('password=jisdofjdio')], 'w': 250}]}

specs[3] = {'overlay': 'X',
    'arrows': [{'p1': P['O']['right'], 'p2': P['C']['left']}],
    'labels': [{'x': 260, 'y': 120, 'lines': ['제 소셜 로그인 정보예요', code('user_email=dingco@gmail.com'), code('facebook_id=239239238923')]}]}

specs[4] = {'overlay': 'O',
    'arrows': [{'p1': P['O']['bottom'], 'p2': P['S']['left']},
               {'p1': P['C']['bottom'], 'p2': P['S']['top']}],
    'labels': [{'x': 250, 'y': 330, 'lines': ['소셜 로그인 할래요', code('user_email=dingco@gmail.com'), code('password=jisdofjdio')]},
               {'x': 470, 'y': 240, 'lines': ['방금 로그인 한 유저 정보 주세요'], 'w': 240}]}

specs[5] = {'overlay': '?',
    'arrows': [{'p1': P['O']['bottom'], 'p2': P['S']['left']},
               {'p1': P['C']['bottom'], 'p2': P['S']['top']}],
    'labels': [{'x': 250, 'y': 330, 'lines': ['소셜 로그인 할래요', code('user_email=dingco@gmail.com'), code('password=jisdofjdio')]},
               {'x': 470, 'y': 240, 'lines': ['방금 로그인 한 유저 정보 주세요'], 'w': 240}]}

specs[6] = {
    'arrows': [
        {'p1': P['O']['bottom'], 'p2': P['S']['left']},     # 1
        {'p1': P['S']['left'], 'p2': P['O']['right']},      # 2
        {'p1': P['O']['right'], 'p2': P['C']['left']},      # 3
        {'p1': P['C']['bottom'], 'p2': P['S']['top']},      # 4 (far-right vertical)
        {'p1': (486, 410), 'p2': (486, 90)},                # 5 (left vertical)
    ],
    'bcircles': [
        {'x': 300, 'y': 140, 'r': 46, 'num': 3, 'badge': (256, 96), 'lines': [code('authorization'), code('code')]},
        {'x': 300, 'y': 322, 'r': 46, 'num': 2, 'badge': (256, 358), 'lines': [code('authorization'), code('code')]},
        {'x': 430, 'y': 300, 'r': 44, 'num': 5, 'badge': (392, 256), 'lines': [code('access_token')]},
    ],
    'labels': [
        {'x': 144, 'y': 410, 'w': 240, 'num': 1, 'badge': (150, 378), 'lines': ['소셜 로그인 할래요', code('user_email=dingco@gmail.com'), code('password=jisdofjdio')]},
        {'x': 561, 'y': 188, 'w': 175, 'num': 4, 'badge': (600, 150), 'lines': [code('authorization_code'), code('client_secret')]},
    ]}

specs[7] = {'arrows': [{'p1': P['C']['bottom'], 'p2': P['S']['top']}],
    'labels': [{'x': 470, 'y': 210, 'lines': ['name: 딩코딩코웹', code('callback_url : dingco.com/oauth/callback'), '입니다!'], 'w': 280}]}

specs[8] = {'arrows': [{'p1': P['S']['top'], 'p2': P['C']['bottom']}],
    'labels': [{'x': 460, 'y': 230, 'lines': ['알겠습니다 당신의 정보입니다.', code('client_id : 1395321700867573'), code('client_secret: d34b9cbb4da8839d0787c11b9de')], 'w': 300}]}

specs[9] = {'arrows': [{'p1': P['O']['right'], 'p2': P['C']['left']}],
    'labels': [{'x': 280, 'y': 150, 'lines': ['홈페이지 구경하는 중..'], 'w': 230}]}

specs[10] = {'arrows': [{'p1': P['O']['right'], 'p2': P['C']['left']}],
    'labels': [{'x': 280, 'y': 150, 'lines': ['페이스북 로그인으로 나의 서비스 로그인할래요'], 'w': 300}]}

specs[11] = {'arrows': [{'p1': P['C']['left'], 'p2': P['O']['right']}],
    'labels': [{'x': 280, 'y': 150, 'lines': ['아 그럴래? 그러면 페이스북가서 로그인 하고 와.', '우리 ' + code('client_id') + ' 는 1395321700867573 이고,', code('callback_url') + ' 은', 'dingco.com/social/facebook/callback 이야.'], 'w': 320}]}

specs[12] = {'arrows': [{'p1': P['O']['bottom'], 'p2': P['S']['left']}],
    'labels': [{'x': 250, 'y': 300, 'lines': [code('client_id') + ' 는 1395321700867573 이고,', code('callback_url') + ' 은', 'dingco.com/social/facebook/callback 인', '서비스에 로그인할래요.'], 'w': 320}]}

specs[13] = {'arrows': [{'p1': P['S']['left'], 'p2': P['O']['right']}],
    'labels': [{'x': 250, 'y': 300, 'lines': ['그런 Client 가 존재하네요.', '알겠습니다. 로그인하세요!'], 'w': 280}]}

specs[14] = {'arrows': [{'p1': P['O']['bottom'], 'p2': P['S']['left']}],
    'labels': [{'x': 250, 'y': 300, 'lines': ['ID: dingco@gmail.com', 'PW: skdfjosdjfsd', '입니다!'], 'w': 250}]}

specs[15] = {'arrows': [{'p1': P['S']['left'], 'p2': P['O']['right']}],
    'labels': [{'x': 250, 'y': 300, 'lines': ['로그인 성공했습니다.', code('dingco.com/social/facebook/callback?'), code('code=843jdsoe'), '로 가세요!'], 'w': 320}]}

specs[16] = {'arrows': [{'p1': P['O']['right'], 'p2': P['C']['left']}],
    'labels': [{'x': 280, 'y': 150, 'lines': ['로그인 하고 왔어요.', code('code=843jdsoe'), '라고 하네요'], 'w': 250}]}

specs[17] = {'arrows': [{'p1': P['C']['bottom'], 'p2': P['S']['top']}],
    'labels': [{'x': 470, 'y': 210, 'lines': ['Resource Owner 가 로그인 했대요!', code('code=843jdsoe'), '그리고 저 Client 맞습니다.', code('client_secret=d34b4da8839d0787c11b9de843e5')], 'w': 320}]}

specs[18] = {'arrows': [{'p1': P['S']['top'], 'p2': P['C']['bottom']}],
    'labels': [{'x': 470, 'y': 220, 'lines': ['오 그렇네요!', '알겠습니다 여기 토큰입니다!', code('access_token=j34uf8sdjfksdjsdfkljds')], 'w': 300}]}

specs[19] = specs[18]

specs[20] = {'arrows': [{'p1': P['C']['bottom'], 'p2': P['S']['top']}],
    'labels': [{'x': 470, 'y': 220, 'lines': ['유저 정보 주세염 여기 토큰입니다', code('access_token=j34uf8sdjfksdjsdfkljds')], 'w': 300}]}

specs[21] = {'arrows': [{'p1': P['S']['top'], 'p2': P['C']['bottom']}],
    'labels': [{'x': 470, 'y': 230, 'lines': ['여기 있습니당', code('user_id=1'), code('user_email=dingco@gmail.com')], 'w': 280}]}

os.makedirs('out', exist_ok=True)
for n, sp in specs.items():
    open(f'out/d{n:02d}.html', 'w').write(render(sp))

# 합본 페이지 (세로로 쌓아 한 번에 캡처 후 crop)
blocks = []
for n in sorted(specs):
    inner = render(specs[n])
    body = inner.split('<body>')[1].split('</body>')[0]
    blocks.append(f'<div class="blk" data-n="{n}">{body}</div>')
style = render(specs[1]).split('<style>')[1].split('</style>')[0]
combined = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
            + style + 'body{margin:0}.blk{width:%dpx;height:%dpx;overflow:hidden}'
            '.blk .canvas{margin:0}</style></head><body>' % (W, H)
            + ''.join(blocks) + '</body></html>')
open('out/all.html', 'w').write(combined)
print('generated', len(specs), 'html + all.html. W,H=', W, H)
