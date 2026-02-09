import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- Page Config ----------------
st.set_page_config(page_title="Stock Price Prediction", layout="wide")
st.title("📊 Stock Price Prediction using Machine Learning")

st.write("""
This application predicts the **next day's closing stock price**
using a **Random Forest Regression model**.
""")

# ---------------- Upload Data ----------------
uploaded_file = st.file_uploader("Upload Stock CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ---------------- Data Preprocessing ----------------
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # ---------------- Feature Engineering ----------------
    df["Target"] = df["Close"].shift(-1)  # Next-day close
    df.dropna(inplace=True)

    features = ["Open", "High", "Low", "Close", "Volume"]
    X = df[features]
    y = df["Target"]

    # ---------------- Train-Test Split ----------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # ---------------- Model Training ----------------
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)

    # ---------------- Prediction ----------------
    predictions = model.predict(X_test)

    # ---------------- Evaluation Metrics ----------------
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    st.subheader("📌 Model Performance")
    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{mae:.2f}")
    col2.metric("RMSE", f"{rmse:.2f}")
    col3.metric("R² Score", f"{r2:.2f}")

    # ---------------- Graph 1: Actual vs Predicted ----------------
    st.subheader("📈 Actual vs Predicted Close Price")

    fig, ax = plt.subplots(figsize=(16, 4))
    ax.plot(y_test.values, label="Actual Close Price", color="blue")
    ax.plot(predictions, label="Predicted Close Price", color="red")
    ax.set_xlabel("Days")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)

    # ---------------- Graph 2: Error Distribution ----------------
    st.subheader("📉 Prediction Error Distribution")

    errors = y_test.values - predictions
    fig, ax = plt.subplots(figsize=(16, 4))
    sns.histplot(errors, bins=50, kde=True, ax=ax)
    ax.set_xlabel("Prediction Error")
    st.pyplot(fig)

    # ---------------- Graph 3: Feature Importance ----------------
    st.subheader("🔍 Feature Importance")

    importance = model.feature_importances_
    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": importance
    }).sort_values(by="Importance", ascending=False)

    fig, ax = plt.subplots(figsize=(16, 4))
    sns.barplot(x="Importance", y="Feature", data=importance_df, ax=ax)
    st.pyplot(fig)

    # ---------------- Next Day Prediction ----------------
    st.subheader("📊 Next Day Stock Price Prediction")

    last_data = X.iloc[-1:].values
    next_day_prediction = model.predict(last_data)[0]

    st.success(f"💰 Predicted Next Day Close Price: **{next_day_prediction:.2f}**")

else:
    st.info("Please upload a stock CSV file to begin.")
