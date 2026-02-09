import streamlit as st

# Page title
st.title("My First Streamlit App")

# Simple text
st.write("Welcome to Streamlit")

# Text input
name = st.text_input("Enter your name")

# Button
if st.button("Submit"):
    if name:
        st.success(f"Hello, {name}!")
    else:
        st.warning("Please enter your name")
