"""
app.py

SC Tech Tracker — high-concentration subcutaneous delivery competitive
landscape. Navigation uses Streamlit's native session_state + st.button,
NOT anchor-tag query params — anchor-tag navigation was found to open a
new browser tab in deployed environments (Streamlit's own click handling
does not guarantee same-tab navigation for arbitrary <a> hrefs). Buttons
always rerun the app in-place, guaranteeing same-tab behavior everywhere.

Run with: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go

import db
import claude_extract
from tech_landscape_data import CATEGORIES, CATEGORY_META

st.set_page_config(page_title="SC Tech Tracker", page_icon="💉", layout="wide")

db.init_db()


def entries_with_concentration():
    return db.entries_with_concentration("curated")


def entries_by_category(category):
    return db.entries_by_category(category, "curated")


def _last_updated():
    curated = db.get_entries("curated")
    if not curated:
        return "n/a"
    return max(e["updated_at"][:10] for e in curated)

# ─────────────────────────────────────────────────────────────────────────────
# HTML helper — flattens leading whitespace on every line before rendering.
# Streamlit's markdown renderer treats any line indented 4+ spaces as an
# indented code block (raw text), which was silently breaking every card's
# deals/source section (they were built as separately-indented f-strings and
# then nested inside another indented f-string). Flattening prevents this
# everywhere, permanently.
# ─────────────────────────────────────────────────────────────────────────────
def md(html: str):
    flat = "\n".join(line.strip() for line in html.strip("\n").splitlines())
    st.markdown(flat, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Session state / navigation
# ─────────────────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "category" not in st.session_state:
    st.session_state.category = None


def go_home():
    st.session_state.page = "home"
    st.session_state.category = None


def go_category(cat):
    st.session_state.page = "category"
    st.session_state.category = cat


def go_landscape():
    st.session_state.page = "landscape"


def go_review():
    st.session_state.page = "review"


# ─────────────────────────────────────────────────────────────────────────────
# Theme (rust/orange, matching the source slide deck)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: #f4f1ec; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.2rem; max-width: 1100px; }

    .topbar {
        background: linear-gradient(135deg, #b45309, #9a3412);
        color: #fff7ed;
        padding: 12px 22px;
        border-radius: 8px;
        font-size: 12px;
        letter-spacing: 0.06em;
        font-weight: 700;
        height: 42px;
        display: flex;
        align-items: center;
    }

    /* Back-to-home button (top left, plain readable text) */
    div[data-testid="stButton"] button[kind="primary"] {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 8px;
        color: #b45309;
        font-weight: 700;
        font-size: 13px;
        padding: 6px 14px;
        min-height: 42px;
        height: 42px;
        width: 100%;
        box-shadow: none;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        color: #9a3412;
        background: #fff0dc;
        border-color: #c2410c;
    }

    /* Category / ladder navigation buttons (secondary, card look) */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 10px;
        color: #1e293b;
        font-weight: 700;
        font-size: 13px;
        text-align: left;
        justify-content: flex-start;
        white-space: pre-line;
        min-height: 78px;
        padding: 14px 16px;
        line-height: 1.5;
        width: 100%;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        border-color: #c2410c;
        box-shadow: 0 6px 16px rgba(180,83,9,0.18);
        color: #1e293b;
    }

    .box-sub {
        font-size: 11px;
        color: #b45309;
        font-style: italic;
        margin-top: 6px;
        min-height: 32px;
    }

    .eyebrow { font-size: 11px; letter-spacing: 0.12em; font-weight: 700; color: #b45309; margin: 18px 0 6px; }
    h1.page-title { font-size: 25px; margin: 0 0 4px; color: #7c2d12; }
    .subtitle { font-size: 13px; color: #64748b; margin-bottom: 22px; }

    .ladder-box {
        background: #fff7ed; border: 1px solid #fed7aa; border-bottom: none;
        border-radius: 10px 10px 0 0; padding: 18px 26px 8px;
    }
    .ladder-title { font-size: 12px; font-weight: 700; color: #7c2d12; margin-bottom: 18px; letter-spacing: 0.04em; }
    .ladder-track { position: relative; height: 6px; background: #fed7aa; border-radius: 3px; margin: 0 20px 46px; }
    .ladder-dot { position: absolute; top: -5px; width: 16px; height: 16px; border-radius: 50%; border: 2px solid #fff7ed; }
    .ladder-label { position: absolute; top: 14px; font-size: 10.5px; color: #475569; white-space: nowrap; transform: translateX(-50%); text-align: center; }
    .ladder-label b { display: block; font-size: 11px; }

    #ladder_btn button {
        border-radius: 0 0 10px 10px !important;
        border-top: none !important;
        margin-top: -1px;
    }

    .info-box { background: #fdf6ee; border-radius: 8px; padding: 14px 18px; font-size: 12px; color: #475569; line-height: 1.6; }
    .info-box b { color: #1e293b; }

    .kpi { background: #fdf6ee; border-radius: 8px; padding: 12px 14px; text-align: left; }
    .kpi .v { font-size: 20px; font-weight: 700; color: #7c2d12; }
    .kpi .l { font-size: 11px; color: #64748b; margin-top: 2px; }

    .card {
        background: #fff; border: 1px solid #e2e8f0; border-left: 4px solid #c2410c;
        border-radius: 8px; padding: 16px 20px; margin-bottom: 14px;
    }
    .card.internal { border-left-color: #ef4444; }
    .card-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;}
    .card-head .name { font-size: 15px; font-weight: 700; color: #1e293b; }
    .card-head .dev { font-size: 11px; color: #94a3b8; }
    .badge { display: inline-block; font-size: 10px; font-weight: 700; padding: 3px 9px; border-radius: 10px; margin-right: 6px; }
    .field-label { font-size: 10px; color: #94a3b8; letter-spacing: 0.04em; margin-top: 10px; }
    .field-val { font-size: 13px; color: #1e293b; font-weight: 600; }
    .field-val.muted { color: #94a3b8; font-weight: 400; }
    .mech-box { background: #f8fafc; border-radius: 6px; padding: 10px 14px; font-size: 12px; color: #374151; line-height: 1.55; margin-top: 4px; }
    .deals-box { margin-top: 10px; }
    .deals-box ul { font-size: 12px; color: #374151; line-height: 1.6; margin: 4px 0 0; padding-left: 18px; }
    .source-line { font-size: 11px; color: #64748b; margin-top: 10px; }
    .source-line a { color: #b45309; text-decoration: none; font-weight: 600; }
    .source-line a:hover { text-decoration: underline; }

    .side-panel { background: #fff7ed; border-radius: 8px; padding: 14px 16px; font-size: 12px; color: #7c2d12; line-height: 1.7; }
    .side-panel b { display: block; margin-bottom: 6px; font-size: 11px; letter-spacing: 0.04em; }
</style>
""", unsafe_allow_html=True)

