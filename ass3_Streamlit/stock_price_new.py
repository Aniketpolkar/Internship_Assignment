import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline

# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(
    page_title="Stock Dashboard & Text Summarization",
    layout="wide"
)

st.title("📊 Stock Price Dashboard & 📝 Text Summarization")

# ===============================
# SECTION 1: STOCK DASHBOARD
# ===============================
st.header("1. Stock Price Visualization Dashboard")

uploaded_file = st.file_uploader(
    "Upload Stock Dataset (CSV)",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Data preprocessing
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Statistical Summary")
    st.write(df.describe())

    # Sidebar controls
    st.sidebar.header("Stock Visualization Controls")

    price_col = st.sidebar.selectbox(
        "Select Price Column",
        ["Open", "High", "Low", "Close", "Adj Close"]
    )

    show_ma = st.sidebar.checkbox("Show Moving Averages")
    show_volume = st.sidebar.checkbox("Show Volume")

    # Price chart
    st.subheader(f"{price_col} Price Trend")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["Date"], df[price_col], label=price_col)

    if show_ma:
        df["MA20"] = df[price_col].rolling(20).mean()
        df["MA50"] = df[price_col].rolling(50).mean()
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

else:
    st.info("Upload a stock CSV file to enable visualization.")

# ===============================
# SECTION 2: TEXT SUMMARIZATION
# ===============================
st.header("2. Stock Text Summarization")

st.write(
    "Enter stock-related news, reports, or descriptions below. "
    "The system will generate a concise summary."
)

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

input_text = st.text_area(
    "Enter Stock News / Description Text",
    height=250
)

if st.button("Generate Summary"):
    if len(input_text.strip()) < 50:
        st.warning("Please enter more text for meaningful summarization.")
    else:
        with st.spinner("Generating summary..."):
            summary = summarizer(
                input_text,
                max_length=130,
                min_length=40,
                do_sample=False
            )
        st.subheader("Summary Output")
        st.success(summary[0]["summary_text"])
