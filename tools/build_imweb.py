# index.html(완성본)에서 아임웹용 파일을 만듭니다.
#   assets/miso.js  : 프로그램 (아임웹 페이지 안의 독립 공간(Shadow DOM)에 사이트를 그림)
#   assets/miso.css : 스타일 (독립 공간 안에만 적용돼 아임웹 디자인과 충돌하지 않음)
# 사용법: python3 tools/build_imweb.py   (miso-site 폴더에서 실행)
import re, pathlib, hashlib

BASE = 'https://da6uoar.github.io/miso-site/'
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'index.html').read_text(encoding='utf-8')

js_s = s.find('<script type="module" crossorigin>') + len('<script type="module" crossorigin>')
st = s.find('<style rel="stylesheet" crossorigin>')
js_e = s.rfind('</script>', js_s, st)
js = s[js_s:js_e]
css = s[st + len('<style rel="stylesheet" crossorigin>'):s.find('</style>', st)]

def absolutize(t):
    return re.sub(r'(["`(])(images|video)/', lambda m: m.group(1) + BASE + m.group(2) + '/', t)

def rep(t, a, b, n=1):
    c = t.count(a)
    assert c == n, (a[:60], c)
    return t.replace(a, b)

# ---- JS ----
js = absolutize(js)
js = rep(js, 'wh.createRoot(document.getElementById("root"))', 'wh.createRoot(__misoMount())')
js = rep(js, 'const c=u==="top"?0:document.getElementById(u);', 'const c=u==="top"?0:__misoRoot.getElementById(u);')
js = rep(js, 'const T=document.getElementById("quote");', 'const T=__misoRoot.getElementById("quote");')
js = rep(js, 'smoothScroll:l=!0', 'smoothScroll:l=!1')

prelude = (
    'var __misoRoot=null;'
    'function __misoMount(){'
    'var host=document.getElementById("miso-root");'
    'if(!host){host=document.createElement("div");host.id="miso-root";(document.currentScript&&document.currentScript.parentNode||document.body).appendChild(host);}'
    'host.style.display="block";'
    'var sr=host.shadowRoot||host.attachShadow({mode:"open"});'
    '__misoRoot=sr;'
    'if(!document.getElementById("miso-font")){var f=document.createElement("link");f.id="miso-font";f.rel="stylesheet";'
    'f.href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css";document.head.appendChild(f);}'
    'var l=document.createElement("link");l.rel="stylesheet";l.href="' + BASE + 'assets/miso.css?v=__CSSV__";sr.appendChild(l);'
    'var m=document.createElement("div");m.className="miso-app";sr.appendChild(m);'
    'return m;}'
)
out_js = '(function(){"use strict";' + prelude + js + '\n})();\n'

# ---- CSS ----
css = absolutize(css)
css = re.sub(r'@import\s*"[^"]*";', '', css)          # 글꼴은 문서 쪽에서 불러옴 (Shadow DOM 안 @font-face 무시됨)
css = css.replace(':root{', ':host{')
css = css.replace('html{', ':host{')
css = re.sub(r'(?<![\w-])body\{', ':host{', css)
css = ':host{display:block;all:initial;display:block}' + css

(root / 'assets').mkdir(exist_ok=True)
out_js = out_js.replace('__CSSV__', hashlib.md5(css.encode('utf-8')).hexdigest()[:8])
(root / 'assets' / 'miso.js').write_text(out_js, encoding='utf-8')
(root / 'assets' / 'miso.css').write_text(css, encoding='utf-8')
print('miso.js', len(out_js), 'miso.css', len(css))
