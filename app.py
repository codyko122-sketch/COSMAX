import base64
from pathlib import Path

import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="SampleTrack · 패키징 샘플 트래커", page_icon="📦", layout="wide")

# ---------------------------------------------------------------
# 로컬 이미지를 base64로 인코딩해 CSS 배경으로 삽입하기 위한 헬퍼
# ---------------------------------------------------------------
ASSETS_DIR = Path(__file__).parent / "assets"

def get_base64_image(filename: str):
    path = ASSETS_DIR / filename
    if not path.exists():
        return None
    ext = path.suffix.lstrip(".").lower()
    ext = "jpeg" if ext == "jpg" else ext
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/{ext};base64,{data}"

hero_bg_data_uri = get_base64_image("cosmax_hq.jpg")
# assets 폴더에 이미지가 없을 경우를 대비한 대체 이미지
HERO_BG_URL = hero_bg_data_uri or (
    "https://www.news1.kr/_next/image?url=https%3A%2F%2Fi3n.news1.kr%2Fsystem%2Fphotos%2F2026%2F5%2F12%2F7901864%2Fhigh.jpg&w=1920&q=75"
)

# ---------------------------------------------------------------
# 스타일 (원본 HTML의 색상 / 폰트 / 카드 디자인을 최대한 재현)
# ---------------------------------------------------------------
CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com/">
<link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">

<style>
:root{
  --ink:#14181D; --ink-soft:#6B7280; --line:#E7E8EA; --paper:#F6F6F5; --card:#FFFFFF;
  --blueprint:#0E6E8C; --amber:#C8791E; --terracotta:#B14431; --sage:#427856;
}
html, body, [class*="css"]  { font-family:'Inter', sans-serif; }
.mono{ font-family:'IBM Plex Mono', monospace; }

#MainMenu, footer, header {visibility:hidden;}
.block-container{ padding-top:0 !important; max-width:1180px; }

/* ---------- hero ---------- */
.hero{
  position:relative; overflow:hidden; background:#101820;
  padding:34px 24px 30px; color:#fff; margin:0 -1rem 24px -1rem;
  border-radius: 0 0 20px 20px;
}
.hero-bg{
  position:absolute; inset:0;
  background:url('__HERO_BG_URL__') center/cover no-repeat;
  z-index:0;
}
.hero-overlay{ position:absolute; inset:0; background:rgba(10,14,18,.62); z-index:1; }
.hero-inner{ max-width:880px; margin:0 auto; position:relative; z-index:2; text-align:center; }

.brand-chip{
  display:inline-flex; align-items:center; gap:7px; background:#fff;
  border-radius:999px; padding:7px 18px; box-shadow:0 6px 18px rgba(0,0,0,.25); margin-bottom:18px;
}
.brand-text{ font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:13px; color:var(--ink); }
.brand-text b{ color:var(--terracotta); font-weight:700; }

.hero-title{
  font-family:'Space Grotesk',sans-serif; font-size:36px; font-weight:700;
  line-height:1.25; margin:0 0 12px; letter-spacing:-0.01em;
}
.hero-sub{ font-size:15px; color:rgba(255,255,255,.75); max-width:520px; margin:0 auto 20px; line-height:1.6; text-align:center; }

.hero-tags{ display:flex; justify-content:center; gap:10px; flex-wrap:wrap; font-size:12.5px; margin-top:6px; }
.tag-label{ color:rgba(255,255,255,.55); margin-right:2px; }
.tag-pill{ border:1px solid rgba(255,255,255,.25); color:rgba(255,255,255,.9); padding:6px 14px; border-radius:999px; }
.tag-pill b{ font-family:'IBM Plex Mono',monospace; font-weight:600; }

/* ---------- toolbar ---------- */
.content-toolbar{ display:flex; justify-content:space-between; align-items:baseline; margin:4px 0 18px; }
.toolbar-label{ font-size:16px; font-weight:700; }
.toolbar-count{ font-size:13px; color:var(--ink-soft); }

