import streamlit as st 
import datetime as dt
st.title("chai maker app")

add_masala = st.checkbox("add masala to chai")

if add_masala:
    st.write("masala is added ")

tea_type = st.radio("Pick up chai base. ",["milk","Water","Almond milk"])
st.write(f"selected base {tea_type}")

flavour = st.selectbox("choose flavour",["adrak"," kesar"," tulsi"])
st.write(f"selected flavour is {flavour}")

sugar = st.slider("sugar level:(spoon) ",0,5,4)
st.write(f"Selected sugar level {sugar}")

cups = st.number_input("How many cups ",min_value=1,max_value=12,step=1)

name = st.text_input("Enter your name")
if name:
    st.write(f"{name} Your chai is on the way.")
else :
    st.write("Hello your chai is on the way ")

dob = st.date_input("Enter your dob: ")
st.write(f"Your dob is {dt}")

if st.button("make chai "):
    st.success("Your chai is brewed")