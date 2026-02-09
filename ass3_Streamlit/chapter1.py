import streamlit as st 

st.title("Hello world app ")
st.subheader("Subheader in streamlit app ")
st.text("Welcome to text app ")
st.write("Welcome to write app ")

chai = st.selectbox("your favourit chai ",["lemon tea","masala chai","adrak chai"])
coffee = st.selectbox("Your favourite coffee ",["cold coffee","hot coffe"])
st.write(coffee)
st.text(f"you choose {chai}. excellent choise")
st.success("Your chai has been brewed! ")