/* ---------- card ---------- */
.card-item{
  background:var(--card); border-radius:16px; overflow:hidden;
  box-shadow:0 1px 2px rgba(20,24,29,.06); border:1px solid var(--line);
  margin-bottom:20px;
}
.card-cover{ position:relative; height:100px; display:flex; align-items:center; justify-content:center; }
.cover-요청{ background:linear-gradient(135deg,#6B7280,#14181D); }
.cover-제작중{ background:linear-gradient(135deg,#C8791E,#B14431); }
.cover-배송중{ background:linear-gradient(135deg,#1794B8,#123244); }
.cover-검수완료{ background:linear-gradient(135deg,#5A9973,#1C3A29); }
.cover-type{ font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:700; color:rgba(255,255,255,.92); }
.badge-float{ position:absolute; top:12px; right:12px; }
.badge{ display:inline-block; font-size:11.5px; font-weight:600; padding:4px 10px; border-radius:999px; background:rgba(255,255,255,.92); }
.badge.stage-요청{ color:var(--ink-soft); }
.badge.stage-제작중{ color:var(--amber); }
.badge.stage-배송중{ color:var(--blueprint); }
.badge.stage-검수완료{ color:var(--sage); }

.card-body{ padding:14px 16px 16px; }
.card-name{ font-weight:700; font-size:14.5px; margin-bottom:6px; line-height:1.35; }
.card-meta{ font-size:12.5px; color:var(--ink-soft); margin-bottom:12px; }
.card-meta .qty{ font-family:'IBM Plex Mono',monospace; }
.card-foot{ display:flex; justify-content:space-between; align-items:center; border-top:1px solid #EEF0EE; padding-top:10px; }
.foot-label{ font-size:11px; color:var(--ink-soft); }
.dday{ font-family:'IBM Plex Mono',monospace; font-size:13px; font-weight:600; }
.dday.urgent{ color:var(--terracotta); }
.dday.normal{ color:var(--ink-soft); }
.dday.done{ color:var(--sage); }

.empty-state{
  text-align:center; padding:70px 20px; color:var(--ink-soft); font-size:14px;
  background:var(--card); border:1px dashed var(--line); border-radius:16px;
}

/* 필터 버튼 & CTA 버튼을 원본 느낌으로 */
div[data-testid="stButton"] > button{
  border-radius:999px !important; font-weight:600 !important; font-size:13px !important;
}
</style>
"""

st.markdown(CSS.replace("__HERO_BG_URL__", HERO_BG_URL), unsafe_allow_html=True)

# ---------------------------------------------------------------
# 초기 데이터
# ---------------------------------------------------------------
def add_days(n):
    return date.today() + timedelta(days=n)

if "samples" not in st.session_state:
    st.session_state.samples = [
        {"name": "톤업선크림 리필 용기", "vendor": "대한패키징", "type": "용기", "qty": 500,  "stage": "제작중",   "due": add_days(5)},
        {"name": "립밤 스틱 케이스",     "vendor": "우리산업",   "type": "캡",   "qty": 1000, "stage": "배송중",   "due": add_days(2)},
        {"name": "쿠션 콤팩트 상자",     "vendor": "한빛테크",   "type": "박스", "qty": 300,  "stage": "요청",     "due": add_days(10)},
        {"name": "앰플 유리병 40ml",     "vendor": "삼진글라스", "type": "용기", "qty": 800,  "stage": "검수완료", "due": add_days(-1)},
        {"name": "크림자 이너캡 뚜껑",   "vendor": "대한패키징", "type": "캡",   "qty": 1200, "stage": "제작중",   "due": add_days(-2)},
        {"name": "PE 완충 박스",         "vendor": "한빛테크",   "type": "박스", "qty": 600,  "stage": "요청",     "due": add_days(14)},
        {"name": "프라이머 튜브 용기",   "vendor": "성진화학",   "type": "용기", "qty": 400,  "stage": "배송중",   "due": add_days(1)},
    ]

if "current_filter" not in st.session_state:
    st.session_state.current_filter = "전체"

STAGES = ["요청", "제작중", "배송중", "검수완료"]

def stage_count(stage):
    return sum(1 for s in st.session_state.samples if s["stage"] == stage)

def dday_info(sample):
    if sample["stage"] == "검수완료":
        return "완료", "done"
    diff = (sample["due"] - date.today()).days
    if diff < 0:
        return f"D+{-diff} 지연", "urgent"
    if diff == 0:
        return "D-DAY", "urgent"
    if diff <= 2:
        return f"D-{diff}", "urgent"
    return f"D-{diff}", "normal"

# ---------------------------------------------------------------
# 새 샘플 요청 모달
# ---------------------------------------------------------------
@st.dialog("새 샘플 요청")
def open_request_modal():
    st.caption("등록하면 목록 맨 위에 '요청' 상태로 추가됩니다.")
    with st.form("sample_form", border=False):
        name = st.text_input("샘플명", placeholder="예: 톤업선크림 리필 용기")
        vendor = st.text_input("벤더명", placeholder="예: 대한패키징")
        c1, c2 = st.columns(2)
        with c1:
            type_ = st.selectbox("포장재 종류", ["용기", "캡", "박스", "라벨", "기타"])
        with c2:
            qty = st.number_input("수량", min_value=1, value=100, step=10)
        due = st.date_input("희망완료일", value=add_days(7))

        col_a, col_b = st.columns(2)
        with col_a:
            cancel = st.form_submit_button("취소", use_container_width=True)
        with col_b:
            submitted = st.form_submit_button("요청 등록", type="primary", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            if not name.strip() or not vendor.strip():
                st.error("샘플명과 벤더명을 입력해주세요.")
            else:
                st.session_state.samples.insert(0, {
                    "name": name.strip(), "vendor": vendor.strip(),
                    "type": type_, "qty": int(qty), "stage": "요청", "due": due,
                })
                st.session_state.current_filter = "전체"
                st.rerun()

# ---------------------------------------------------------------
# 헤더 (히어로 섹션)
# ---------------------------------------------------------------
st.markdown(f"""
<div class="hero">
  <span class="hero-bg"></span><span class="hero-overlay"></span>
  <div class="hero-inner">
    <div class="brand-chip"><span class="brand-text">COSMAX <b>TOOL</b></span></div>
    <h1 class="hero-title">패키징 샘플, 지금 어디 있는지<br>한눈에 확인하세요</h1>
    <p class="hero-sub">벤더에게 요청한 포장재 샘플이 지금 어느 단계인지, 더 이상 물어보지 않아도 됩니다.</p>
    <div class="hero-tags">
      <span class="tag-label">진행 현황</span>
      <span class="tag-pill">요청 <b>{stage_count('요청')}</b></span>
      <span class="tag-pill">제작중 <b>{stage_count('제작중')}</b></span>
      <span class="tag-pill">배송중 <b>{stage_count('배송중')}</b></span>
      <span class="tag-pill">검수완료 <b>{stage_count('검수완료')}</b></span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# CTA + 필터 버튼 (실제 Streamlit 위젯)
cta_col = st.columns([1, 2, 1])[1]
with cta_col:
    if st.button("➕  새 샘플 요청 등록하기", use_container_width=True, type="primary"):
        open_request_modal()

filter_options = ["전체"] + STAGES
cols = st.columns(len(filter_options))
for col, opt in zip(cols, filter_options):
    with col:
        is_active = st.session_state.current_filter == opt
        if st.button(opt, key=f"filter_{opt}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.current_filter = opt
            st.rerun()

st.write("")

# ---------------------------------------------------------------
# 목록 (필터 적용)
# ---------------------------------------------------------------
current_filter = st.session_state.current_filter
samples = st.session_state.samples
filtered = samples if current_filter == "전체" else [s for s in samples if s["stage"] == current_filter]

label = "전체 샘플" if current_filter == "전체" else f"{current_filter} 샘플"
st.markdown(f"""
<div class="content-toolbar">
  <span class="toolbar-label">{label}</span>
  <span class="toolbar-count">{len(filtered)}건</span>
</div>
""", unsafe_allow_html=True)

if not filtered:
    st.markdown(f"<div class='empty-state'>'{current_filter}' 단계의 샘플이 없습니다.</div>", unsafe_allow_html=True)
else:
    n_cols = 4
    rows = [filtered[i:i + n_cols] for i in range(0, len(filtered), n_cols)]
    for row in rows:
        cols = st.columns(n_cols)
        for col, s in zip(cols, row):
            dd_text, dd_cls = dday_info(s)
            with col:
                st.markdown(f"""
                <div class="card-item">
                  <div class="card-cover cover-{s['stage']}">
                    <span class="cover-type">{s['type']}</span>
                    <span class="badge-float badge stage-{s['stage']}">{s['stage']}</span>
                  </div>
                  <div class="card-body">
                    <div class="card-name">{s['name']}</div>
                    <div class="card-meta">{s['vendor']} · <span class="qty">{s['qty']:,}개</span></div>
                    <div class="card-foot">
                      <span class="foot-label">희망완료일</span>
                      <span class="dday {dd_cls}">{dd_text}</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
