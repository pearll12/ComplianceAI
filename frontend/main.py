import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# --- Page Configuration ---
st.set_page_config(
    page_title="PDF Compliance Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS: Bold Neon / Electric Dark Theme with Large Typography ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-base:        #07080d;
        --bg-panel:       #0e1018;
        --bg-card:        #13151f;
        --bg-card-hover:  #1a1d2a;
        --border:         #1e2236;
        --border-bright:  #2a2f48;
        --accent-cyan:    #00f5ff;
        --accent-violet:  #a855f7;
        --accent-amber:   #fbbf24;
        --accent-red:     #ff4d6d;
        --accent-green:   #00e5a0;
        --glow-cyan:      rgba(0,245,255,0.15);
        --glow-violet:    rgba(168,85,247,0.15);
        --text-primary:   #f0f4ff;
        --text-secondary: #7a869e;
        --text-muted:     #3a4259;
        --font-display:   'Syne', sans-serif;
        --font-mono:      'IBM Plex Mono', monospace;
        --font-body:      'Manrope', sans-serif;
    }

    /* ── Global Reset ── */
    .stApp {
        background: var(--bg-base);
        font-family: var(--font-body);
        background-image:
            radial-gradient(ellipse 80% 40% at 50% -10%, rgba(0,245,255,0.05) 0%, transparent 60%),
            radial-gradient(ellipse 60% 30% at 90% 80%, rgba(168,85,247,0.04) 0%, transparent 50%);
    }
    .main .block-container { padding: 2.5rem 3.5rem; max-width: 1440px; }
    html, body, [class*="css"] { color: var(--text-primary); }

    /* ── Header Banner ── */
    .dash-header {
        background: linear-gradient(135deg, #0d1020 0%, #111428 60%, #0a0d1a 100%);
        border: 1px solid var(--border-bright);
        border-top: 3px solid var(--accent-cyan);
        padding: 2.5rem 3rem;
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        border-radius: 8px;
    }
    .dash-header::before {
        content: '';
        position: absolute;
        top: -80px; right: -80px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0,245,255,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .dash-header::after {
        content: '';
        position: absolute;
        bottom: -40px; left: 30%;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(168,85,247,0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    .dash-header h1 {
        font-family: var(--font-display);
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        margin: 0 0 0.5rem;
        line-height: 1.1;
    }
    .dash-header h1 span {
        color: var(--accent-cyan);
        text-shadow: 0 0 30px rgba(0,245,255,0.4);
    }
    .dash-header p {
        font-family: var(--font-body);
        color: var(--text-secondary);
        font-size: 1rem;
        margin: 0;
        letter-spacing: 0.01em;
        font-weight: 500;
    }
    .dash-header .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0,229,160,0.1);
        border: 1px solid rgba(0,229,160,0.3);
        color: var(--accent-green);
        font-family: var(--font-mono);
        font-size: 0.8rem;
        padding: 0.35em 1em;
        border-radius: 100px;
        margin-top: 1.25rem;
        letter-spacing: 0.06em;
        font-weight: 600;
    }
    .dot-pulse {
        width: 7px; height: 7px;
        background: var(--accent-green);
        border-radius: 50%;
        box-shadow: 0 0 8px var(--accent-green);
        display: inline-block;
    }

    /* ── KPI Cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 2.5rem;
    }
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.75rem 2rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s, border-color 0.2s;
    }
    .kpi-card:hover { transform: translateY(-2px); }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 10px 10px 0 0;
    }
    .kpi-card.cyan::before   { background: var(--accent-cyan); box-shadow: 0 0 20px rgba(0,245,255,0.5); }
    .kpi-card.amber::before  { background: var(--accent-amber); box-shadow: 0 0 20px rgba(251,191,36,0.5); }
    .kpi-card.red::before    { background: var(--accent-red); box-shadow: 0 0 20px rgba(255,77,109,0.5); }
    .kpi-card.green::before  { background: var(--accent-green); box-shadow: 0 0 20px rgba(0,229,160,0.5); }
    .kpi-card .kpi-icon {
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
        display: block;
    }
    .kpi-label {
        font-family: var(--font-body);
        font-size: 0.92rem;
        letter-spacing: 0.02em;
        color: #9aabbe;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .kpi-value {
        font-family: var(--font-display);
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1;
        color: var(--text-primary);
        letter-spacing: -0.03em;
    }
    .kpi-delta {
        font-family: var(--font-body);
        font-size: 0.88rem;
        margin-top: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .kpi-delta.up   { color: var(--accent-green); }
    .kpi-delta.down { color: var(--accent-red); }
    .kpi-delta.inv-down { color: var(--accent-green); }

    /* ── Section Headers ── */
    .section-title {
        font-family: var(--font-display);
        font-size: 1.05rem;
        letter-spacing: 0.06em;
        color: #c8d4e8;
        text-transform: uppercase;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.75rem;
        margin-bottom: 1.5rem;
        font-weight: 800;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 0.35rem !important;
        gap: 0.25rem !important;
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        font-family: var(--font-display) !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.7rem 1.75rem !important;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0,245,255,0.08) !important;
        color: var(--accent-cyan) !important;
        text-shadow: 0 0 20px rgba(0,245,255,0.5);
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 1.75rem; }

    /* ── Severity Badges ── */
    .badge {
        display: inline-block;
        font-family: var(--font-body);
        font-size: 0.82rem;
        letter-spacing: 0.04em;
        padding: 0.32em 0.9em;
        border-radius: 5px;
        font-weight: 700;
    }
    .badge-critical { background: rgba(255,77,109,0.15); color: #ff4d6d; border: 1px solid rgba(255,77,109,0.4); }
    .badge-high     { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.4); }
    .badge-medium   { background: rgba(168,85,247,0.15); color: #c084fc; border: 1px solid rgba(168,85,247,0.4); }
    .badge-low      { background: rgba(0,229,160,0.15);  color: #00e5a0; border: 1px solid rgba(0,229,160,0.4); }

    /* ── Table Rows ── */
    .vio-table tr:hover td { background: rgba(0,245,255,0.02) !important; }

    /* ── Streamlit element overrides ── */
    .stMetric { display: none; }

    div[data-testid="stFileUploader"] {
        border: 2px dashed var(--border-bright) !important;
        background: var(--bg-card) !important;
        border-radius: 8px !important;
        padding: 2rem !important;
        transition: border-color 0.2s;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: rgba(0,245,255,0.3) !important;
    }
    div[data-testid="stFileUploader"] * {
        color: var(--text-secondary) !important;
        font-family: var(--font-body) !important;
        font-size: 0.95rem !important;
    }

    div[data-testid="stAlert"] {
        background: rgba(0,245,255,0.05) !important;
        border: 1px solid rgba(0,245,255,0.2) !important;
        color: var(--text-secondary) !important;
        border-radius: 6px !important;
    }

    .stMultiSelect > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-bright) !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
    }
    .stMultiSelect span {
        font-family: var(--font-body) !important;
        font-size: 0.85rem !important;
    }
    label[data-testid="stWidgetLabel"] p {
        font-family: var(--font-display) !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        color: var(--text-secondary) !important;
    }

    div[data-testid="stSuccessMessage"] {
        background: rgba(0,229,160,0.08) !important;
        border: 1px solid rgba(0,229,160,0.25) !important;
        color: var(--accent-green) !important;
        border-radius: 6px !important;
        font-family: var(--font-mono) !important;
        font-size: 0.85rem !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,245,255,0.2); }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="dash-header">
    <h1>⬡ PDF <span>COMPLIANCE</span> TRACKER</h1>
    <p>Automated document scanning · Violation detection · Audit trail</p>
    <div class="status-pill">
        <span class="dot-pulse"></span>
        SYSTEM OPERATIONAL
    </div>
