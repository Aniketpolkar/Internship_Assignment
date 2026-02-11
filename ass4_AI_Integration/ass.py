import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Dual GenAI Assistant")
st.write("Mode: Research 📝 or Creative Writing ✍️")

mode = st.radio("Choose Mode:", ["Research", "Creative Writing"])

user_input = st.text_input("Enter topic or prompt:")

if st.button("Submit") and user_input:
    with st.spinner("Generating response..."):
        if mode == "Research":
            prompt = f"Provide a brief research summary on: {user_input}"
        else:
            prompt = f"Write a creative piece on: {user_input}"

        response = client.models.generate_content(
           model="gemini-3-flash-preview",
            contents=prompt
        )
        st.markdown("**Assistant:**")
        st.write(response.text)
