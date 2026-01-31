"""
Admin Home Page - Main dashboard for course data management system
"""
import streamlit as st
import sys
import os

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from components.admin_auth import render_login_page
from components.session_manager import SessionManager

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🏠",
    layout="wide"
)

# Initialize session state FIRST
SessionManager.initialize_session_state()

# Custom CSS for styling
st.markdown("""
<style>
/* Style specifically for multipage navigation only */
div[data-testid="stSidebarNav"] ul li a {
    font-weight: bold !important;
    font-size: 1.1rem !important;
}

/* Alternative selector for page navigation in sidebar */
.css-1544g2n a {
    font-weight: bold !important;
    font-size: 1.1rem !important;
}

/* Reset other elements to normal weight */
.stSelectbox label, .stSelectbox div {
    font-weight: normal !important;
}

/* Admin panel specific styles */
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    padding: 1rem 0;
    margin-bottom: 0.5rem;
    display: inline-block;
    width: 100%;
}
.sub-header {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 1rem;
}
.feature-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 1rem 0;
}
.feature-card h3 {
    margin: 0;
    font-size: 1.5rem;
}
.feature-card p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

def render_admin_dashboard():
    """Render the admin dashboard after login"""

    # Sidebar navigation
    with st.sidebar:
        st.header("📋 Admin Navigation")

        page = st.radio(
            "Select Page",
            ["📤 Upload Data", "📂 Manage Curriculums"],
            key="admin_nav",
            index=1
        )

        st.markdown("---")
        st.info("👤 Logged in as: **admin**")

        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            SessionManager.logout_admin()
            st.switch_page("Home.py")

    # Route to appropriate page
    if page == "📤 Upload Data":
        from components.admin_upload import render_upload_page
        render_upload_page()

    elif page == "📂 Manage Curriculums":
        from components.admin_manage import render_manage_page
        render_manage_page()


if not st.session_state.admin_logged_in:
    render_login_page()
    st.stop()   # important: prevent admin code from running
else:
    render_admin_dashboard()
