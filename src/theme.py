"""
EV Battery Health Prediction
Premium Streamlit Theme

Central UI styling for the application.
"""

import html
import textwrap
import streamlit as st


def _html(content: str) -> str:
    """Flatten an HTML string so Streamlit's Markdown pass can never
    mistake any of it for a preformatted code block.

    Two separate Markdown rules matter here:
    1. Any line indented 4+ spaces is treated as an indented code block.
    2. A raw HTML block (recognized because a line starts with a tag at
       column 0) is TERMINATED by the next blank line — after which
       normal Markdown parsing resumes for whatever follows.

    Our HTML is written with blank lines between tags for readability,
    so textwrap.dedent()+strip() alone isn't enough: it only removes
    the *common* margin, but anything after an internal blank line
    still has leftover indentation and gets swallowed by rule 1.

    The reliable fix is to strip leading whitespace from every
    individual line (not just the shared minimum), so no line can
    ever qualify as indented, regardless of where blank lines fall.
    """
    lines = [line.strip() for line in content.split("\n")]
    return "\n".join(lines).strip()


# ============================================================
# COLOR SYSTEM
# ============================================================

BG = "#07111F"
BG_2 = "#0A1626"

PANEL = "#0E1B2B"
PANEL_2 = "#12243A"

BORDER = "rgba(255, 255, 255, 0.09)"
PANEL_BORDER = BORDER

TEXT = "#F8FAFC"
TEXT_SOFT = "#CBD5E1"
TEXT_MUTED = "#8FA3B8"

ACCENT = "#19D3AE"
ACCENT_BLUE = "#38BDF8"
ACCENT_PURPLE = "#8B7CFF"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"

PLOTLY_TEMPLATE = "plotly_dark"


# ============================================================
# PREMIUM CSS
# ============================================================

