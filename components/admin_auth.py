"""
Authentication module for admin login and password management
"""
import streamlit as st
import hashlib
import os

PASSWORD_FILE = "admin_password.txt"

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_password():
    """Load password from file"""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as f:
            return f.read().strip()
    else:
        # Default password: admin
        default_password = hash_password("admin")
        with open(PASSWORD_FILE, 'w') as f:
            f.write(default_password)
        return default_password

def save_password(password):
    """Save new password"""
    with open(PASSWORD_FILE, 'w') as f:
        f.write(hash_password(password))

def check_login(username, password):
    """Check login credentials"""
    stored_password = load_password()
    return username == "admin" and hash_password(password) == stored_password

def render_login_page():
    """Render the login page"""
    # Hero Section
    st.markdown('<h1 class="main-header">Course Data Management System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage your curriculum data efficiently and securely</p>', unsafe_allow_html=True)
    
    # Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Admin Login")
        
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Login", use_container_width=True, type="primary"):
                if check_login(username, password):
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        with col_btn2:
            if st.button("🔑 Change Password", use_container_width=True):
                st.session_state.show_change_password = True
        
        # Change Password Section
        if st.session_state.show_change_password:
            st.markdown("---")
            st.subheader("Change Password")
            
            old_password = st.text_input("Current Password", type="password", key="old_pass")
            new_password = st.text_input("New Password", type="password", key="new_pass")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pass")
            
            if st.button("✅ Confirm Change", use_container_width=True, type="primary"):
                if hash_password(old_password) != load_password():
                    st.error("❌ Current password is incorrect")
                elif new_password != confirm_password:
                    st.error("❌ New passwords do not match")
                elif len(new_password) < 4:
                    st.error("❌ Password must be at least 4 characters")
                else:
                    save_password(new_password)
                    st.success("✅ Password changed successfully!")
                    st.session_state.show_change_password = False
                    st.rerun()
