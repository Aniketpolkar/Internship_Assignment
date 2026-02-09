import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ------------------ UI ------------------
st.set_page_config(page_title="Stock Price Prediction", layout="centered")
st.title("📈 Stock Price Prediction (Simple ML)")
st.write("Predict **Next Day Close Price** using Linear Regression")

# ------------------ Upload CSV ------------------
uploaded_file = st.file_uploader("Upload stock CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ------------------ Feature Engineering ------------------
    df["Target"] = df["Close"].shift(-1)  # next day close
    df.dropna(inplace=True)

    X = df[["Open", "High", "Low", "Volume"]]
    y = df["Target"]

    # ------------------ Train-Test Split ------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # ------------------ Train Model ------------------
    model = LinearRegression()
    model.fit(X_train, y_train)

    # ------------------ Predictions ------------------
    predictions = model.predict(X_test)

    # ------------------ Plot ------------------
    st.subheader("Actual vs Predicted Close Price")

    fig, ax = plt.subplots()
    ax.plot(y_test.values, label="Actual Close", color="blue")
    ax.plot(predictions, label="Predicted Close", color="red")
    ax.legend()
    ax.set_xlabel("Days")
    ax.set_ylabel("Price")

    st.pyplot(fig)

    # ------------------ Next Day Prediction ------------------
    st.subheader("Predict Next Day Close Price")

    last_row = X.iloc[-1:].values
    next_day_price = model.predict(last_row)[0]

    st.success(f"📊 Predicted Next Day Close Price: **{next_day_price:.2f}**")

else:
    st.info("Please upload a CSV file with stock data.")
