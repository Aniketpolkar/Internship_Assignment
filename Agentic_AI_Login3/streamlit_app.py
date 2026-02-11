import streamlit as st
import requests
import re

# Set page configuration
st.set_page_config(page_title="Auth System", page_icon="🔒", layout="centered")

# Backend URL
API_BASE_URL = "http://localhost:8000"

# Custom CSS for modern look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .main {
        background-color: #f8f9fa;
    }
    .auth-container {
        padding: 2rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Login'
if 'email' not in st.session_state:
    st.session_state.email = ''
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def login_page():
    st.title("Welcome Back")
    st.subheader("Login to your account")
    
    with st.container():
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if not email or not password:
                st.error("Please fill in all fields")
                return
            
            try:
                response = requests.post(f"{API_BASE_URL}/login", json={
                    "email": email,
                    "password": password
                })
                
                if response.status_code == 200:
                    st.success("Login successful!")
                    st.balloons()
                    st.session_state.email = email
                    st.session_state.is_logged_in = True
                    navigate_to("Dashboard")
                elif response.status_code == 403:
                    st.error(response.json().get("detail", "Access denied"))
                else:
                    st.error(response.json().get("detail", "Login failed"))
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend server. Make sure it's running.")

    st.markdown("---")
    if st.button("Don't have an account? Register"):
        navigate_to("Register")

def register_page():
    st.title("Create Account")
    st.subheader("Join us today")
    
    with st.container():
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Register"):
            if not email or not password or not confirm_password:
                st.error("Please fill in all fields")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            try:
                response = requests.post(f"{API_BASE_URL}/register", json={
                    "email": email,
                    "password": password
                })
                
                if response.status_code == 200:
                    st.success("Registration successful! Check your email for the verification code.")
                    st.session_state.email = email
                    navigate_to("Verify PIN")
                else:
                    st.error(response.json().get("detail", "Registration failed"))
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend server. Make sure it's running.")

    st.markdown("---")
    if st.button("Already have an account? Login"):
        navigate_to("Login")

def verify_pin_page():
    st.title("Verify Your Email")
    st.subheader(f"Enter the 4-digit PIN sent to {st.session_state.email}")
    
    with st.container():
        pin = st.text_input("Verification Code (OTP)", max_chars=4)
        
        if st.button("Verify"):
            if not pin or len(pin) != 4 or not pin.isdigit():
                st.error("Please enter a valid 4-digit PIN")
                return
            
            try:
                response = requests.post(f"{API_BASE_URL}/verify", json={
                    "email": st.session_state.email,
                    "otp": pin
                })
                
                if response.status_code == 200:
                    st.success("Email verified successfully! You can now login.")
                    navigate_to("Login")
                else:
                    st.error(response.json().get("detail", "Verification failed"))
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend server. Make sure it's running.")

    st.markdown("---")
    if st.button("Back to Login"):
        navigate_to("Login")


def dashboard_page():
    st.title("User Dashboard")
    st.success(f"Welcome, {st.session_state.email}!")
    
    st.markdown("""
    ### Account Overview
    You are now logged in to the secure area of our application.
    """)
    
    with st.expander("View Profile Info"):
        st.write(f"**Email:** {st.session_state.email}")
        st.write(f"**Status:** Verified ✅")
    
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.is_logged_in = False
        st.session_state.email = ''
        navigate_to("Login")

# Sidebar navigation
st.sidebar.title("Navigation")
nav_options = ["Login", "Register"]
if st.session_state.is_logged_in:
    nav_options = ["Dashboard"]

# Handle cases where session state page is not in nav_options (e.g., after login/logout)
current_index = 0
if st.session_state.page in nav_options:
    current_index = nav_options.index(st.session_state.page)

page = st.sidebar.radio("Go to", nav_options, index=current_index)

if page != st.session_state.page:
    st.session_state.page = page
    st.rerun()

# Render the selected page
if st.session_state.page == "Login":
    login_page()
elif st.session_state.page == "Register":
    register_page()
elif st.session_state.page == "Dashboard":
    if not st.session_state.is_logged_in:
        navigate_to("Login")
    dashboard_page()
