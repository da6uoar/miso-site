# 미소건설기계 홈페이지

- `index.html` — 홈페이지 (미소건설기계_수정본 8 기준)
- `images/`, `video/` — 사진·영상

GitHub Pages로 공개하면 `https://(아이디).github.io/miso-site/` 에서 열립니다.

## 아임웹에 넣기 (프로 요금제 이상)
아임웹 코드 위젯에 아래 두 줄만 넣으면 됩니다. (주석 없이)

```html
<div id="miso-root"></div>
<script src="https://da6uoar.github.io/miso-site/assets/miso.js"></script>
```

- `assets/miso.js`, `assets/miso.css` 는 `index.html` 에서 만듭니다: `python3 tools/build_imweb.py`
- 사이트는 아임웹 페이지 안의 독립 공간(Shadow DOM)에 그려져 아임웹 디자인과 서로 섞이지 않습니다.
- `imweb-test.html` 은 아임웹과 비슷한 환경에서 확인하는 테스트 페이지입니다.