PHASE_BADGE = {
    "Commercial": ("#dcfce7", "#15803d"),
    "CDMO service available": ("#dbeafe", "#1d4ed8"),
    "Phase 3": ("#ede9fe", "#6d28d9"),
    "Phase 1": ("#fef3c7", "#b45309"),
    "Preclinical": ("#fef3c7", "#b45309"),
    "Platform PoC": ("#fce7f3", "#9d174d"),
    "Proof-of-concept": ("#f1f5f9", "#475569"),
    "Internal R&D": ("#fee2e2", "#b91c1c"),
}

STAGE_X = {
    "Proof-of-concept": 0,
    "Platform PoC": 0.6,
    "Preclinical": 1.2,
    "Internal R&D": 1.2,
    "Phase 1": 2.2,
    "Phase 3": 2.8,
    "CDMO service available": 3.3,
    "Commercial": 3.8,
}
STAGE_TICKS = [0, 0.6, 1.2, 2.2, 2.8, 3.3, 3.8]
STAGE_LABELS = ["Proof-of-\nconcept", "Platform\nPoC", "Preclinical /\nInternal",
                "Phase 1", "Phase 3", "CDMO\nservice", "Commercial"]

CATEGORY_COLOR = {
    "Liquid + excipient": "#3b82f6",
    "Enzyme co-formulation": "#f59e0b",
    "Suspension / particle": "#10b981",
    "Crystalline": "#8b5cf6",
}

