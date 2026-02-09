import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Task Manager", layout="centered")

# -------- Session State --------
if "token" not in st.session_state:
    st.session_state.token = None

if "email" not in st.session_state:
    st.session_state.email = None


def api_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


# ---------- AUTH ----------
def login_user(email, password):
    return requests.post(
        f"{API_URL}api/auth/login",
        data={  # ✅ FORM DATA (OAuth2)
            "username": email,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )


def register_user(email, password):
    print(email)
    return requests.post(
        f"{API_URL}api/auth/register",
        json={  # ✅ JSON as expected by FastAPI
            "email": email,
            "password": password
        }
    )


# ---------- TASKS ----------
def get_tasks():
    return requests.get(f"{API_URL}api/tasks", headers=api_headers())


def create_task(title, description):
    return requests.post(
        f"{API_URL}api/tasks",
        json={"title": title, "description": description},
        headers=api_headers()
    )


def update_task(task_id, title, description):
    return requests.put(
        f"{API_URL}api/tasks/{task_id}",
        json={"title": title, "description": description},
        headers=api_headers()
    )


def delete_task(task_id):
    return requests.delete(
        f"{API_URL}api/tasks/{task_id}",
        headers=api_headers()
    )


# ---------- UI ----------
def auth_page():
    st.title("Task Manager")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            res = login_user(email, password)
            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["access_token"]
                st.session_state.email = email
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error(res.json().get("detail", "Login failed"))

    with tab_register:
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            res = register_user(email, password)
            if res.status_code in (200, 201):
                st.success("Registration successful. Please login.")
            else:
                st.error(res.json().get("detail", "Registration failed"))


def dashboard():
    st.title("Dashboard")
    st.write(f"Logged in as **{st.session_state.email}**")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.email = None
        st.rerun()

    st.divider()

    # ---- Create Task ----
    st.subheader("Create Task")
    title = st.text_input("Title")
    description = st.text_area("Description")

    if st.button("Add Task"):
        res = create_task(title, description)
        
        if res.status_code == 200:
            st.success("Task created")
            # st.rerun()
        else:
            st.error("Failed to create task")

    st.divider()

    # ---- List Tasks ----
    st.subheader("Your Tasks")
    res = get_tasks()

    if res.status_code != 200:
        st.error("Could not fetch tasks")
        return

    tasks = res.json()

    if not tasks:
        st.info("No tasks yet")
        return

    for task in tasks:
        with st.expander(task["title"]):
            new_title = st.text_input(
                "Edit title", task["title"], key=f"title_{task['id']}"
            )
            new_desc = st.text_area(
                "Edit description", task["description"], key=f"desc_{task['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Update", key=f"upd_{task['id']}"):
                    update_task(task["id"], new_title, new_desc)
                    st.rerun()

            with col2:
                if st.button("Delete", key=f"del_{task['id']}"):
                    delete_task(task["id"])
                    st.rerun()


# ---------- ENTRY ----------
if st.session_state.token is None:
    auth_page()
else:
    dashboard()

