import streamlit as st
from google import genai
import os

# Initialize Gemini client
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.Client(api_key="AIzaSyBDJWRCD0rCFrKOfeHpn__vbOMfyb4XG04")

st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")
st.title("Gemini Chatbot")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini response
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_input
    )

    bot_reply = response.text

    # Show bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