# Display label used only for the chart legend — keeps the underlying
# category name (used for cards, routing, colors) unchanged.
CATEGORY_LEGEND_LABEL = {
    "Suspension / particle": "Target Concentration",
}

CIRCLED_DIGITS = {1: "①", 2: "②", 3: "③", 4: "④"}

LADDER_MAX = 800
LADDER_POINTS = [
    (175, "#3b82f6", "Commercial liquid ceiling", "~150–175 mg/mL"),
    (500, "#10b981", "Leading external suspension", "400–500 mg/mL"),
    (700, "#ef4444", "Hyperion (ours)", "700 mg/mL"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Shared components
# ─────────────────────────────────────────────────────────────────────────────
def topbar():
    show_home = st.session_state.page != "home"
    n_pending = len(db.get_entries("staging"))
    col1, col2, col3 = st.columns([2, 7, 2])
    with col1:
        if show_home:
            st.button("← Back to home", key="home_btn", type="primary", on_click=go_home)
    with col2:
        md(f"""
        <div class="topbar">SC TECH TRACKER &middot; last updated {_last_updated()}</div>
        """)
    with col3:
        label = f"📋 {n_pending} pending" if n_pending else "📋 Review"
        st.button(label, key="review_btn", on_click=go_review, use_container_width=True)


def render_card(entry):
    bg, fc = PHASE_BADGE.get(entry["phase"], ("#f1f5f9", "#475569"))
    is_internal = entry.get("is_internal", False)
    card_class = "card internal" if is_internal else "card"
    star = " &#11088;" if is_internal else ""

    needle = entry.get("needle_size_g", "Not disclosed")
    needle_class = "field-val" if needle != "Not disclosed" else "field-val muted"

    deals_html = ""
    if entry["deals"]:
        items = "".join(f"<li>{d}</li>" for d in entry["deals"])
        deals_html = (
            '<div class="deals-box">'
            '<span style="font-size:11px;color:#64748b;font-weight:700;">DEAL / NEWS ACTIVITY</span>'
            f"<ul>{items}</ul>"
            "</div>"
        )

    if entry["source_url"]:
        source_html = (
            '<div class="source-line">'
            f"Source: {entry['source_name']} &middot; "
            f'<a href="{entry["source_url"]}" target="_blank" rel="noopener">'
            f"View reference for {entry['name']} &#8599;</a>"
            "</div>"
        )
    else:
        source_html = f'<div class="source-line">Source: {entry["source_name"]} (internal, no external link)</div>'

    md(f"""
    <div class="{card_class}">
        <div class="card-head">
            <span class="name">{entry['name']}{star}</span>
            <span class="dev">{entry['developer']}</span>
        </div>
        <span class="badge" style="background:{bg};color:{fc};">{entry['phase']}</span>
        <span class="badge" style="background:#f1f5f9;color:#475569;">{entry['category']}</span>
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:16px;">
            <div>
                <div class="field-label">CONCENTRATION</div>
                <div class="field-val">{entry['concentration_display']}</div>
                <div class="field-label">NEEDLE SIZE</div>
                <div class="{needle_class}">{needle}</div>
            </div>
            <div>
                <div class="field-label">MECHANISM</div>
                <div class="mech-box">{entry['mechanism_long']}</div>
                {deals_html}
                {source_html}
            </div>
        </div>
    </div>
    """)


def render_ladder():
    dots_html = ""
    labels_html = ""
    for value, color, label, sub in LADDER_POINTS:
        pct = max(6, min(94, (value / LADDER_MAX) * 100))
        dots_html += f'<div class="ladder-dot" style="left:{pct}%; background:{color};"></div>'
        labels_html += f'<div class="ladder-label" style="left:{pct}%;"><b>{label}</b>{sub}</div>'

    md(f"""
    <div class="ladder-box">
        <div class="ladder-title">WHERE 700 MG/ML SITS ON THE CONCENTRATION LADDER</div>
        <div class="ladder-track">{dots_html}{labels_html}</div>
    </div>
    """)


def build_positioning_chart():
    """
    Points sharing a development stage are jittered apart on x (as before).
    Labels are the real technology names, placed via leader-line annotations
    rather than printed inside the marker. Placement is chosen by a greedy
    collision-avoidance pass: candidate offsets are tried in order of
    increasing distance from the point, and the first one whose estimated
    text bounding box doesn't overlap any already-placed label is used.
    This is what actually prevents overlap regardless of how many points
    cluster in one area \u2014 not a fixed rule like "always place above".
    """
    plotted = sorted(entries_with_concentration(), key=lambda e: -e["concentration_mgml"])

    base_x = {}
    for e in plotted:
        bx = STAGE_X.get(e["phase"], 1.2)
        base_x.setdefault(bx, []).append(e)

    jittered_x = {}
    for bx, group in base_x.items():
        n = len(group)
        if n == 1:
            jittered_x[group[0]["id"]] = bx
        else:
            spread = min(0.45, 0.16 * (n - 1))
            step = (2 * spread) / (n - 1)
            for i, e in enumerate(group):
                jittered_x[e["id"]] = bx - spread + i * step

    by_category = {}
    for e in plotted:
        by_category.setdefault(e["category"], []).append(e)

    # ── approximate data -> pixel mapping (must match the layout below) ──
    X_RANGE = (-0.6, 4.3)
    Y_RANGE = (0, 760)
    PLOT_W, PLOT_H = 1300, 330  # inside the l/r/t/b margins set below (matches the widened landscape container)
    px_per_x = PLOT_W / (X_RANGE[1] - X_RANGE[0])
    px_per_y = PLOT_H / (Y_RANGE[1] - Y_RANGE[0])

    def to_px(x, y):
        return ((x - X_RANGE[0]) * px_per_x, (Y_RANGE[1] - y) * px_per_y)

    def label_box(px, py, ax, ay, text):
        cx, cy = px + ax, py + ay
        w = max(24, len(text) * 5.6 + 10)
        h = 15
        return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

    def overlaps(a, b, pad=3):
        return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])

    # candidate offsets tried nearest-first; alternates side/direction
    CANDIDATES = [
        (0, -26), (0, 26),
        (34, -22), (-34, -22), (34, 22), (-34, 22),
        (55, -40), (-55, -40), (55, 40), (-55, 40),
        (0, -55), (0, 55),
        (75, -18), (-75, -18), (75, 18), (-75, 18),
        (0, -80), (0, 80),
        (95, 5), (-95, 5),
    ]

    placed_boxes = []
    annotations = []
    for e in plotted:
        x = jittered_x[e["id"]]
        y = e["concentration_mgml"]
        px, py = to_px(x, y)
        text = e["name"]
        chosen = None
        for ax, ay in CANDIDATES:
            box = label_box(px, py, ax, ay, text)
            if not any(overlaps(box, other) for other in placed_boxes):
                chosen = (ax, ay, box)
                break
        if chosen is None:
            ax, ay = CANDIDATES[-1]
            chosen = (ax, ay, label_box(px, py, ax, ay, text))
        ax, ay, box = chosen
        placed_boxes.append(box)
        annotations.append(dict(
            x=x, y=y, text=text, showarrow=True,
            arrowhead=0, arrowwidth=1, arrowcolor="#cbd5e1",
            ax=ax, ay=ay, font={"size": 10, "color": "#475569"},
            bgcolor="rgba(255,255,255,0.85)",
        ))

    fig = go.Figure()
    for category, items in by_category.items():
        fig.add_trace(go.Scatter(
            x=[jittered_x[e["id"]] for e in items],
            y=[e["concentration_mgml"] for e in items],
            mode="markers",
            name=CATEGORY_LEGEND_LABEL.get(category, category),
            marker={
                "size": [24 if e.get("is_internal") else 17 for e in items],
                "color": (CATEGORY_COLOR.get(category, "#94a3b8") if category != "Suspension / particle"
                          else ["#ef4444" if e.get("is_internal") else CATEGORY_COLOR[category] for e in items]),
                "line": {"width": 2, "color": "white"},
            },
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>%{y} mg/mL<extra></extra>",
            customdata=[[e["name"], e["developer"]] for e in items],
        ))

    fig.update_layout(
        xaxis={
            "title": "Development stage",
            "tickmode": "array",
            "tickvals": STAGE_TICKS,
            "ticktext": STAGE_LABELS,
            "range": [X_RANGE[0], X_RANGE[1]],
            "gridcolor": "#f1f5f9",
        },
        yaxis={"title": "Concentration (mg/mL)", "range": [Y_RANGE[0], Y_RANGE[1]], "gridcolor": "#f1f5f9"},
        height=460,
        margin={"t": 60, "b": 70, "l": 60, "r": 20},
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0, "font": {"size": 11}},
        annotations=annotations,
    )

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Views
# ─────────────────────────────────────────────────────────────────────────────
def render_home():
    topbar()
    md('<div class="eyebrow">EXECUTIVE SUMMARY</div>')
    md('<h1 class="page-title">Four paths to high-concentration SC delivery — Positioning of our technology</h1>')
    md('<div class="subtitle">Click a numbered box to see that category\'s technologies. Click the ladder to see the full landscape.</div>')

    _, refresh_col = st.columns([3, 1])
    with refresh_col:
        if st.button("🔄 Refresh intelligence", key="refresh_btn", use_container_width=True):
            try:
                claude_extract.get_api_key()  # fail fast, before burning 4 searches
            except claude_extract.MissingAPIKeyError as exc:
                st.error(str(exc))
            else:
                with st.spinner("Searching all 4 categories — this can take a minute or two..."):
                    candidates = claude_extract.search_all_categories()
                    db.add_staging_entries(candidates)
                st.success(f"Found {len(candidates)} candidate(s). Review them before they go live.")
                go_review()
                st.rerun()

    ordered = sorted(CATEGORIES, key=lambda c: CATEGORY_META[c]["number"])
    cols = st.columns(4)
    for col, category in zip(cols, ordered):
        meta = CATEGORY_META[category]
        with col:
            label = f"{CIRCLED_DIGITS[meta['number']]}  {meta['title']}"
            st.button(label, key=f"cat_btn_{meta['number']}", on_click=go_category, args=(category,), use_container_width=True)
            md(f'<div class="box-sub">{meta["subtitle"]}</div>')

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    render_ladder()
    st.button("Click to open the full landscape overview →", key="ladder_btn", on_click=go_landscape, use_container_width=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        md("""
        <div class="info-box"><b>A real differentiator — but one that needs context</b><br>
        Is this a stable, syringeable powder-to-suspension system? What viscosity, glide-force, and long-term
        stability data exist at 700 mg/mL through a 23G needle?</div>
        """)
    with c2:
        md("""
        <div class="info-box"><b>Dupixent's real strategic weakness</b><br>
        Not concentration — Dupixent's liquid formulation is simple, mature, low-complexity. A full loading dose
        still needs two injections, opening a convenience gap biosimilars can target directly.</div>
        """)


def render_category(category: str):
    topbar()
    if category not in CATEGORIES:
        st.error(f"Unknown category: {category}")
        return
    meta = CATEGORY_META[category]
    items = entries_by_category(category)

    md(f'<div class="eyebrow">CATEGORY {meta["number"]} OF {len(CATEGORIES)}</div>')
    md(f'<h1 class="page-title">{meta["title"]}</h1>')
    md(f'<div class="subtitle">{len(items)} technologies tracked in this category.</div>')

    for entry in items:
        render_card(entry)


def render_landscape():
    topbar()
    md("<style>.block-container { max-width: 1400px !important; }</style>")
    md('<div class="eyebrow">LANDSCAPE OVERVIEW</div>')
    md('<h1 class="page-title">High-concentration SC delivery — technology landscape</h1>')
    curated = db.get_entries("curated")
    n_with_conc = len(entries_with_concentration())
    top = max(entries_with_concentration(), key=lambda e: e["concentration_mgml"])
    n_commercial = sum(1 for e in curated if e["phase"] == "Commercial")
    md(
        f'<div class="subtitle">Benchmarks Dupixent and our internal platforms against {len(curated)} tracked '
        f'high-concentration and large-volume subcutaneous delivery technologies.</div>'
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        md(f'<div class="kpi"><div class="v">{len(curated)}</div><div class="l">Technologies tracked</div></div>')
    with k2:
        md(f'<div class="kpi"><div class="v">{n_with_conc}</div><div class="l">With a comparable mg/mL</div></div>')
    with k3:
        md(f'<div class="kpi"><div class="v">{top["concentration_mgml"]}+</div><div class="l">Targeted {top["name"]} Concentration</div></div>')
    with k4:
        md(f'<div class="kpi"><div class="v">{n_commercial}</div><div class="l">Already commercial</div></div>')

    st.markdown("<br>", unsafe_allow_html=True)

    fig = build_positioning_chart()
    st.plotly_chart(fig, use_container_width=True)
    md("""
    <div class="side-panel">
        <b>READING THIS CHART</b>
        Only entries with a directly comparable mg/mL figure are plotted. Enzyme co-formulation platforms
        (ENHANZE, ALT-B4) enable large-volume delivery rather than raising concentration, so they sit
        outside this axis.<br><br>
        Points sharing a development stage are spread out slightly, and each name is placed by an
        automatic layout pass that keeps labels from overlapping \u2014 hover any point for the developer too.
    </div>
    """)


def render_review():
    topbar()
    md('<div class="eyebrow">HUMAN REVIEW</div>')
    md('<h1 class="page-title">Pending intelligence candidates</h1>')

    staged = db.get_entries("staging")
    if not staged:
        md('<div class="subtitle">Nothing pending. Run "Refresh intelligence" from the home page to search for updates.</div>')
        return

    md(f'<div class="subtitle">{len(staged)} candidate(s) found by Claude, not yet on the dashboard. '
       f'Approve, edit, or reject each before it becomes visible.</div>')

    CONFIDENCE_THRESHOLD = 0.75

    for entry in staged:
        conf = entry.get("confidence", 0.5) or 0.0
        if conf >= CONFIDENCE_THRESHOLD:
            conf_color, conf_label = "#15803d", "High confidence"
        elif conf >= 0.4:
            conf_color, conf_label = "#b45309", "Medium confidence"
        else:
            conf_color, conf_label = "#b91c1c", "Low confidence"

        render_card(entry)
        md(f'<div style="margin-top:-10px; margin-bottom:8px; font-size:11px; '
           f'color:{conf_color}; font-weight:700;">{conf_label} ({conf:.2f})</div>')

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("✅ Approve", key=f"approve-{entry['id']}", use_container_width=True):
                db.approve_entry(entry["id"])
                st.rerun()
        with c2:
            with st.popover("✏️ Edit", use_container_width=True):
                new_conc = st.number_input(
                    "Concentration (mg/mL)", value=float(entry.get("concentration_mgml") or 0.0),
                    key=f"conc-{entry['id']}",
                )
                phases = ["Proof-of-concept", "Platform PoC", "Preclinical", "Phase 1",
                          "Phase 3", "Commercial", "CDMO service available"]
                current_phase = entry.get("phase") if entry.get("phase") in phases else phases[0]
                new_phase = st.selectbox("Phase", phases, index=phases.index(current_phase), key=f"phase-{entry['id']}")
                if st.button("Save edits", key=f"save-{entry['id']}"):
                    db.update_staging_entry(entry["id"], {"concentration_mgml": new_conc, "phase": new_phase})
                    st.rerun()
        with c3:
            if st.button("❌ Reject", key=f"reject-{entry['id']}", use_container_width=True):
                db.reject_entry(entry["id"])
                st.rerun()

        st.markdown("<hr style='margin:8px 0 20px; border-color:#f1f5f9;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "category":
    render_category(st.session_state.category)
elif st.session_state.page == "landscape":
    render_landscape()
elif st.session_state.page == "review":
    render_review()
else:
    render_home()
