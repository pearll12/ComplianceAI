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

# --- Custom CSS: Dark Industrial / Refined Security Theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-base:        #0a0c10;
        --bg-panel:       #111318;
        --bg-card:        #181c24;
        --bg-card-hover:  #1e2330;
        --border:         #252b38;
        --border-bright:  #2e3748;
        --accent-cyan:    #00d4ff;
        --accent-amber:   #f59e0b;
        --accent-red:     #ef4444;
        --accent-green:   #22c55e;
        --text-primary:   #e8edf5;
        --text-secondary: #6b7b96;
        --text-muted:     #3d4a5c;
        --font-mono:      'Space Mono', monospace;
        --font-sans:      'DM Sans', sans-serif;
    }

    /* ── Global Reset ── */
    .stApp { background: var(--bg-base); font-family: var(--font-sans); }
    .main .block-container { padding: 2rem 3rem; max-width: 1400px; }
    html, body, [class*="css"] { color: var(--text-primary); }

    /* ── Header Banner ── */
    .dash-header {
        background: linear-gradient(135deg, #0d1117 0%, #111827 50%, #0d1117 100%);
        border: 1px solid var(--border-bright);
        border-left: 4px solid var(--accent-cyan);
        padding: 2rem 2.5rem 1.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border-radius: 2px;
    }
    .dash-header::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(0,212,255,0.06) 0%, transparent 70%);
    }
    .dash-header h1 {
        font-family: var(--font-mono);
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: var(--text-primary);
        margin: 0 0 0.25rem;
    }
    .dash-header p {
        font-family: var(--font-sans);
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin: 0;
        letter-spacing: 0.03em;
    }
    .dash-header .status-pill {
        display: inline-block;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.3);
        color: #22c55e;
        font-family: var(--font-mono);
        font-size: 0.7rem;
        padding: 0.2em 0.7em;
        border-radius: 2px;
        margin-top: 0.75rem;
        letter-spacing: 0.1em;
    }

    /* ── KPI Cards ── */
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-top: 2px solid transparent;
        padding: 1.25rem 1.5rem;
        border-radius: 2px;
        position: relative;
        transition: border-color 0.2s;
    }
    .kpi-card.cyan  { border-top-color: var(--accent-cyan); }
    .kpi-card.amber { border-top-color: var(--accent-amber); }
    .kpi-card.red   { border-top-color: var(--accent-red); }
    .kpi-card.green { border-top-color: var(--accent-green); }
    .kpi-label {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        letter-spacing: 0.12em;
        color: var(--text-secondary);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: var(--font-mono);
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1;
        color: var(--text-primary);
    }
    .kpi-delta {
        font-family: var(--font-sans);
        font-size: 0.75rem;
        margin-top: 0.4rem;
        font-weight: 500;
    }
    .kpi-delta.up   { color: var(--accent-green); }
    .kpi-delta.down { color: var(--accent-red); }
    .kpi-delta.inv-down { color: var(--accent-green); }

    /* ── Section Headers ── */
    .section-title {
        font-family: var(--font-mono);
        font-size: 0.75rem;
        letter-spacing: 0.15em;
        color: var(--text-secondary);
        text-transform: uppercase;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.5rem;
        margin-bottom: 1.25rem;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 0;
        border-bottom: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        font-family: var(--font-mono) !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.08em;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        padding: 0.75rem 1.25rem !important;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-cyan) !important;
        border-bottom-color: var(--accent-cyan) !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

    /* ── Severity Badges ── */
    .badge {
        display: inline-block;
        font-family: var(--font-mono);
        font-size: 0.65rem;
        letter-spacing: 0.08em;
        padding: 0.2em 0.6em;
        border-radius: 2px;
        font-weight: 700;
    }
    .badge-critical { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
    .badge-high     { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
    .badge-medium   { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); }
    .badge-low      { background: rgba(34,197,94,0.15);  color: #22c55e; border: 1px solid rgba(34,197,94,0.3); }

    /* ── Upload Zone ── */
    .upload-zone {
        border: 2px dashed var(--border-bright);
        background: var(--bg-card);
        border-radius: 4px;
        padding: 3rem 2rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .upload-icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .upload-title {
        font-family: var(--font-mono);
        font-size: 0.9rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .upload-sub { color: var(--text-secondary); font-size: 0.8rem; }

    /* ── Plotly chart bg overrides ── */
    .js-plotly-plot .plotly .bg { fill: transparent !important; }

    /* ── Streamlit element overrides ── */
    .stMetric { display: none; }
    div[data-testid="stFileUploader"] {
        border: 2px dashed var(--border-bright) !important;
        background: var(--bg-card) !important;
        border-radius: 4px !important;
        padding: 1.5rem !important;
    }
    div[data-testid="stFileUploader"] * { color: var(--text-secondary) !important; }
    div[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 2px; }
    .stDataFrame * { font-family: var(--font-sans) !important; color: var(--text-primary) !important; background: var(--bg-card) !important; }
    div[data-testid="stAlert"] {
        background: rgba(0,212,255,0.05) !important;
        border: 1px solid rgba(0,212,255,0.2) !important;
        color: var(--text-secondary) !important;
        border-radius: 2px !important;
    }
    .stMultiSelect > div { background: var(--bg-card) !important; border: 1px solid var(--border-bright) !important; border-radius: 2px !important; }
    .stMultiSelect span { font-family: var(--font-mono) !important; font-size: 0.75rem !important; }

    /* Success file upload pills */
    div[data-testid="stSuccessMessage"] {
        background: rgba(34,197,94,0.08) !important;
        border: 1px solid rgba(34,197,94,0.25) !important;
        color: #22c55e !important;
        border-radius: 2px !important;
        font-family: var(--font-mono) !important;
        font-size: 0.75rem !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="dash-header">
    <h1>⬡ PDF COMPLIANCE TRACKER</h1>
    <p>Automated document scanning · Violation detection · Audit trail</p>
    <div class="status-pill">● SYSTEM OPERATIONAL</div>
</div>
""", unsafe_allow_html=True)

# --- KPI Cards ---
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card cyan">
        <div class="kpi-label">PDFs Processed</div>
        <div class="kpi-value">128</div>
        <div class="kpi-delta up">↑ +12% from last period</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Active Violations</div>
        <div class="kpi-value">30</div>
        <div class="kpi-delta inv-down">↓ −5% improvement</div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-label">Under Review</div>
        <div class="kpi-value">8</div>
        <div class="kpi-delta up">↑ 3 new this week</div>
    </div>
    <div class="kpi-card green">
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
                colorscale=[[0, '#1a2535'], [0.4, '#1e3a5f'], [0.7, '#0ea5e9'], [1.0, '#00d4ff']],
                line=dict(width=0)
            )
        ))
        fig_bar.add_trace(go.Bar(
            x=dept_data['Department'], y=dept_data['Resolved'],
            name='Resolved',
            marker=dict(color='rgba(34,197,94,0.35)', line=dict(width=0))
        ))
        fig_bar.update_layout(
            title=dict(text='Violations by Department', font=dict(family='Space Mono', size=12, color='#6b7b96'), x=0),
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', color='#6b7b96', size=11),
            xaxis=dict(gridcolor='#1a2030', linecolor='#252b38', tickfont=dict(color='#6b7b96')),
            yaxis=dict(gridcolor='#1a2030', linecolor='rgba(0,0,0,0)', tickfont=dict(color='#6b7b96')),
            legend=dict(font=dict(family='Space Mono', size=10, color='#6b7b96'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=40, b=10, l=10, r=10),
            height=310,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        sev_data = pd.DataFrame({
            'Severity': ['Critical', 'High', 'Medium', 'Low'],
            'Count':    [4, 11, 9, 6]
        })
        colors = ['#ef4444', '#f59e0b', '#818cf8', '#22c55e']
        fig_donut = go.Figure(go.Pie(
            labels=sev_data['Severity'], values=sev_data['Count'],
            hole=0.65,
            marker=dict(colors=colors, line=dict(color='#0a0c10', width=3)),
            textfont=dict(family='Space Mono', size=10, color='#6b7b96'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
        ))
        fig_donut.add_annotation(
            text='<b>30</b><br><span style="font-size:10px">VIOLATIONS</span>',
            x=0.5, y=0.5, showarrow=False,
            font=dict(family='Space Mono', size=14, color='#e8edf5'), align='center'
        )
        fig_donut.update_layout(
            title=dict(text='Severity Distribution', font=dict(family='Space Mono', size=12, color='#6b7b96'), x=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(font=dict(family='Space Mono', size=10, color='#6b7b96'), bgcolor='rgba(0,0,0,0)', orientation='h', y=-0.1),
            margin=dict(t=40, b=10, l=10, r=10),
            height=310,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Trend line
    st.markdown('<div class="section-title" style="margin-top:1rem;">Monthly Violation Trend</div>', unsafe_allow_html=True)
    months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
    trend_vals = [42, 38, 35, 44, 31, 27, 30]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=months, y=trend_vals, mode='lines+markers',
        line=dict(color='#00d4ff', width=2),
        marker=dict(size=6, color='#00d4ff', symbol='circle',
                    line=dict(color='#0a0c10', width=2)),
        fill='tozeroy',
        fillcolor='rgba(0,212,255,0.05)',
        name='Violations'
    ))
    fig_line.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#6b7b96', size=11),
        xaxis=dict(gridcolor='#1a2030', linecolor='#252b38', tickfont=dict(color='#6b7b96')),
        yaxis=dict(gridcolor='#1a2030', linecolor='rgba(0,0,0,0)', tickfont=dict(color='#6b7b96')),
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        height=180,
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
        <div style="background:#111318; border:1px solid #252b38; padding:1.5rem; border-radius:2px; margin-bottom:1rem;">
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.12em; color:#6b7b96; text-transform:uppercase; margin-bottom:1rem;">
                Scan Configuration
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div style="background:#181c24; border:1px solid #252b38; padding:0.75rem 1rem; border-radius:2px;">
                    <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#6b7b96; letter-spacing:0.1em;">CHECK TYPE</div>
                    <div style="font-family:'DM Sans',sans-serif; color:#e8edf5; font-size:0.85rem; margin-top:0.3rem;">Full Compliance Scan</div>
                </div>
                <div style="background:#181c24; border:1px solid #252b38; padding:0.75rem 1rem; border-radius:2px;">
                    <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#6b7b96; letter-spacing:0.1em;">PII DETECTION</div>
                    <div style="font-size:0.85rem; margin-top:0.3rem;">
                        <span style="color:#22c55e; font-family:'Space Mono',monospace; font-size:0.75rem;">● ENABLED</span>
                    </div>
                </div>
                <div style="background:#181c24; border:1px solid #252b38; padding:0.75rem 1rem; border-radius:2px;">
                    <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#6b7b96; letter-spacing:0.1em;">SIGNATURE CHECK</div>
                    <div style="font-size:0.85rem; margin-top:0.3rem;">
                        <span style="color:#22c55e; font-family:'Space Mono',monospace; font-size:0.75rem;">● ENABLED</span>
                    </div>
                </div>
                <div style="background:#181c24; border:1px solid #252b38; padding:0.75rem 1rem; border-radius:2px;">
                    <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#6b7b96; letter-spacing:0.1em;">EXPIRY DATES</div>
                    <div style="font-size:0.85rem; margin-top:0.3rem;">
                        <span style="color:#22c55e; font-family:'Space Mono',monospace; font-size:0.75rem;">● ENABLED</span>
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
        <div style="background:#111318; border:1px solid #252b38; padding:1.5rem; border-radius:2px; height:100%;">
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.12em; color:#6b7b96; text-transform:uppercase; margin-bottom:1rem;">
                Scan Queue Status
            </div>
            <div style="display:flex; flex-direction:column; gap:0.6rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid #1a2030;">
                    <span style="font-size:0.8rem; color:#e8edf5;">HR_Policy_2024.pdf</span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#22c55e; background:rgba(34,197,94,0.1); padding:0.15em 0.5em; border-radius:2px;">DONE</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid #1a2030;">
                    <span style="font-size:0.8rem; color:#e8edf5;">Q4_Financial.pdf</span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#00d4ff; background:rgba(0,212,255,0.1); padding:0.15em 0.5em; border-radius:2px;">SCANNING</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid #1a2030;">
                    <span style="font-size:0.8rem; color:#6b7b96;">Contracts_Batch.pdf</span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3d4a5c; background:rgba(61,74,92,0.2); padding:0.15em 0.5em; border-radius:2px;">QUEUED</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0;">
                    <span style="font-size:0.8rem; color:#6b7b96;">Legal_Archive_v2.pdf</span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3d4a5c; background:rgba(61,74,92,0.2); padding:0.15em 0.5em; border-radius:2px;">QUEUED</span>
                </div>
            </div>
            <div style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid #1a2030;">
                <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#6b7b96; letter-spacing:0.1em; margin-bottom:0.5rem;">PROCESSING RATE</div>
                <div style="background:#1a2030; border-radius:2px; height:4px; overflow:hidden;">
                    <div style="background:linear-gradient(90deg, #00d4ff, #0ea5e9); width:62%; height:100%; border-radius:2px;"></div>
                </div>
                <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#00d4ff; margin-top:0.4rem;">2 / 4 complete</div>
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

    # Styled HTML table
    badge_map = {
        'Critical': 'badge-critical',
        'High':     'badge-high',
        'Medium':   'badge-medium',
        'Low':      'badge-low'
    }
    status_color = {
        'Open':         '#ef4444',
        'Under Review': '#f59e0b',
        'Resolved':     '#22c55e'
    }

    rows_html = ""
    for _, row in filtered_df.iterrows():
        sev_cls = badge_map.get(row['Severity'], '')
        s_color = status_color.get(row['Status'], '#6b7b96')
        rows_html += f"""
        <tr style="border-bottom:1px solid #1a2030;">
            <td style="padding:0.85rem 1rem; color:#e8edf5; font-size:0.82rem;">{row['Document']}</td>
            <td style="padding:0.85rem 1rem; color:#6b7b96; font-size:0.82rem;">{row['Violation Type']}</td>
            <td style="padding:0.85rem 1rem; color:#6b7b96; font-size:0.82rem;">{row['Department']}</td>
            <td style="padding:0.85rem 1rem;"><span class="badge {sev_cls}">{row['Severity']}</span></td>
            <td style="padding:0.85rem 1rem; font-family:'Space Mono',monospace; font-size:0.7rem; color:{s_color};">● {row['Status']}</td>
            <td style="padding:0.85rem 1rem; color:#3d4a5c; font-family:'Space Mono',monospace; font-size:0.7rem;">{row['Detected']}</td>
        </tr>"""

    table_html = f"""
    <div style="background:#111318; border:1px solid #252b38; border-radius:2px; overflow:hidden; margin-top:0.5rem;">
        <table style="width:100%; border-collapse:collapse;">
            <thead>
                <tr style="background:#0d1117; border-bottom:1px solid #252b38;">
                    <th style="padding:0.75rem 1rem; text-align:left; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; color:#3d4a5c; text-transform:uppercase;">Document</th>
                    <th style="padding:0.75rem 1rem; text-align:left; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; color:#3d4a5c; text-transform:uppercase;">Violation</th>
                    <th style="padding:0.75rem 1rem; text-align:left; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; color:#3d4a5c; text-transform:uppercase;">Dept</th>
                    <th style="padding:0.75rem 1rem; text-align:left; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; color:#3d4a5c; text-transform:uppercase;">Severity</th>
                    <th style="padding:0.75rem 1rem; text-align:left; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; color:#3d4a5c; text-transform:uppercase;">Status</th>
                    <th style="padding:0.75rem 1rem; text-align:left; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; color:#3d4a5c; text-transform:uppercase;">Detected</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div style="padding:0.6rem 1rem; border-top:1px solid #1a2030; font-family:'Space Mono',monospace; font-size:0.65rem; color:#3d4a5c;">
            {len(filtered_df)} records · filtered from {len(violation_log)} total
        </div>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)