def inject_css():
    """
    Apply the complete premium EV analytics theme.
    Call once near the beginning of app.py.
    """

    st.markdown(_html(f"""
        <style>

        /* ====================================================
           APP BACKGROUND
           ==================================================== */

        .stApp {{
            background:
                radial-gradient(
                    circle at 0% 0%,
                    rgba(56, 189, 248, 0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 100% 0%,
                    rgba(139, 124, 255, 0.10),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    {BG} 0%,
                    {BG_2} 50%,
                    #050D17 100%
                );

            color: {TEXT};
        }}

        .main .block-container {{
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }}


        /* ====================================================
           HEADINGS
           ==================================================== */

        h1, h2, h3, h4 {{
            color: {TEXT} !important;
            font-weight: 700 !important;
        }}

        h1 {{
            letter-spacing: -0.035em;
        }}

        p {{
            color: {TEXT_SOFT};
        }}


        /* ====================================================
           SIDEBAR
           ==================================================== */

        section[data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    #081321 0%,
                    #0A1727 55%,
                    #06101C 100%
                );

            border-right:
                1px solid {BORDER};
        }}

        section[data-testid="stSidebar"] > div {{
            padding-top: 1.5rem;
        }}

        section[data-testid="stSidebar"] hr {{
            border-color:
                rgba(255,255,255,0.07);
        }}


        /* ====================================================
           BUTTONS
           ==================================================== */

        div.stButton > button {{
            width: 100%;

            min-height: 44px;

            border-radius: 12px;

            border:
                1px solid rgba(255,255,255,0.08);

            background:
                linear-gradient(
                    135deg,
                    {ACCENT},
                    #0EA5A0
                );

            color: #031514;

            font-weight: 750;

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }}

        div.stButton > button:hover {{
            transform: translateY(-2px);

            box-shadow:
                0 10px 30px rgba(25,211,174,0.22);

            color: #031514;
        }}

        div.stButton > button:active {{
            transform: translateY(0);
        }}


        /* ====================================================
           DOWNLOAD BUTTON
           ==================================================== */

        div.stDownloadButton > button {{
            width: 100%;

            min-height: 44px;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    #13283D,
                    #0C1A2B
                );

            color: {TEXT};

            border:
                1px solid rgba(255,255,255,0.10);

            font-weight: 650;
        }}

        div.stDownloadButton > button:hover {{
            border-color:
                rgba(25,211,174,0.45);

            color: #ffffff;
        }}


        /* ====================================================
           INPUTS
           ==================================================== */

        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {{
            background:
                rgba(5,15,27,0.90) !important;

            color:
                #FFFFFF !important;

            border:
                1px solid rgba(255,255,255,0.10) !important;

            border-radius:
                12px !important;
        }}

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stTextArea textarea:focus {{
            border-color:
                {ACCENT_BLUE} !important;

            box-shadow:
                0 0 0 1px
                rgba(56,189,248,0.20) !important;
        }}


        /* ====================================================
           SELECT BOX
           ==================================================== */

        div[data-baseweb="select"] > div {{
            background:
                rgba(5,15,27,0.90);

            border:
                1px solid rgba(255,255,255,0.10);

            border-radius:
                12px;
        }}


        /* ====================================================
           KPI CARDS
           ==================================================== */

        .ev-kpi {{
            position: relative;

            overflow: hidden;

            min-height: 145px;

            padding: 1.25rem;

            border-radius: 18px;

            border:
                1px solid rgba(255,255,255,0.09);

            background:
                linear-gradient(
                    145deg,
                    rgba(18,36,58,0.98),
                    rgba(7,18,31,0.98)
                );

            box-shadow:
                0 14px 40px rgba(0,0,0,0.24);

            transition:
                transform 0.18s ease,
                border-color 0.18s ease;
        }}

        .ev-kpi:hover {{
            transform: translateY(-3px);

            border-color:
                rgba(25,211,174,0.30);
        }}

        .ev-kpi::before {{
            content: "";

            position: absolute;

            top: 0;
            left: 0;

            width: 100%;
            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    {ACCENT},
                    {ACCENT_BLUE},
                    {ACCENT_PURPLE}
                );
        }}

        .ev-kpi-label {{
            color: {TEXT_MUTED};

            font-size: 0.76rem;

            font-weight: 650;

            text-transform: uppercase;

            letter-spacing: 0.08em;

            margin-bottom: 0.55rem;
        }}

        .ev-kpi-value {{
            color: {TEXT};

            font-size: 2rem;

            font-weight: 800;

            line-height: 1.15;
        }}

        .ev-kpi-sub {{
            color: {TEXT_SOFT};

            font-size: 0.82rem;

            margin-top: 0.55rem;
        }}


        /* ====================================================
           NORMAL CARD
           ==================================================== */

        .ev-card {{
            background:
                linear-gradient(
                    145deg,
                    rgba(18,36,58,0.95),
                    rgba(7,18,31,0.95)
                );

            border:
                1px solid rgba(255,255,255,0.09);

            border-radius: 18px;

            padding: 1.3rem;

            margin-bottom: 1rem;

            box-shadow:
                0 12px 35px rgba(0,0,0,0.20);
        }}

        .ev-card-title {{
            color: {TEXT};

            font-size: 1.05rem;

            font-weight: 700;

            margin-bottom: 0.8rem;
        }}


        /* ====================================================
           METRIC
           ==================================================== */

        div[data-testid="stMetric"] {{
            background:
                linear-gradient(
                    145deg,
                    rgba(18,36,58,0.95),
                    rgba(7,18,31,0.95)
                );

            border:
                1px solid rgba(255,255,255,0.08);

            border-radius: 16px;

            padding: 1rem;

            box-shadow:
                0 10px 30px rgba(0,0,0,0.18);
        }}


        /* ====================================================
           DATAFRAME
           ==================================================== */

        [data-testid="stDataFrame"] {{
            border-radius: 14px;

            overflow: hidden;

            border:
                1px solid rgba(255,255,255,0.08);
        }}


        /* ====================================================
           FILE UPLOADER
           ==================================================== */

        [data-testid="stFileUploader"] {{
            background:
                rgba(8,20,34,0.60);

            border-radius:
                14px;
        }}


        /* ====================================================
           TABS
           ==================================================== */

        button[data-baseweb="tab"] {{
            color:
                {TEXT_MUTED} !important;

            font-weight:
                650 !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color:
                {ACCENT} !important;
        }}


        /* ====================================================
           ALERTS
           ==================================================== */

        .stAlert {{
            border-radius:
                14px;
        }}


        /* ====================================================
           PROGRESS
           ==================================================== */

        div[data-testid="stProgress"] > div > div {{
            background:
                linear-gradient(
                    90deg,
                    {ACCENT},
                    {ACCENT_BLUE}
                );
        }}


        /* ====================================================
           DIVIDER
           ==================================================== */

        hr {{
            border-color:
                rgba(255,255,255,0.07);
        }}


        /* ====================================================
           SCROLLBAR
           ==================================================== */

        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: {BG};
        }}

        ::-webkit-scrollbar-thumb {{
            background: #263A50;
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #35546D;
        }}

        </style>
        """), unsafe_allow_html=True)


# ============================================================
# KPI CARD
# ============================================================

