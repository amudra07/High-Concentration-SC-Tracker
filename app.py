"""
app.py

SC Tech Tracker — high-concentration subcutaneous delivery competitive
landscape. Three views, navigated via real URL query params (?page=...):

    ?page=home                      Executive summary (4 clickable category
                                     boxes + concentration ladder)
    ?page=category&category=<name>  Card list for one category
    ?page=landscape                 Full landscape overview (KPIs + chart)

Run with: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go

from tech_landscape_data import (
    ENTRIES,
    LAST_UPDATED,
    CATEGORIES,
    CATEGORY_META,
    entries_with_concentration,
    entries_by_category,
)

st.set_page_config(page_title="SC Tech Tracker", page_icon="💉", layout="wide")

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
        padding: 8px 22px;
        border-radius: 8px;
        font-size: 12px;
        letter-spacing: 0.06em;
        font-weight: 700;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    a.home-icon {
        font-size: 24px;
        text-decoration: none;
        line-height: 1;
    }
    a.home-icon:hover { opacity: 0.75; }

    .eyebrow { font-size: 11px; letter-spacing: 0.12em; font-weight: 700; color: #b45309; margin-bottom: 6px; }
    h1.page-title { font-size: 25px; margin: 0 0 4px; color: #7c2d12; }
    .subtitle { font-size: 13px; color: #64748b; margin-bottom: 22px; }

    a.num-box {
        display: block;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 10px;
        padding: 16px 14px;
        text-decoration: none;
        transition: box-shadow .15s, transform .15s;
        height: 100%;
    }
    a.num-box:hover { box-shadow: 0 6px 16px rgba(180,83,9,0.18); transform: translateY(-2px); }
    .num-circle {
        width: 26px; height: 26px; border-radius: 50%;
        background: #c2410c; color: #fff; font-size: 13px; font-weight: 700;
        display: flex; align-items: center; justify-content: center; margin-bottom: 10px;
    }
    .num-box .t { font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 4px; }
    .num-box .s { font-size: 11px; color: #b45309; font-style: italic; }

    a.ladder-card {
        display: block;
        background: #fff7ed; border: 1px solid #fed7aa; border-radius: 10px;
        padding: 18px 22px; text-decoration: none;
        transition: box-shadow .15s, transform .15s;
    }
    a.ladder-card:hover { box-shadow: 0 6px 16px rgba(180,83,9,0.18); transform: translateY(-2px); }
    .ladder-title { font-size: 12px; font-weight: 700; color: #7c2d12; margin-bottom: 4px; letter-spacing: 0.04em; }
    .ladder-hint { font-size: 11px; color: #b45309; margin-top: 4px; }

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


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def topbar(show_home: bool):
    home_html = '<a class="home-icon" href="?page=home" title="Back to executive summary">&#127968;</a>' if show_home else ""
    st.markdown(f"""
    <div class="topbar">
        <span>SC TECH TRACKER &middot; last updated {LAST_UPDATED.isoformat()}</span>
        {home_html}
    </div>
    """, unsafe_allow_html=True)


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
        deals_html = f"""
        <div class="deals-box">
            <span style="font-size:11px;color:#64748b;font-weight:700;">DEAL / NEWS ACTIVITY</span>
            <ul>{items}</ul>
        </div>
        """

    if entry["source_url"]:
        source_html = f"""
        <div class="source-line">
            Source: {entry['source_name']} &middot;
            <a href="{entry['source_url']}" target="_blank" rel="noopener">View reference for {entry['name']} &#8599;</a>
        </div>
        """
    else:
        source_html = f"""<div class="source-line">Source: {entry['source_name']} (internal, no external link)</div>"""

    st.markdown(f"""
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
    """, unsafe_allow_html=True)


def build_positioning_chart():
    """
    Scatter chart with two fixes for the label-overlap problem seen before:
    1. Points sharing an x-position get a small horizontal jitter so
       markers don't stack directly on top of each other.
    2. Marker labels are just a short reference number (not the full name),
       with a compact legend/key rendered underneath the chart. Full names
       only ever appear on hover or in the key — never as long overlapping
       chart text.
    """
    plotted = sorted(entries_with_concentration(), key=lambda e: -e["concentration_mgml"])

    # group by rounded base-x to detect and jitter collisions
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

    fig = go.Figure()
    by_category = {}
    for e in plotted:
        by_category.setdefault(e["category"], []).append(e)

    key_lines = []
    counter = 1
    id_to_number = {}
    for e in plotted:
        id_to_number[e["id"]] = counter
        counter += 1

    for category, items in by_category.items():
        fig.add_trace(go.Scatter(
            x=[jittered_x[e["id"]] for e in items],
            y=[e["concentration_mgml"] for e in items],
            mode="markers+text",
            name=category,
            text=[str(id_to_number[e["id"]]) for e in items],
            textposition="middle center",
            textfont={"size": 10, "color": "white"},
            marker={
                "size": [30 if e.get("is_internal") else 22 for e in items],
                "color": CATEGORY_COLOR.get(category, "#94a3b8") if category != "Suspension / particle"
                         else ["#ef4444" if e.get("is_internal") else CATEGORY_COLOR[category] for e in items],
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
            "range": [-0.6, 4.3],
            "gridcolor": "#f1f5f9",
        },
        yaxis={"title": "Concentration (mg/mL)", "range": [0, 760], "gridcolor": "#f1f5f9"},
        height=460,
        margin={"t": 60, "b": 70, "l": 60, "r": 20},
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0, "font": {"size": 11}},
    )

    for e in plotted:
        key_lines.append((id_to_number[e["id"]], e["name"], e["developer"], e["concentration_mgml"]))

    return fig, key_lines


# ─────────────────────────────────────────────────────────────────────────────
# Views
# ─────────────────────────────────────────────────────────────────────────────
def render_home():
    topbar(show_home=False)
    st.markdown('<div class="eyebrow">EXECUTIVE SUMMARY</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Four paths to high-concentration SC delivery — and where 700 mg/mL sits</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Click a numbered box to see that category\'s technologies. Click the ladder to see the full landscape.</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for col, category in zip(cols, CATEGORIES):
        meta = CATEGORY_META[category]
        with col:
            st.markdown(f"""
            <a class="num-box" href="?page=category&category={category.replace(' ', '+')}">
                <div class="num-circle">{meta['number']}</div>
                <div class="t">{meta['title']}</div>
                <div class="s">{meta['subtitle']}</div>
            </a>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <a class="ladder-card" href="?page=landscape">
        <div class="ladder-title">WHERE 700 MG/ML SITS ON THE CONCENTRATION LADDER</div>
        <div style="font-size:12px; color:#374151;">
            Commercial liquid ceiling ~150&ndash;175 mg/mL &rarr; leading external suspension platforms 400&ndash;500 mg/mL &rarr;
            <strong style="color:#b91c1c;">Hyperion (ours): 700 mg/mL</strong>
        </div>
        <div class="ladder-hint">Click to open the full landscape overview &rarr;</div>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box"><b>A real differentiator — but one that needs context</b><br>
        Is this a stable, syringeable powder-to-suspension system? What viscosity, glide-force, and long-term
        stability data exist at 700 mg/mL through a 23G needle?</div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box"><b>Dupixent's real strategic weakness</b><br>
        Not concentration — Dupixent's liquid formulation is simple, mature, low-complexity. A full loading dose
        still needs two injections, opening a convenience gap biosimilars can target directly.</div>
        """, unsafe_allow_html=True)


def render_category(category: str):
    topbar(show_home=True)
    if category not in CATEGORIES:
        st.error(f"Unknown category: {category}")
        return
    meta = CATEGORY_META[category]
    items = entries_by_category(category)

    st.markdown(f'<div class="eyebrow">CATEGORY {meta["number"]} OF {len(CATEGORIES)}</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="page-title">{meta["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{len(items)} technologies tracked in this category.</div>', unsafe_allow_html=True)

    for entry in items:
        render_card(entry)


def render_landscape():
    topbar(show_home=True)
    st.markdown('<div class="eyebrow">LANDSCAPE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">High-concentration SC delivery — technology landscape</h1>', unsafe_allow_html=True)
    n_with_conc = len(entries_with_concentration())
    top = max(entries_with_concentration(), key=lambda e: e["concentration_mgml"])
    n_commercial = sum(1 for e in ENTRIES if e["phase"] == "Commercial")
    st.markdown(
        f'<div class="subtitle">Benchmarks Dupixent and our internal platforms against {len(ENTRIES)} tracked '
        f'high-concentration and large-volume subcutaneous delivery technologies.</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi"><div class="v">{len(ENTRIES)}</div><div class="l">Technologies tracked</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi"><div class="v">{n_with_conc}</div><div class="l">With a comparable mg/mL</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi"><div class="v">{top["concentration_mgml"]}+</div><div class="l">Highest reported ({top["name"]})</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi"><div class="v">{n_commercial}</div><div class="l">Already commercial</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig, key_lines = build_positioning_chart()
    col_chart, col_side = st.columns([2.2, 1])
    with col_chart:
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div style="font-size:11px; color:#64748b; margin-top:-8px;">Reference key:</div>', unsafe_allow_html=True)
        key_html = "".join(
            f'<span style="font-size:11px; color:#374151; margin-right:14px;"><strong>{n}</strong> {name} ({dev}) &mdash; {conc} mg/mL</span>'
            for n, name, dev, conc in key_lines
        )
        st.markdown(f'<div style="line-height:2.1;">{key_html}</div>', unsafe_allow_html=True)
    with col_side:
        st.markdown("""
        <div class="side-panel">
            <b>READING THIS CHART</b>
            Only entries with a directly comparable mg/mL figure are plotted. Enzyme co-formulation platforms
            (ENHANZE, ALT-B4) enable large-volume delivery rather than raising concentration, so they sit
            outside this axis.<br><br>
            Points sharing a development stage are spread out slightly so markers and numbers never overlap —
            hover any point, or check the reference key below the chart, for the full name.
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────────────────────
params = st.query_params
page = params.get("page", "home")

if page == "home":
    render_home()
elif page == "category":
    render_category(params.get("category", ""))
elif page == "landscape":
    render_landscape()
else:
    render_home()
