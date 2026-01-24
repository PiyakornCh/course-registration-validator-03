"""Admin panel component for course data management."""
import streamlit as st


def display_admin_panel():
    """Display admin panel."""
    from components.admin_auth import render_login_page
    from components.admin_upload import render_upload_page
    from components.admin_manage import render_manage_page
    
    # Custom CSS for admin panel
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)
    
    # Check if logged in
    if not st.session_state.admin_logged_in:
        render_login_page()
        
        # Add back button
        if st.button("← Back to Main App"):
            st.session_state.admin_mode = False
            st.rerun()
    else:
        # Admin panel after login
        st.title("Course Data Management System")
        
        # Sidebar menu
        with st.sidebar:
            st.header("📋 Menu")
            menu = st.radio(
                "Select Page",
                ["📤 Upload Data", "📂 Manage Curriculums"],
                key="admin_menu"
            )
            
            st.markdown("---")
            st.info(f"👤 Logged in as: **admin**")
            
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                st.session_state.admin_logged_in = False
                st.rerun()
            
            if st.button("← Back to Main App", use_container_width=True):
                st.session_state.admin_mode = False
                st.session_state.admin_logged_in = False
                st.rerun()
        
        # Route to appropriate page
        if menu == "📤 Upload Data":
            render_upload_page()
        elif menu == "📂 Manage Curriculums":
            render_manage_page()