def kpi_card(
    label: str,
    value: str,
    sub: str = "",
    sub_color: str = ACCENT,
):
    """
    Standalone KPI card.

    Important:
    This creates one complete HTML element.
    Do not place it inside card_open/card_close.
    """

    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    safe_sub = html.escape(str(sub))
    safe_color = html.escape(str(sub_color))

    st.markdown(_html(f"""
        <div class="ev-kpi">

            <div class="ev-kpi-label">
                {safe_label}
            </div>

            <div class="ev-kpi-value">
                {safe_value}
            </div>

            <div
                class="ev-kpi-sub"
                style="color:{safe_color};"
            >
                {safe_sub}
            </div>

        </div>
        """), unsafe_allow_html=True)


# ============================================================
# PREMIUM CARD (returns HTML string — used by dashboard.py,
# which renders it itself via st.markdown)
# ============================================================

def premium_card(label: str, value, sub: str = "") -> str:
    """
    Returns (does NOT render) one complete KPI-style HTML card,
    for callers that want to render it themselves, e.g.:
        st.markdown(premium_card("USERS", 12, "Active"), unsafe_allow_html=True)
    """
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    safe_sub = html.escape(str(sub))

    return _html(f"""
        <div class="ev-kpi">
            <div class="ev-kpi-label">
                {safe_label}
            </div>
            <div class="ev-kpi-value">
                {safe_value}
            </div>
            <div class="ev-kpi-sub" style="color:{ACCENT};">
                {safe_sub}
            </div>
        </div>
        """)


def section_header(title: str, subtitle: str = ""):
    """Renders a page-section title + subtitle line."""
    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))

    st.markdown(_html(f"""
        <div style="margin: 0.5rem 0 1rem 0;">
            <h2 style="margin-bottom:0.1rem;">{safe_title}</h2>
            <p style="color:{TEXT_MUTED};margin-top:0;">{safe_subtitle}</p>
        </div>
        """), unsafe_allow_html=True)


# ============================================================
# SIMPLE CARD
# ============================================================

def card(title: str = "", content: str = ""):
    """
    Render one complete HTML card.

    Use this instead of opening and closing HTML
    containers across different Streamlit elements.
    """

    safe_title = html.escape(str(title))
    safe_content = str(content)

    title_html = ""

    if title:
        title_html = f"""
        <div class="ev-card-title">
            {safe_title}
        </div>
        """

    st.markdown(_html(f"""
        <div class="ev-card">
            {title_html}
            {safe_content}
        </div>
        """), unsafe_allow_html=True)


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def card_open(title: str = ""):
    """
    Kept for compatibility with older app code.

    Prefer using card() for new sections.
    """

    if title:
        st.markdown(_html(f"""
            <div class="ev-card">
                <div class="ev-card-title">
                    {html.escape(str(title))}
                </div>
            </div>
            """), unsafe_allow_html=True)


def card_close():
    """
    Kept for compatibility.

    Do not use this to wrap Streamlit widgets.
    """
    pass


# ============================================================
# PLOTLY THEME
# ============================================================

def style_plotly(fig):
    """
    Apply the premium dark analytics style
    to a Plotly figure.
    """

    fig.update_layout(
        template=PLOTLY_TEMPLATE,

        paper_bgcolor=PANEL,

        plot_bgcolor="#091625",

        font=dict(
            color=TEXT,
            family="Arial",
        ),

        margin=dict(
            l=35,
            r=35,
            t=55,
            b=35,
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=TEXT_SOFT
            ),
        ),

        hoverlabel=dict(
            bgcolor=PANEL_2,
            font_color=TEXT,
        ),

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.08)",
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.08)",
        ),
    )

    # Only style the figure-level title font if a figure-level title
    # actually exists (e.g. px.line(title="..."), px.pie(title="...")).
    # Setting title_font with no title.text — which is the case for
    # go.Indicator gauge charts, since those set their OWN title
    # separately from the figure's layout.title — makes Plotly's JS
    # renderer display the literal word "undefined" as the title.
    if fig.layout.title is not None and fig.layout.title.text:
        fig.update_layout(
            title_font=dict(
                color=TEXT,
                size=18,
            ),
        )

    return fig


# ============================================================
# STATUS BADGE
# ============================================================

def status_badge_class(status: str) -> str:
    """
    Return the appropriate CSS class
    for a battery health status.
    """

    status = str(status).lower()

    if (
        "good" in status
        or "excellent" in status
        or "green" in status
        or "🟢" in status
    ):
        return "ev-badge-green"

    if (
        "fair" in status
        or "warning" in status
        or "medium" in status
        or "yellow" in status
        or "🟡" in status
        or "🟠" in status
    ):
        return "ev-badge-amber"

    return "ev-badge-red"