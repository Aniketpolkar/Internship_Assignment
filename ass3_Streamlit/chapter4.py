import streamlit as st 
import pandas as pd

st.title("chai sales download ")

file = st.file_uploader("Upload your csv file ",type=["csv"])

if file:
    df = pd.read_csv(file)
    st.subheader("data preview")
    st.dataframe(df)

if file:
    st.subheader("summary stats ")
    st.write(df.describe())

if file:
    species = df["species"].unique()
    selected_species = st.selectbox("filter by species ",species)
    filtered_data = df[df["species"]==selected_species]
    st.dataframe(filtered_data)