</div>
""", unsafe_allow_html=True)

# --- KPI Cards ---
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card cyan">
        <span class="kpi-icon">📄</span>
        <div class="kpi-label">PDFs Processed</div>
        <div class="kpi-value">128</div>
        <div class="kpi-delta up">↑ +12% from last period</div>
    </div>
    <div class="kpi-card red">
        <span class="kpi-icon">🚨</span>
        <div class="kpi-label">Active Violations</div>
        <div class="kpi-value">30</div>
        <div class="kpi-delta inv-down">↓ −5% improvement</div>
    </div>
    <div class="kpi-card amber">
        <span class="kpi-icon">🔍</span>
        <div class="kpi-label">Under Review</div>
        <div class="kpi-value">8</div>
        <div class="kpi-delta up">↑ 3 new this week</div>
    </div>
    <div class="kpi-card green">
        <span class="kpi-icon">✅</span>
        <div class="kpi-label">Resolved</div>
        <div class="kpi-value">94</div>
        <div class="kpi-delta inv-down">↑ 73% resolution rate</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Tabs ---
tab_graph, tab_upload, tab_violations = st.tabs([
    "  📊  ANALYTICS",
    "  📁  UPLOAD",
    "  ⚠   VIOLATIONS"
])

# ══════════════════════════════════════════
# TAB 1: Analytics
# ══════════════════════════════════════════
with tab_graph:
    st.markdown('<div class="section-title">Compliance Analytics Overview</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        dept_data = pd.DataFrame({
            'Department': ['HR', 'Finance', 'Legal', 'IT', 'Operations', 'Marketing'],
            'Violations': [5, 12, 3, 8, 2, 7],
            'Resolved':   [4, 9, 3, 6, 2, 5]
        })

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=dept_data['Department'], y=dept_data['Violations'],
            name='Active Violations',
            marker=dict(
                color=dept_data['Violations'],
                colorscale=[[0, '#1a2535'], [0.4, '#0a3d6b'], [0.7, '#00a8d4'], [1.0, '#00f5ff']],
                line=dict(width=0)
            )
        ))
        fig_bar.add_trace(go.Bar(
            x=dept_data['Department'], y=dept_data['Resolved'],
            name='Resolved',
            marker=dict(color='rgba(0,229,160,0.3)', line=dict(color='rgba(0,229,160,0.5)', width=1))
        ))
        fig_bar.update_layout(
            title=dict(
                text='Violations by Department',
                font=dict(family='Syne', size=15, color='#7a869e'),
                x=0
            ),
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Manrope', color='#7a869e', size=13),
            xaxis=dict(gridcolor='#1a2030', linecolor='#1e2236', tickfont=dict(color='#7a869e', size=13)),
            yaxis=dict(gridcolor='#1a2030', linecolor='rgba(0,0,0,0)', tickfont=dict(color='#7a869e', size=12)),
            legend=dict(font=dict(family='Manrope', size=12, color='#7a869e'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=45, b=10, l=10, r=10),
            height=320,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        sev_data = pd.DataFrame({
            'Severity': ['Critical', 'High', 'Medium', 'Low'],
            'Count':    [4, 11, 9, 6]
        })
        colors = ['#ff4d6d', '#fbbf24', '#a855f7', '#00e5a0']
        fig_donut = go.Figure(go.Pie(
            labels=sev_data['Severity'], values=sev_data['Count'],
            hole=0.65,
            marker=dict(colors=colors, line=dict(color='#07080d', width=4)),
            textfont=dict(family='Manrope', size=13, color='#7a869e'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
        ))
        fig_donut.add_annotation(
            text='<b style="font-size:22px">30</b><br><span style="font-size:11px; color:#7a869e">VIOLATIONS</span>',
            x=0.5, y=0.5, showarrow=False,
            font=dict(family='Syne', size=18, color='#f0f4ff'), align='center'
        )
        fig_donut.update_layout(
            title=dict(text='Severity Distribution', font=dict(family='Syne', size=15, color='#7a869e'), x=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                font=dict(family='Manrope', size=13, color='#7a869e'),
                bgcolor='rgba(0,0,0,0)',
                orientation='h', y=-0.12
            ),
            margin=dict(t=45, b=10, l=10, r=10),
            height=320,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown('<div class="section-title" style="margin-top:1rem;">Monthly Violation Trend</div>', unsafe_allow_html=True)
    months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
    trend_vals = [42, 38, 35, 44, 31, 27, 30]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=months, y=trend_vals, mode='lines+markers',
        line=dict(color='#00f5ff', width=2.5),
        marker=dict(size=8, color='#00f5ff', symbol='circle',
                    line=dict(color='#07080d', width=2.5)),
        fill='tozeroy',
        fillcolor='rgba(0,245,255,0.06)',
        name='Violations'
    ))
    fig_line.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Manrope', color='#7a869e', size=13),
        xaxis=dict(gridcolor='#1a2030', linecolor='#1e2236', tickfont=dict(color='#7a869e', size=13)),
        yaxis=dict(gridcolor='#1a2030', linecolor='rgba(0,0,0,0)', tickfont=dict(color='#7a869e', size=12)),
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        height=200,
    )
    st.plotly_chart(fig_line, use_container_width=True)


# ══════════════════════════════════════════
# TAB 2: Upload
# ══════════════════════════════════════════
with tab_upload:
    st.markdown('<div class="section-title">Document Ingestion Pipeline</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2], gap="large")
    with col_a:
        st.markdown("""
        <div style="background:#0e1018; border:1px solid #1e2236; padding:2rem; border-radius:10px; margin-bottom:1.25rem;">
            <div style="font-family:'Syne',sans-serif; font-size:1rem; letter-spacing:0.06em; color:#c8d4e8; text-transform:uppercase; margin-bottom:1.5rem; font-weight:800;">
                Scan Configuration
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                <div style="background:#13151f; border:1px solid #1e2236; padding:1rem 1.25rem; border-radius:8px;">
                    <div style="font-family:'Manrope',sans-serif; font-size:0.78rem; color:#6a7a96; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:0.4rem; font-weight:700;">CHECK TYPE</div>
                    <div style="font-family:'Manrope',sans-serif; color:#f0f4ff; font-size:1rem; font-weight:700;">Full Compliance Scan</div>
                </div>
                <div style="background:#13151f; border:1px solid #1e2236; padding:1rem 1.25rem; border-radius:8px;">
                    <div style="font-family:'Manrope',sans-serif; font-size:0.78rem; color:#6a7a96; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:0.4rem; font-weight:700;">PII DETECTION</div>
                    <div style="font-size:0.85rem; margin-top:0.1rem;">
                        <span style="color:#00e5a0; font-family:'Manrope',sans-serif; font-size:0.9rem; font-weight:800; background:rgba(0,229,160,0.1); padding:0.2em 0.75em; border-radius:5px; border:1px solid rgba(0,229,160,0.3);">● ENABLED</span>
                    </div>
                </div>
                <div style="background:#13151f; border:1px solid #1e2236; padding:1rem 1.25rem; border-radius:8px;">
                    <div style="font-family:'Manrope',sans-serif; font-size:0.78rem; color:#6a7a96; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:0.4rem; font-weight:700;">SIGNATURE CHECK</div>
                    <div style="font-size:0.85rem; margin-top:0.1rem;">
                        <span style="color:#00e5a0; font-family:'Manrope',sans-serif; font-size:0.9rem; font-weight:800; background:rgba(0,229,160,0.1); padding:0.2em 0.75em; border-radius:5px; border:1px solid rgba(0,229,160,0.3);">● ENABLED</span>
                    </div>
                </div>
                <div style="background:#13151f; border:1px solid #1e2236; padding:1rem 1.25rem; border-radius:8px;">
                    <div style="font-family:'Manrope',sans-serif; font-size:0.78rem; color:#6a7a96; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:0.4rem; font-weight:700;">EXPIRY DATES</div>
                    <div style="font-size:0.85rem; margin-top:0.1rem;">
                        <span style="color:#00e5a0; font-family:'Manrope',sans-serif; font-size:0.9rem; font-weight:800; background:rgba(0,229,160,0.1); padding:0.2em 0.75em; border-radius:5px; border:1px solid rgba(0,229,160,0.3);">● ENABLED</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Drop PDF files here or click to browse",
            type="pdf",
            accept_multiple_files=True,
            label_visibility="visible"
        )

        if uploaded_files:
            for file in uploaded_files:
                size_kb = round(file.size / 1024, 1)
                st.success(f"✓  {file.name}  ·  {size_kb} KB  ·  Queued for scanning")

    with col_b:
        st.markdown("""
        <div style="background:#0e1018; border:1px solid #1e2236; padding:2rem; border-radius:10px;">
            <div style="font-family:'Syne',sans-serif; font-size:1rem; letter-spacing:0.06em; color:#c8d4e8; text-transform:uppercase; margin-bottom:1.5rem; font-weight:800;">
                Scan Queue Status
            </div>
            <div style="display:flex; flex-direction:column; gap:0;">
                <div style="display:flex; justify-content:space-between; align-items:center; padding:1rem 0; border-bottom:1px solid #1a2030;">
                    <span style="font-size:1rem; color:#f0f4ff; font-family:'Manrope',sans-serif; font-weight:700;">HR_Policy_2024.pdf</span>
                    <span style="font-family:'Manrope',monospace; font-size:0.82rem; color:#00e5a0; background:rgba(0,229,160,0.1); padding:0.28em 0.85em; border-radius:5px; border:1px solid rgba(0,229,160,0.3); font-weight:800;">DONE</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:1rem 0; border-bottom:1px solid #1a2030;">
                    <span style="font-size:1rem; color:#f0f4ff; font-family:'Manrope',sans-serif; font-weight:700;">Q4_Financial.pdf</span>
                    <span style="font-family:'Manrope',monospace; font-size:0.82rem; color:#00f5ff; background:rgba(0,245,255,0.08); padding:0.28em 0.85em; border-radius:5px; border:1px solid rgba(0,245,255,0.25); font-weight:800;">SCANNING</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:1rem 0; border-bottom:1px solid #1a2030;">
                    <span style="font-size:1rem; color:#7a869e; font-family:'Manrope',sans-serif; font-weight:600;">Contracts_Batch.pdf</span>
                    <span style="font-family:'Manrope',monospace; font-size:0.82rem; color:#4a5a72; background:rgba(58,66,89,0.2); padding:0.28em 0.85em; border-radius:5px; border:1px solid rgba(58,66,89,0.35); font-weight:700;">QUEUED</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:1rem 0;">
                    <span style="font-size:1rem; color:#7a869e; font-family:'Manrope',sans-serif; font-weight:600;">Legal_Archive_v2.pdf</span>
                    <span style="font-family:'Manrope',monospace; font-size:0.82rem; color:#4a5a72; background:rgba(58,66,89,0.2); padding:0.28em 0.85em; border-radius:5px; border:1px solid rgba(58,66,89,0.35); font-weight:700;">QUEUED</span>
                </div>
            </div>
            <div style="margin-top:1.75rem; padding-top:1.25rem; border-top:1px solid #1a2030;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                    <div style="font-family:'Manrope',sans-serif; font-size:0.85rem; color:#9aabbe; letter-spacing:0.05em; text-transform:uppercase; font-weight:800;">PROCESSING RATE</div>
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.88rem; color:#00f5ff; font-weight:700;">2 / 4 complete</div>
                </div>
                <div style="background:#1a2030; border-radius:4px; height:7px; overflow:hidden;">
                    <div style="background:linear-gradient(90deg, #00f5ff, #a855f7); width:62%; height:100%; border-radius:4px; box-shadow:0 0 12px rgba(0,245,255,0.4);"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 3: Violations
# ══════════════════════════════════════════
with tab_violations:
    st.markdown('<div class="section-title">Violation Log</div>', unsafe_allow_html=True)

    violation_log = pd.DataFrame({
        "Document":       ["Policy_v1.pdf", "Financial_Report.pdf", "User_Data.pdf", "Contract_2024.pdf", "Ops_Manual.pdf"],
        "Violation Type": ["Missing Signature", "Expired Date", "PII Leak", "Unauthorized Access", "Outdated Template"],
        "Department":     ["HR", "Finance", "IT", "Legal", "Operations"],
        "Severity":       ["Medium", "High", "Critical", "High", "Low"],
        "Status":         ["Open", "Under Review", "Open", "Resolved", "Open"],
        "Detected":       ["2024-01-08", "2024-01-12", "2024-01-15", "2024-01-10", "2024-01-17"]
    })

    filter_col, status_col, _ = st.columns([2, 2, 3])
    with filter_col:
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=["Critical", "High", "Medium", "Low"],
            default=["Critical", "High"],
        )
    with status_col:
        status_filter = st.multiselect(
            "Filter by Status",
            options=["Open", "Under Review", "Resolved"],
            default=["Open", "Under Review"],
        )

    filtered_df = violation_log[
        violation_log["Severity"].isin(severity_filter) &
        violation_log["Status"].isin(status_filter)
    ]

    badge_map = {
        'Critical': 'badge-critical',
        'High':     'badge-high',
        'Medium':   'badge-medium',
        'Low':      'badge-low'
    }
    status_color = {
        'Open':         '#ff4d6d',
        'Under Review': '#fbbf24',
        'Resolved':     '#00e5a0'
    }

    rows_html = ""
    for _, row in filtered_df.iterrows():
        sev_cls = badge_map.get(row['Severity'], '')
        s_color = status_color.get(row['Status'], '#7a869e')
        rows_html += f"""
        <tr style="border-bottom:1px solid #1a2030; transition:background 0.15s;" onmouseover="this.style.background='rgba(0,245,255,0.025)'" onmouseout="this.style.background='transparent'">
            <td style="padding:1.1rem 1.4rem; color:#f0f4ff; font-size:0.97rem; font-family:'Manrope',sans-serif; font-weight:700;">{row['Document']}</td>
            <td style="padding:1.1rem 1.4rem; color:#c0cfe0; font-size:0.95rem; font-family:'Manrope',sans-serif; font-weight:500;">{row['Violation Type']}</td>
            <td style="padding:1.1rem 1.4rem; color:#c0cfe0; font-size:0.95rem; font-family:'Manrope',sans-serif; font-weight:500;">{row['Department']}</td>
            <td style="padding:1.1rem 1.4rem;"><span class="badge {sev_cls}">{row['Severity']}</span></td>
            <td style="padding:1.1rem 1.4rem; font-family:'Manrope',sans-serif; font-size:0.92rem; color:{s_color}; font-weight:800;">● {row['Status']}</td>
            <td style="padding:1.1rem 1.4rem; color:#6a7a96; font-family:'IBM Plex Mono',monospace; font-size:0.88rem; font-weight:500;">{row['Detected']}</td>
        </tr>"""

    table_html = f"""
    <div style="background:#0e1018; border:1px solid #1e2236; border-radius:10px; overflow:hidden; margin-top:0.75rem;">
        <table style="width:100%; border-collapse:collapse;">
            <thead>
                <tr style="background:#0a0c14; border-bottom:2px solid #1e2236;">
                    <th style="padding:1rem 1.4rem; text-align:left; font-family:'Manrope',sans-serif; font-size:0.82rem; letter-spacing:0.06em; color:#7a8faa; text-transform:uppercase; font-weight:800;">Document</th>
                    <th style="padding:1rem 1.4rem; text-align:left; font-family:'Manrope',sans-serif; font-size:0.82rem; letter-spacing:0.06em; color:#7a8faa; text-transform:uppercase; font-weight:800;">Violation</th>
                    <th style="padding:1rem 1.4rem; text-align:left; font-family:'Manrope',sans-serif; font-size:0.82rem; letter-spacing:0.06em; color:#7a8faa; text-transform:uppercase; font-weight:800;">Dept</th>
                    <th style="padding:1rem 1.4rem; text-align:left; font-family:'Manrope',sans-serif; font-size:0.82rem; letter-spacing:0.06em; color:#7a8faa; text-transform:uppercase; font-weight:800;">Severity</th>
                    <th style="padding:1rem 1.4rem; text-align:left; font-family:'Manrope',sans-serif; font-size:0.82rem; letter-spacing:0.06em; color:#7a8faa; text-transform:uppercase; font-weight:800;">Status</th>
                    <th style="padding:1rem 1.4rem; text-align:left; font-family:'Manrope',sans-serif; font-size:0.82rem; letter-spacing:0.06em; color:#7a8faa; text-transform:uppercase; font-weight:800;">Detected</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div style="padding:0.9rem 1.4rem; border-top:1px solid #1a2030; font-family:'Manrope',sans-serif; font-size:0.85rem; color:#5a6a82; font-weight:600;">
            {len(filtered_df)} records · filtered from {len(violation_log)} total
        </div>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)