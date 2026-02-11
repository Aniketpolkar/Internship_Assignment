import streamlit as st
import requests
import hashlib

st.title("Secure Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

def get_device_hash():
    raw = st.session_state.get("client_id", "default")
    return hashlib.sha256(raw.encode()).hexdigest()

if st.button("Login"):
    payload = {
        "email": email,
        "password": password,
        "ip": "192.168.1.10",  # replace with real IP capture
        "device_hash": get_device_hash()
    }

    r = requests.post("http://localhost:8000/login", json=payload)

    if r.status_code == 200:
        data = r.json()
        if data["decision"] == "ALLOW":
            st.success("Login successful")
        elif data["decision"] == "REQUIRE_MFA":
            st.warning("MFA required")
        else:
            st.error("Login blocked")
    else:
        st.error("Invalid credentials")
