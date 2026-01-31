"""
Authentication module for admin login (Streamlit Cloud safe)
"""
import streamlit as st
import hashlib


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def get_admin_credentials():
    """Load admin credentials from Streamlit secrets (read-only)"""
    try:
        username = st.secrets["admin"]["username"]
        password_hash = st.secrets["admin"]["password_hash"]
        return username, password_hash
    except KeyError:
        # Fail fast with clear message
        st.error("❌ Admin credentials not found in Streamlit Secrets")
        st.stop()


def check_login(username: str, password: str) -> bool:
    """Check login credentials"""
    stored_username, stored_password_hash = get_admin_credentials()
    return (
        username == stored_username
        and hash_password(password) == stored_password_hash
    )


def render_login_page():
    """Render the login page"""
    st.markdown('<h1 class="main-header">Course Data Management System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage your curriculum data efficiently and securely</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
            <div style="text-align: center;">
                <h3>Admin Login</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("admin_login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

        if submitted:
            if check_login(username, password):
                st.session_state.admin_logged_in = True
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
