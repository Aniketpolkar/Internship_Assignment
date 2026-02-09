import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Task Manager", layout="centered")

# ---------------- SESSION STATE ----------------
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- AUTH ----------------
def login(username, password):
    res = requests.post(
        f"{API_URL}/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if res.status_code == 200:
        st.session_state.token = res.json()["access_token"]
        st.success("Login successful")
    else:
        st.error("Invalid credentials")

# ---------------- API CALLS ----------------
def get_tasks():
    res = requests.get(
        f"{API_URL}/tasks",
        headers={"Authorization": f"Bearer {st.session_state.token}"},
    )
    return res.json() if res.status_code == 200 else []

def create_task(title, completed):
    res = requests.post(
        f"{API_URL}/tasks",
        json={"title": title, "completed": completed},
        headers={"Authorization": f"Bearer {st.session_state.token}"},
    )
    return res.status_code == 200

def delete_task(task_id):
    res = requests.delete(
        f"{API_URL}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {st.session_state.token}"},
    )
    return res.status_code == 200

# ---------------- UI ----------------
st.title("📝 Task Manager")

# ---- LOGIN ----
if not st.session_state.token:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login(username, password)

    st.stop()

# ---- TASKS ----
st.subheader("Your Tasks")

tasks = get_tasks()

for task in tasks:
    col1, col2, col3 = st.columns([5, 2, 1])
    col1.write(task["title"])
    col2.write("✅ Done" if task["completed"] else "⏳ Pending")
    if col3.button("❌", key=task["id"]):
        delete_task(task["id"])
        st.rerun()

# ---- CREATE TASK ----
st.subheader("Add New Task")

title = st.text_input("Task title")
completed = st.checkbox("Completed")

if st.button("Add Task"):
    if title:
        create_task(title, completed)
        st.success("Task added")
        st.rerun()
    else:
        st.warning("Title required")

# ---- LOGOUT ----
if st.button("Logout"):
    st.session_state.token = None
    st.rerun()
