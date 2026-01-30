"""
Authentication module for admin login and password management
"""
import streamlit as st
import hashlib
import os
import re

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_password():
    """Load password from Streamlit secrets"""
    try:
        # Try to load from secrets.toml
        return st.secrets["admin"]["password_hash"]
    except (KeyError, FileNotFoundError):
        # Fallback: check for legacy password file
        legacy_file = "admin_password.txt"
        if os.path.exists(legacy_file):
            with open(legacy_file, 'r') as f:
                return f.read().strip()
        else:
            # Default password: admin (hashed)
            return hash_password("admin")

def save_password(password):
    """Save new password to secrets.toml"""
    import toml
    
    # Create secrets directory if it doesn't exist
    secrets_dir = ".streamlit"
    if not os.path.exists(secrets_dir):
        os.makedirs(secrets_dir)
    
    secrets_file = os.path.join(secrets_dir, "secrets.toml")
    
    # Load existing secrets or create new structure
    try:
        if os.path.exists(secrets_file):
            with open(secrets_file, 'r') as f:
                secrets = toml.load(f)
        else:
            secrets = {}
    except:
        secrets = {}
    
    # Update admin password
    if "admin" not in secrets:
        secrets["admin"] = {}
    
    secrets["admin"]["password_hash"] = hash_password(password)
    secrets["admin"]["username"] = "admin"
    
    # Write back to file
    with open(secrets_file, 'w') as f:
        toml.dump(secrets, f)

def get_username():
    """Get admin username from secrets"""
    try:
        return st.secrets["admin"]["username"]
    except (KeyError, FileNotFoundError):
        return "admin"  # Default username

def check_login(username, password):
    """Check login credentials"""
    stored_password = load_password()
    stored_username = get_username()
    return username == stored_username and hash_password(password) == stored_password

def validate_password_strength(password):
    """
    Validate password strength
    Requirements:
    - At least 8 characters
    - Contains at least one digit
    - Contains at least one special character
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("• At least 8 characters")
    
    if not re.search(r'[0-9]', password):
        errors.append("• At least one digit (0-9)")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;\'`~]', password):
        errors.append("• At least one special character (!@#$%^&* etc.)")
    
    if not re.search(r'[a-z]', password):
        errors.append("• At least one lowercase letter (a-z)")
    
    if not re.search(r'[A-Z]', password):
        errors.append("• At least one uppercase letter (A-Z)")
    
    if errors:
        return False, errors
    
    return True, []

def render_login_page():
    """Render the login page"""
    # Hero Section
    st.markdown('<h1 class="main-header">Course Data Management System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage your curriculum data efficiently and securely</p>', unsafe_allow_html=True)
    
    # Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Admin Login")
        
        # Create a form to enable Enter key submission
        with st.form(key="login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            with col_btn2:
                change_pass_btn = st.form_submit_button("🔑 Change Password", use_container_width=True)
        
        # Handle login submission
        if login_submitted:
            if check_login(username, password):
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        # Handle change password button
        if change_pass_btn:
            st.session_state.show_change_password = True
        
        # Show success message after password change (outside the form, below login box)
        if 'password_changed_success' in st.session_state and st.session_state.password_changed_success:
            st.success("✅ Password changed successfully!")
            del st.session_state.password_changed_success
        
        # Change Password Section
        if st.session_state.show_change_password:
            st.markdown("---")
            st.subheader("Change Password")
            
            # Track button click state
            button_clicked = False
            
            # Input fields outside form for real-time validation
            old_password = st.text_input("Current Password", type="password", key="old_pass_input")
            
            # Show error for current password after button click
            if 'change_pwd_clicked' in st.session_state and st.session_state.change_pwd_clicked:
                if not old_password:
                    st.error("❌ Please enter current password")
                elif hash_password(old_password) != load_password():
                    st.error("❌ Current password is incorrect")
            
            new_password = st.text_input("New Password", type="password", key="new_pass_input", 
                                        help="Must be at least 8 characters with uppercase, lowercase, digit, and special character")
            
            # Real-time password strength validation
            if new_password:
                is_valid, errors = validate_password_strength(new_password)
                if is_valid:
                    st.success("✅ Password is strong!")
                else:
                    st.error("❌ Password requirements:  \n  \n" + "  \n".join(errors))
            elif 'change_pwd_clicked' in st.session_state and st.session_state.change_pwd_clicked and not new_password:
                st.error("❌ Please enter new password")
            
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pass_input")
            
            # Real-time password match validation
            if confirm_password and new_password:
                # Check if new password meets requirements first
                is_valid, errors = validate_password_strength(new_password)
                if confirm_password != new_password:
                    st.error("❌ New passwords do not match")

            elif 'change_pwd_clicked' in st.session_state and st.session_state.change_pwd_clicked and not confirm_password:
                st.error("❌ Please confirm new password")
            
            # Submit button
            if st.button("✅ Confirm Change", use_container_width=True, type="primary", key="confirm_change_btn"):
                st.session_state.change_pwd_clicked = True
                
                # Validate all fields
                if old_password and new_password and confirm_password:
                    if hash_password(old_password) == load_password():
                        if new_password == confirm_password:
                            # Validate password strength
                            is_valid, errors = validate_password_strength(new_password)
                            if is_valid:
                                save_password(new_password)
                                st.session_state.password_changed_success = True
                                st.session_state.show_change_password = False
                                if 'change_pwd_clicked' in st.session_state:
                                    del st.session_state.change_pwd_clicked
                                st.rerun()
                st.rerun()
                    
