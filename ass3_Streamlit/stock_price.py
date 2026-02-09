import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
st.title("📈 Stock Market Analysis & Prediction Dashboard")

uploaded_file = st.file_uploader("Upload Stock CSV File", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")
    st.write("Shape:", df.shape)
    st.write(df.describe())

    # Sidebar options
    st.sidebar.header("Visualization Settings")

    price_type = st.sidebar.selectbox(
        "Select Price Type",
        ["Open", "High", "Low", "Close", "Adj Close"]
    )

    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    show_ma = st.sidebar.checkbox("Show Moving Averages")

    # Plot price
    st.subheader(f"{price_type} Price Over Time")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["Date"], df[price_type], label=price_type)

    # Moving averages
    if show_ma:
        df["MA20"] = df[price_type].rolling(window=20).mean()
        df["MA50"] = df[price_type].rolling(window=50).mean()
        ax.plot(df["Date"], df["MA20"], label="MA 20")
        ax.plot(df["Date"], df["MA50"], label="MA 50")

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)

    # Volume chart
    if show_volume:
        st.subheader("Trading Volume")
        fig2, ax2 = plt.subplots(figsize=(12, 3))
        ax2.bar(df["Date"], df["Volume"])
        ax2.set_ylabel("Volume")
        st.pyplot(fig2)

    # Correlation
    st.subheader("Feature Correlation Matrix")
    st.dataframe(df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].corr())

    # Prediction placeholder
    st.subheader("Prediction (Extension)")
    st.info(
        "You can integrate ML models such as Linear Regression, LSTM, or Prophet here "
        "for future stock price prediction."
    )

else:
    st.warning("Please upload a CSV file to proceed.")
