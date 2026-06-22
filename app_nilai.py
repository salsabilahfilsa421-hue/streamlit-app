import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#  KONSTANTA

BATAS_LULUS = 65
BOBOT       = [0.3, 0.3, 0.4]

WARNA_LULUS = [
    "#BBD7F6","#FFDD57","#2ED573","#A29BFE",
    "#1E90FF","#B8E994","#FF7F50","#00CEC9",
]
WARNA_TIDAK = "#FF4040"

DATA_AWAL = [
    ("Andi",    80, 75, 85),
    ("Budi",    50, 55, 58),
    ("Citra",   90, 85, 88),
    ("Dinda",   45, 50, 55),
    ("Eko",     78, 82, 79),
    ("Farida",  85, 88, 92),
    ("Gilang",  55, 58, 60),
    ("Hana",    48, 52, 56),
    ("Irfan",   88, 90, 91),
    ("Jasmine", 65, 74, 70),
]

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sistem Penilaian Akademik",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS RESPONSIVE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d1a !important;
    color: #e2e8f0;
    font-family: 'Space Grotesk', sans-serif;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 100% !important;
}
.main > div { padding: 0 !important; }
section[data-testid="stSidebar"] { background: #13132b; }

/* ── hero ── */
.hero {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a1040 55%, #0d1a2e 100%);
    border-bottom: 1px solid #2a2a4a;
    padding: clamp(1.8rem, 5vw, 3.5rem) clamp(1rem, 4vw, 2.5rem) clamp(1.5rem, 4vw, 2.5rem);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(162,155,254,.13), transparent);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(.6rem, 1.5vw, .72rem);
    letter-spacing: .18em; color: #A29BFE;
    text-transform: uppercase; margin-bottom: .5rem;
    animation: fadeDown .6s ease both;
}
.hero-title {
    font-size: clamp(1.5rem, 5vw, 3.2rem);
    font-weight: 700; line-height: 1.1;
    background: linear-gradient(90deg, #fff 30%, #A29BFE 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .65rem;
    animation: fadeDown .7s .1s ease both;
    min-height: 1.2em;
}
.hero-sub {
    font-size: clamp(.8rem, 2vw, .95rem); color: #8b93a8;
    max-width: 560px; margin: 0 auto;
    animation: fadeDown .8s .2s ease both;
}
.hero-formula {
    display: inline-block; margin-top: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(.8rem, 2vw, 1.05rem); font-weight: 600; color: #2ED573;
    background: rgba(46,213,115,.1);
    border: 1px solid rgba(46,213,115,.3);
    border-radius: 8px; padding: .35rem 1rem;
    animation: fadeDown .9s .3s ease both;
}

/* ── animations ── */
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-16px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes slideIn {
    from { opacity:0; transform:translateX(-18px); }
    to   { opacity:1; transform:translateX(0); }
}

/* ── inner wrapper ── */
.inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 clamp(.8rem, 3vw, 1.5rem);
}

/* ── metric cards ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: .75rem;
    padding: 1.4rem 0 .6rem;
    animation: fadeUp .6s .1s ease both;
}
.metric-card {
    background: #13132b;
    border: 1px solid #2a2a4a;
    border-radius: 14px;
    padding: 1rem 1rem;
    text-align: center;
    transition: border-color .2s, transform .2s;
}
.metric-card:hover { border-color: #A29BFE; transform: translateY(-2px); }
.metric-num {
    font-size: clamp(1.4rem, 3.5vw, 2rem);
    font-weight: 700; font-family: 'JetBrains Mono', monospace;
}
.metric-label { font-size: .72rem; color: #6c7086; margin-top: .15rem; letter-spacing: .04em; }

/* ── section headings ── */
.section-head {
    font-size: .68rem; font-weight: 600; letter-spacing: .15em;
    text-transform: uppercase; color: #A29BFE;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: .55rem; padding-bottom: .28rem;
    border-bottom: 1px solid #2a2a4a;
}

