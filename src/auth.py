import hashlib
import os
import textwrap
import streamlit as st


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _get_password(env_var: str, secrets_key: str, default: str) -> str:
    
    try:
        if secrets_key in st.secrets:
            return str(st.secrets[secrets_key])
    except Exception:
        pass  # no secrets.toml present locally — that's fine

    return os.environ.get(env_var, default)


# ------------------------------------------------------------
# User store: username -> {password hash, role, display name}
#
# Passwords are demo defaults ("admin123" / "user123") UNLESS
# overridden via Streamlit secrets or environment variables — see
# _get_password() above. To set real credentials:
#
#   Locally: create .streamlit/secrets.toml (already gitignored) with
#       ADMIN_PASSWORD = "your-real-password"
#       USER_PASSWORD = "your-real-password"
#
#   On Streamlit Community Cloud: App settings -> Secrets -> paste the
#   same two lines.
#
#   Or via a plain environment variable instead of secrets.toml:
#       export ADMIN_PASSWORD="your-real-password"
#
# To generate a hash manually for any other use:
#   python -c "import hashlib; print(hashlib.sha256(b'yourpassword').hexdigest())"
# ------------------------------------------------------------
USERS = {
    "admin": {
        "password_hash": _hash(_get_password("ADMIN_PASSWORD", "ADMIN_PASSWORD", "admin123")),
        "role": "admin",
        "display_name": "Administrator",
    },
    "user": {
        "password_hash": _hash(_get_password("USER_PASSWORD", "USER_PASSWORD", "user123")),
        "role": "user",
        "display_name": "Standard User",
    },
}


def _init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None


def is_logged_in() -> bool:
    _init_session_state()
    return st.session_state["logged_in"]


def is_admin() -> bool:
    return st.session_state.get("role") == "admin"


def current_user() -> str:
    return st.session_state.get("username")


def _attempt_login(username: str, password: str) -> bool:
    user = USERS.get(username)
    if user is None:
        return False
    if user["password_hash"] != _hash(password):
        return False

    st.session_state["logged_in"] = True
    st.session_state["username"] = username
    st.session_state["role"] = user["role"]
    st.session_state["display_name"] = user["display_name"]
    return True


def logout():
    for key in ["logged_in", "username", "role", "display_name"]:
        st.session_state.pop(key, None)
    # Also clear anything from a previous session's prediction state
    for key in ["has_predicted", "prediction", "status", "risk_score", "recommendations"]:
        st.session_state.pop(key, None)


def render_login_form():
    """Renders the branded login screen: hero panel on the left,
    login card on the right. Call this and then st.stop() when
    is_logged_in() is False, before rendering the rest of the app."""

    _init_session_state()

    from src.theme import inject_css, ACCENT, PANEL, PANEL_BORDER, TEXT_MUTED, _html
    inject_css()

    st.markdown(_html(f"""
        <style>
        .ev-hero-title {{
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1.15;
            color: #e5e7eb;
        }}
        .ev-hero-title span {{ color: {ACCENT}; }}
        .ev-hero-tagline {{
            color: {TEXT_MUTED};
            font-size: 1.05rem;
            margin: 0.8rem 0 2rem 0;
        }}
        .ev-feature {{
            background: {PANEL};
            border: 1px solid {PANEL_BORDER};
            border-radius: 12px;
            padding: 0.9rem;
            text-align: center;
            height: 100%;
        }}
        .ev-feature .icon {{ font-size: 1.4rem; }}
        .ev-feature .title {{ font-weight: 700; color: {ACCENT}; font-size: 0.85rem; margin-top: 0.3rem; }}
        .ev-feature .desc {{ color: {TEXT_MUTED}; font-size: 0.75rem; margin-top: 0.2rem; }}
        .ev-login-card {{
            background: {PANEL};
            border: 1px solid {PANEL_BORDER};
            border-radius: 16px;
            padding: 2rem;
        }}
        </style>
        """), unsafe_allow_html=True)

    hero_col, login_col = st.columns([1.2, 1], gap="large")

    with hero_col:
        st.markdown(_html("""
            <div style="padding-top:2rem;">
                <div style="font-size:1rem;">🔋</div>
                <div class="ev-hero-title">EV BATTERY<br>HEALTH PREDICTION<br><span>ANALYTICS SYSTEM</span></div>
                <div class="ev-hero-tagline">Predict. Analyze. Optimize.<br>Empowering the future of electric mobility.</div>
            </div>
            """), unsafe_allow_html=True)
        f1, f2, f3, f4 = st.columns(4)
        features = [
            ("🎯", "Accurate Predictions", "ML models for battery health"),
            ("📊", "Smart Analytics", "Deep insights & visualizations"),
            ("📄", "Detailed Reports", "Professional PDF reports"),
            ("🔒", "Secure & Reliable", "Session-based access control"),
        ]
        for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
            with col:
                st.markdown(_html(f"""
                    <div class="ev-feature">
                        <div class="icon">{icon}</div>
                        <div class="title">{title}</div>
                        <div class="desc">{desc}</div>
                    </div>
                    """), unsafe_allow_html=True)

    with login_col:
        st.markdown('<div class="ev-login-card">', unsafe_allow_html=True)
        st.markdown("### Welcome Back!")
        st.caption("Login to your account")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login →", use_container_width=True)

        if submitted:
            if _attempt_login(username, password):
                st.success(f"Welcome, {st.session_state['display_name']}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

        using_demo_creds = (
            _get_password("ADMIN_PASSWORD", "ADMIN_PASSWORD", "admin123") == "admin123"
            and _get_password("USER_PASSWORD", "USER_PASSWORD", "user123") == "user123"
        )
        if using_demo_creds:
            with st.expander("Demo credentials"):
                st.write("**Admin:** username `admin`, password `admin123`")
                st.write("**User:** username `user`, password `user123`")
        st.markdown("</div>", unsafe_allow_html=True)


def render_logout_sidebar():
    """Call this once the user is logged in. Renders the branded sidebar:
    working page navigation (sets st.session_state['page']) plus who's
    logged in and a logout button."""

    from src.theme import inject_css, ACCENT, _html
    inject_css()

    if "page" not in st.session_state:
        st.session_state["page"] = "dashboard"

    with st.sidebar:
        st.markdown(_html(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1.2rem;">
                <span style="font-size:1.4rem;">🔋</span>
                <span style="font-weight:800;color:{ACCENT};letter-spacing:0.02em;">EV BATTERY ANALYTICS</span>
            </div>
            """), unsafe_allow_html=True)

        nav_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("➕", "New Prediction", "prediction"),
            ("📋", "Prediction History", "history"),
            ("📈", "Analytics", "analytics"),
            ("📁", "Batch Prediction", "batch"),
            ("🧠", "Feature Importance", "importance"),
        ]
        current_page = st.session_state["page"]
        for icon, label, page_key in nav_items:
            is_active = current_page == page_key
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["page"] = page_key
                st.rerun()

        st.markdown("---")
        role_label = "🛠️ Admin" if is_admin() else "👤 User"
        st.write(f"**Logged in as:** {st.session_state.get('display_name')}")
        st.write(f"**Role:** {role_label}")
        if st.button("🚪 Log Out", use_container_width=True):
            logout()
            st.rerun()


def require_login():
    """Call this at the very top of app.py. Shows the login form and
    halts the script if the user isn't authenticated yet."""

    if not is_logged_in():
        render_login_form()
        st.stop()

    render_logout_sidebar()