/* ── input panel ── */
.input-panel {
    background: #13132b;
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 1.2rem 1.4rem 1rem;
    margin-bottom: 1rem;
    animation: slideIn .5s ease both;
}

/* ── streamlit overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #0d0d1a !important;
    border: 1px solid #2a2a4a !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: clamp(.8rem, 2vw, .9rem) !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #A29BFE !important;
    box-shadow: 0 0 0 2px rgba(162,155,254,.2) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #8b93a8 !important; font-size: .8rem !important;
}

/* primary button */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #A29BFE, #7c75e8) !important;
    color: #0d0d1a !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: .9rem !important;
    width: 100% !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: opacity .2s, transform .15s !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    opacity: .88 !important; transform: translateY(-1px) !important;
}

/* secondary buttons */
[data-testid="stBaseButton-secondary"] {
    background: #1e1e38 !important;
    border: 1px solid #2a2a4a !important;
    color: #c0c8e0 !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: border-color .2s !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    border-color: #A29BFE !important; color: #A29BFE !important;
}

/* download button */
[data-testid="stDownloadButton"] button {
    background: #1e1e38 !important;
    border: 1px solid #2a2a4a !important;
    color: #A29BFE !important;
    border-radius: 8px !important;
    font-size: .82rem !important;
}

/* ── status badge ── */
.status-badge {
    display: inline-flex; align-items: center; gap: .35rem;
    padding: .35rem .9rem; border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(.72rem, 2vw, .82rem); font-weight: 600;
    margin: .4rem 0; width: 100%;
}
.badge-lulus { background: rgba(46,213,115,.12); color: #2ED573; border: 1px solid rgba(46,213,115,.3); }
.badge-tidak { background: rgba(255,64,64,.12);  color: #FF4040; border: 1px solid rgba(255,64,64,.3); }

/* ── bobot pills ── */
.bobot-row { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: .4rem; }
.bobot-pill {
    padding: .25rem .75rem; border-radius: 100px;
    font-size: .75rem; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.pill-blue  { background: rgba(30,144,255,.15); color: #1E90FF; border: 1px solid rgba(30,144,255,.3); }
.pill-purp  { background: rgba(162,155,254,.15);color: #A29BFE; border: 1px solid rgba(162,155,254,.3);}
.pill-green { background: rgba(46,213,115,.15); color: #2ED573; border: 1px solid rgba(46,213,115,.3); }

/* ── tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #13132b; border-radius: 12px;
    padding: .25rem; gap: .15rem; flex-wrap: wrap;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px !important; color: #8b93a8 !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
    font-size: clamp(.75rem, 2vw, .88rem) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #2a2a4a !important; color: #e2e8f0 !important;
}

/* ── divider ── */
hr { border-color: #2a2a4a !important; margin: .8rem 0 !important; }

/* ── responsive: mobile stacks ── */
@media (max-width: 640px) {
    .metrics-row { grid-template-columns: repeat(2, 1fr); }
    .hero-formula { font-size: .72rem; padding: .3rem .7rem; }
}
@media (max-width: 380px) {
    .metrics-row { grid-template-columns: 1fr 1fr; }
}

/* scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d0d1a; }
::-webkit-scrollbar-thumb { background: #2a2a4a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
def init_data_awal():
    rows = []
    for nama, tugas, uts, uas in DATA_AWAL:
        nilai = tugas * BOBOT[0] + uts * BOBOT[1] + uas * BOBOT[2]
        rows.append({
            "Nama": nama, "Tugas": tugas, "UTS": uts, "UAS": uas,
            "Nilai Akhir": round(nilai, 1),
            "Status": "LULUS" if nilai >= BATAS_LULUS else "TIDAK LULUS",
            "Lulus": nilai >= BATAS_LULUS,
        })
    return rows

if "data" not in st.session_state:
    st.session_state.data = init_data_awal()
if "last_added" not in st.session_state:
    st.session_state.last_added = None

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def get_bar_color(idx, lulus):
    if not lulus:
        return WARNA_TIDAK
    lulus_idx = sum(1 for d in st.session_state.data[:idx] if d["Lulus"])
    return WARNA_LULUS[lulus_idx % len(WARNA_LULUS)]

def build_df():
    return pd.DataFrame(st.session_state.data)[
        ["Nama","Tugas","UTS","UAS","Nilai Akhir","Status"]
    ]

def get_stats():
    data  = st.session_state.data
    total = len(data)
    lulus = sum(1 for d in data if d["Lulus"])
    tidak = total - lulus
    avg   = round(np.mean([d["Nilai Akhir"] for d in data]), 1) if data else 0
    top   = max(data, key=lambda d: d["Nilai Akhir"])["Nama"] if data else "—"
    return total, lulus, tidak, avg, top

def build_colors():
    return [get_bar_color(i, st.session_state.data[i]["Lulus"])
            for i in range(len(st.session_state.data))]

# ─────────────────────────────────────────────
#  HERO — animasi ketik JS
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Sistem Penilaian Akademik Mahasiswa</div>
  <div class="hero-title" id="htitle"></div>
  <div class="hero-sub" id="hsub" style="opacity:0">
    Kalkulasi nilai akhir berbasis model matriks-vektor dengan visualisasi interaktif.
  </div>
  <div class="hero-formula" id="hform" style="opacity:0">
    b = A · x &nbsp;|&nbsp; 30% Tugas &nbsp;+&nbsp; 30% UTS &nbsp;+&nbsp; 40% UAS
  </div>
</div>
<script>
(function(){
  var t=document.getElementById('htitle'),
      s=document.getElementById('hsub'),
      f=document.getElementById('hform'),
      txt='Dashboard Nilai Mahasiswa', i=0;
  function type(){
    if(i<txt.length){ t.textContent+=txt[i++]; setTimeout(type,52); }
    else {
      s.style.transition='opacity .7s .1s'; s.style.opacity='1';
      f.style.transition='opacity .7s .45s'; f.style.opacity='1';
    }
  }
  setTimeout(type, 250);
})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  METRICS
# ─────────────────────────────────────────────
total, lulus, tidak, avg, top = get_stats()

st.markdown(f"""
<div class="inner">
<div class="metrics-row">
  <div class="metric-card">
    <div class="metric-num" style="color:#A29BFE">{total}</div>
    <div class="metric-label">Total Mahasiswa</div>
  </div>
  <div class="metric-card">
    <div class="metric-num" style="color:#2ED573">{lulus}</div>
    <div class="metric-label">Lulus</div>
  </div>
  <div class="metric-card">
    <div class="metric-num" style="color:#FF4040">{tidak}</div>
    <div class="metric-label">Tidak Lulus</div>
  </div>
  <div class="metric-card">
    <div class="metric-num" style="color:#FFDD57">{avg}</div>
    <div class="metric-label">Rata-rata Nilai</div>
  </div>
  <div class="metric-card">
    <div class="metric-num" style="font-size:clamp(1rem,3vw,1.3rem);color:#1E90FF">{top}</div>
    <div class="metric-label">Nilai Tertinggi</div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="inner">', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LAYOUT — responsive 1 kolom di mobile
# ─────────────────────────────────────────────
col_form, col_table = st.columns([1, 2.1], gap="large")

# ── FORM ─────────────────────────────────────
with col_form:
    st.markdown('<div class="section-head">✏️ Input Mahasiswa</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)

    with st.form("form_tambah", clear_on_submit=True):
        nama  = st.text_input("Nama Mahasiswa", placeholder="contoh: Budi Santoso")
        c1, c2 = st.columns(2)
        with c1:
            tugas = st.number_input("Tugas (0–100)", min_value=0.0, max_value=100.0, step=0.5, value=0.0)
            uts   = st.number_input("UTS (0–100)",   min_value=0.0, max_value=100.0, step=0.5, value=0.0)
        with c2:
            uas   = st.number_input("UAS (0–100)",   min_value=0.0, max_value=100.0, step=0.5, value=0.0)
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("➕ Tambah Data", use_container_width=True)

        if submitted:
            if not nama.strip():
                st.error("Nama tidak boleh kosong.")
            else:
                nilai      = tugas * BOBOT[0] + uts * BOBOT[1] + uas * BOBOT[2]
                lulus_flag = nilai >= BATAS_LULUS
                st.session_state.data.append({
                    "Nama": nama.strip(), "Tugas": tugas,
                    "UTS": uts, "UAS": uas,
                    "Nilai Akhir": round(nilai, 1),
                    "Status": "LULUS" if lulus_flag else "TIDAK LULUS",
                    "Lulus": lulus_flag,
                })
                st.session_state.last_added = {
                    "nama": nama.strip(), "nilai": round(nilai, 1), "lulus": lulus_flag
                }
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Badge notifikasi
    if st.session_state.last_added:
        la  = st.session_state.last_added
        cls = "badge-lulus" if la["lulus"] else "badge-tidak"
        ico = "✅" if la["lulus"] else "❌"
        txt = "LULUS" if la["lulus"] else "TIDAK LULUS"
        st.markdown(f"""
        <div class="status-badge {cls}">
            {ico}&nbsp;<b>{la['nama']}</b>&nbsp;—&nbsp;Nilai:&nbsp;<b>{la['nilai']}</b>&nbsp;[{txt}]
        </div>""", unsafe_allow_html=True)

    # Bobot
    st.markdown("""
    <div class="section-head" style="margin-top:1.1rem">⚖️ Bobot Penilaian</div>
    <div class="bobot-row">
        <span class="bobot-pill pill-blue">Tugas 30%</span>
        <span class="bobot-pill pill-purp">UTS 30%</span>
        <span class="bobot-pill pill-green">UAS 40%</span>
    </div>
    <p style="color:#6c7086;font-size:.75rem;margin-top:.6rem;line-height:1.6">
        Batas Lulus: <b style="color:#FFDD57">65</b><br>
        Formula: <span style="font-family:'JetBrains Mono',monospace;color:#2ED573">b = A · x</span><br>
        nilai = 0.3T + 0.3U₁ + 0.4U₂
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-head">🗑️ Kelola Data</div>', unsafe_allow_html=True)

    cd1, cd2 = st.columns(2)
    with cd1:
        if st.button("↩ Reset Data Awal", use_container_width=True):
            st.session_state.data = init_data_awal()
            st.session_state.last_added = None
            st.rerun()
    with cd2:
        if st.button("🗑 Hapus Semua", use_container_width=True):
            st.session_state.data = []
            st.session_state.last_added = None
            st.rerun()

# ── TABEL ────────────────────────────────────
with col_table:
    st.markdown('<div class="section-head">📋 Rekap Nilai Mahasiswa</div>', unsafe_allow_html=True)

    df = build_df()

    if df.empty:
        st.info("Belum ada data mahasiswa.")
    else:
        # Pandas baru pakai .map(), bukan .applymap()
        def color_status(val):
            return "color: #2ED573; font-weight:700" if val == "LULUS" \
                   else "color: #FF4040; font-weight:700"

        def color_nilai(val):
            return "color: #FFDD57; font-weight:600" if val >= BATAS_LULUS \
                   else "color: #FF6b6b"

        try:
            styled = (
                df.style
                .map(color_status, subset=["Status"])
                .map(color_nilai,  subset=["Nilai Akhir"])
                .set_properties(**{
                    "background-color": "#13132b",
                    "color": "#c0c8e0",
                    "border": "1px solid #2a2a4a",
                    "font-family": "JetBrains Mono, monospace",
                    "font-size": "13px",
                })
                .set_table_styles([
                    {"selector": "thead th", "props": [
                        ("background-color","#1e1e38"),
                        ("color","#A29BFE"),
                        ("font-weight","600"),
                        ("text-transform","uppercase"),
                        ("letter-spacing",".07em"),
                        ("font-size","11px"),
                        ("padding","10px 12px"),
                    ]},
                    {"selector": "tbody td", "props": [("padding","8px 12px")]},
                ])
                .format({"Nilai Akhir": "{:.1f}"})
                .hide(axis="index")
            )
            st.dataframe(styled, use_container_width=True, height=400)
        except Exception:
            # Fallback jika styled gagal
            st.dataframe(df, use_container_width=True, hide_index=True, height=400)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Export CSV", data=csv,
            file_name="nilai_mahasiswa.csv", mime="text/csv"
        )

# ─────────────────────────────────────────────
#  GRAFIK TABS
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="section-head" style="margin-bottom:.8rem">📊 Visualisasi Data</div>',
            unsafe_allow_html=True)

data = st.session_state.data

tab2d, tab3d, tab_radar, tab_dist = st.tabs([
    "📈 Bar 2D", "🧊 Bar 3D", "🕸️ Radar Komponen", "📉 Distribusi"
])

# ── 2D ──────────────────────────────────────
with tab2d:
    if not data:
        st.info("Tambahkan data terlebih dahulu.")
    else:
        nama_list  = [d["Nama"]        for d in data]
        nilai_list = [d["Nilai Akhir"] for d in data]
        colors     = build_colors()

        fig = go.Figure(go.Bar(
            x=nama_list, y=nilai_list,
            marker=dict(color=colors, line=dict(color="rgba(255,255,255,.2)", width=1)),
            text=[f"<b>{v:.1f}</b>" for v in nilai_list],
            textposition="outside",
            textfont=dict(color="white", size=11, family="JetBrains Mono"),
            hovertemplate="<b>%{x}</b><br>Nilai: %{y:.1f}<extra></extra>",
        ))
        fig.add_hline(y=BATAS_LULUS,
                      line=dict(color="#FFDD57", dash="dash", width=2),
                      annotation_text=f"  Batas Lulus = {BATAS_LULUS}",
                      annotation_font=dict(color="#FFDD57", size=11))
        fig.update_layout(
            title=dict(text="Nilai Akhir Mahasiswa  <span style='font-family:monospace;color:#2ED573'>b = A·x</span>",
                       font=dict(size=14, color="white"), x=0),
            paper_bgcolor="#13132b", plot_bgcolor="#0d0d1a",
            font=dict(color="#c0c8e0", family="Space Grotesk"),
            yaxis=dict(range=[0,115], gridcolor="#1e1e38", title="Nilai Akhir"),
            xaxis=dict(tickangle=-20, gridcolor="#1e1e38"),
            margin=dict(t=52, b=20, l=10, r=10), height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

# ── 3D ──────────────────────────────────────
with tab3d:
    if not data:
        st.info("Tambahkan data terlebih dahulu.")
    else:
        nama_list  = [d["Nama"]        for d in data]
        nilai_list = [d["Nilai Akhir"] for d in data]
        n      = len(data)
        colors = build_colors()
        b      = np.array(nilai_list)

        BAR_W  = 0.5   # lebar bar di sumbu X
        BAR_D  = 0.4   # kedalaman bar di sumbu Y
        GAP    = 1.0   # jarak antar bar

        def make_box(x0, y0, z0, x1, y1, z1, color, name, val):
            """
            Buat 1 kotak 3D (cuboid) dengan 6 sisi (12 segitiga).
            Vertex:
              0:(x0,y0,z0)  1:(x1,y0,z0)  2:(x1,y1,z0)  3:(x0,y1,z0)
              4:(x0,y0,z1)  5:(x1,y0,z1)  6:(x1,y1,z1)  7:(x0,y1,z1)
            """
            vx = [x0,x1,x1,x0, x0,x1,x1,x0]
            vy = [y0,y0,y1,y1, y0,y0,y1,y1]
            vz = [z0,z0,z0,z0, z1,z1,z1,z1]
            # 12 segitiga (6 sisi × 2)
            ii = [0,0, 1,1, 2,2, 3,3, 0,0, 4,4]
            jj = [1,2, 2,5, 3,6, 0,7, 4,5, 5,6]
            kk = [2,3, 5,6, 6,7, 7,4, 5,1, 6,7]
            return go.Mesh3d(
                x=vx, y=vy, z=vz,
                i=ii, j=jj, k=kk,
                color=color,
                opacity=0.90,
                flatshading=True,
                showscale=False,
                name=name,
                hovertemplate=f"<b>{name}</b><br>Nilai Akhir: {val:.1f}<extra></extra>",
            )

        fig3 = go.Figure()

        for i in range(n):
            xc  = i * GAP          # pusat X bar ke-i
            x0  = xc - BAR_W / 2
            x1  = xc + BAR_W / 2
            y0, y1 = 0.0, BAR_D
            z0, z1 = 0.0, float(b[i])

            fig3.add_trace(make_box(x0, y0, z0, x1, y1, z1,
                                    colors[i], nama_list[i], b[i]))

            # Label nilai di atas bar
            fig3.add_trace(go.Scatter3d(
                x=[xc], y=[BAR_D / 2], z=[z1 + 2.5],
                mode="text",
                text=[f"<b>{b[i]:.1f}</b>"],
                textfont=dict(color="white", size=9, family="JetBrains Mono"),
                showlegend=False, hoverinfo="skip",
            ))

        # Bidang batas lulus (transparan kuning)
        bx = [-(GAP/2), (n-1)*GAP + GAP/2, (n-1)*GAP + GAP/2, -(GAP/2)]
        by = [0, 0, BAR_D, BAR_D]
        bz_plane = [BATAS_LULUS] * 4
        fig3.add_trace(go.Mesh3d(
            x=bx, y=by, z=bz_plane,
            i=[0], j=[1], k=[2],
            color="#FFDD57", opacity=0.12,
            hoverinfo="skip", showlegend=False,
        ))
        fig3.add_trace(go.Mesh3d(
            x=bx, y=by, z=bz_plane,
            i=[0], j=[2], k=[3],
            color="#FFDD57", opacity=0.12,
            hoverinfo="skip", showlegend=False,
        ))

        # Garis batas lulus
        fig3.add_trace(go.Scatter3d(
            x=[-(GAP/2), (n-1)*GAP + GAP/2],
            y=[0, 0],
            z=[BATAS_LULUS, BATAS_LULUS],
            mode="lines+text",
            line=dict(color="#FFDD57", width=4),
            text=["", f"  Batas Lulus = {BATAS_LULUS}"],
            textfont=dict(color="#FFDD57", size=10),
            showlegend=False, hoverinfo="skip",
        ))

        tick_vals = [i * GAP for i in range(n)]

        fig3.update_layout(
            title=dict(
                text="Visualisasi 3D Nilai Mahasiswa  ·  b = A·x",
                font=dict(size=14, color="white", family="Space Grotesk"),
                x=0,
            ),
            paper_bgcolor="#13132b",
            scene=dict(
                bgcolor="#0d0d1a",
                aspectmode="manual",
                aspectratio=dict(x=max(1.2, n * 0.18), y=0.4, z=1.0),
                xaxis=dict(
                    tickmode="array",
                    tickvals=tick_vals,
                    ticktext=nama_list,
                    tickfont=dict(color="#c0c8e0", size=9),
                    gridcolor="#2a2a4a",
                    showbackground=True,
                    backgroundcolor="#0d0d1a",
                    title=dict(text=""),
                    showspikes=False,
                ),
                yaxis=dict(
                    tickmode="array",
                    tickvals=[],
                    ticktext=[],
                    showticklabels=False,
                    gridcolor="#2a2a4a",
                    showbackground=True,
                    backgroundcolor="#0d0d1a",
                    title=dict(text=""),
                    showspikes=False,
                ),
                zaxis=dict(
                    range=[0, 115],
                    tickmode="linear",
                    tick0=0,
                    dtick=20,
                    tickfont=dict(color="#c0c8e0", size=9),
                    gridcolor="#2a2a4a",
                    showbackground=True,
                    backgroundcolor="#0d0d1a",
                    title=dict(text="Nilai Akhir",
                               font=dict(color="#c0c8e0", size=11)),
                    showspikes=False,
                ),
                camera=dict(eye=dict(x=1.8, y=-1.8, z=1.1)),
            ),
            font=dict(color="#c0c8e0", family="Space Grotesk"),
            showlegend=False,
            margin=dict(t=55, b=0, l=0, r=0),
            height=520,
        )
        st.plotly_chart(fig3, use_container_width=True)

# ── Radar ────────────────────────────────────
with tab_radar:
    if not data:
        st.info("Tambahkan data terlebih dahulu.")
    else:
        nama_options = [d["Nama"] for d in data]
        selected = st.multiselect(
            "Pilih mahasiswa (maks 6)",
            nama_options,
            default=nama_options[:min(5, len(nama_options))]
        )
        if selected:
            cats = ["Tugas","UTS","UAS"]
            fig_r = go.Figure()
            for nm in selected:
                d = next((x for x in data if x["Nama"]==nm), None)
                if d:
                    r = [d["Tugas"], d["UTS"], d["UAS"]]
                    fig_r.add_trace(go.Scatterpolar(
                        r=r+[r[0]], theta=cats+[cats[0]],
                        fill="toself", name=nm, opacity=.72,
                        hovertemplate="<b>%{theta}</b>: %{r:.0f}<extra>"+nm+"</extra>",
                    ))
            fig_r.update_layout(
                polar=dict(
                    bgcolor="#0d0d1a",
                    radialaxis=dict(range=[0,100], color="#c0c8e0", gridcolor="#2a2a4a"),
                    angularaxis=dict(color="#c0c8e0", gridcolor="#2a2a4a"),
                ),
                paper_bgcolor="#13132b",
                font=dict(color="#c0c8e0", family="Space Grotesk"),
                legend=dict(bgcolor="#0d0d1a", bordercolor="#2a2a4a", borderwidth=1),
                title=dict(text="Perbandingan Komponen Nilai",
                           font=dict(color="white",size=13), x=0),
                margin=dict(t=50,b=20), height=440,
            )
            st.plotly_chart(fig_r, use_container_width=True)

# ── Distribusi ───────────────────────────────
with tab_dist:
    if not data:
        st.info("Tambahkan data terlebih dahulu.")
    else:
        nilai_all = [d["Nilai Akhir"] for d in data]
        fig_h = go.Figure(go.Histogram(
            x=nilai_all, nbinsx=10,
            marker=dict(color="#A29BFE", line=dict(color="#0d0d1a",width=1)),
            opacity=.82, name="Distribusi",
            hovertemplate="Rentang: %{x}<br>Jumlah: %{y}<extra></extra>",
        ))
        fig_h.add_vline(x=BATAS_LULUS,
                        line=dict(color="#FFDD57",dash="dash",width=2),
                        annotation_text=f"  Batas Lulus={BATAS_LULUS}",
                        annotation_font=dict(color="#FFDD57"))
        fig_h.update_layout(
            title=dict(text="Distribusi Nilai Akhir",
                       font=dict(color="white",size=13), x=0),
            paper_bgcolor="#13132b", plot_bgcolor="#0d0d1a",
            font=dict(color="#c0c8e0"),
            xaxis=dict(title="Nilai Akhir", gridcolor="#1e1e38"),
            yaxis=dict(title="Jumlah Mahasiswa", gridcolor="#1e1e38"),
            margin=dict(t=50,b=20,l=10,r=10), height=380, bargap=.08,
        )
        st.plotly_chart(fig_h, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:1rem 0 1.5rem;
            color:#3d3d5c;font-size:.75rem;
            font-family:'JetBrains Mono',monospace;line-height:1.8">
    🎓 Sistem Penilaian Akademik Mahasiswa &nbsp;·&nbsp;
    Model <b style="color:#2ED573">b = A · x</b> &nbsp;·&nbsp;
    Bobot: 30% Tugas | 30% UTS | 40% UAS &nbsp;·&nbsp; Batas Lulus = 65
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .inner
