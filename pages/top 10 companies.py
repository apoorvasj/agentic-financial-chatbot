# ===============================================================
# 📊 Streamlit App: Evaluate Highest Predicted Cumulative Returns
# ===============================================================
import sys
import os
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import matplotlib.pyplot as plt

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Top 10 Stock Predictions", layout="wide")

# 🎨 Custom Styling
st.markdown("""
    <style>
        body {
            background-color: #f8f7fc;
            color: #0e0e10;
        }
        .stApp {
            background: linear-gradient(135deg, #f8f7fc, #e7e2f9);
            color: #1a1a1a;
            font-family: 'Segoe UI', sans-serif;
        }
        section[data-testid="stSidebar"] {
            background-color: #f2e9fe;
        }
        textarea, .stTextInput > div > input {
            background-color: #ffffff;
            color: #000;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        button[kind="primary"] {
            background-color: #6d4eff;
            color: white;
            border-radius: 12px;
            padding: 0.6em 1.2em;
        }
        button[kind="primary"]:hover {
            background-color: #563bd8;
        }
        h1, h2, h3 {
            color: #1a1a1a;
        }
        a {
            color: #6d4eff;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 Top 10 Companies by Predicted Cumulative Return")
st.write("This app loads your trained LSTM–GRU model and evaluates the top companies based on *predicted cumulative return* using recent stock data.")

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def load_trained_model():
    try:
        model = load_model("services/models/lstm_gru.keras")
        st.success("✅ Model loaded successfully.")
        return model
    except Exception as e:
        st.error(f"❌ Could not load model: {e}")
        return None

model = load_trained_model()

# -------------------------------
# Company Name Mapping
# -------------------------------
company_mapping = {
    "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOG": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc.", "META": "Meta Platforms Inc.",
    "NVDA": "NVIDIA Corp.", "NFLX": "Netflix Inc.", "INTC": "Intel Corp.",
    "ORCL": "Oracle Corp.", "PEP": "PepsiCo Inc.", "KO": "Coca-Cola Co.",
    "CSCO": "Cisco Systems Inc.", "AVGO": "Broadcom Inc.", "ADBE": "Adobe Inc.",
    "COST": "Costco Wholesale Corp.", "PYPL": "PayPal Holdings Inc.",
    "CRM": "Salesforce Inc.", "TXN": "Texas Instruments Inc.", "QCOM": "Qualcomm Inc.",
    "IBM": "IBM Corp.", "AMD": "Advanced Micro Devices Inc.", "HON": "Honeywell Int’l Inc.",
    "ABNB": "Airbnb Inc.", "SHOP": "Shopify Inc.", "BMY": "Bristol Myers Squibb Co.",
    "PFE": "Pfizer Inc.", "MRK": "Merck & Co. Inc.", "UNH": "UnitedHealth Group Inc.",
    "WMT": "Walmart Inc.", "T": "AT&T Inc.", "VZ": "Verizon Communications Inc.",
    "NKE": "Nike Inc.", "DIS": "The Walt Disney Co.", "MCD": "McDonald’s Corp.",
    "V": "Visa Inc.", "MA": "Mastercard Inc.", "GS": "Goldman Sachs Group Inc.",
    "MS": "Morgan Stanley", "JPM": "JPMorgan Chase & Co.", "BAC": "Bank of America Corp.",
    "C": "Citigroup Inc.", "BLK": "BlackRock Inc.", "CAT": "Caterpillar Inc.",
    "GE": "General Electric Co.", "UPS": "United Parcel Service Inc.",
    "PM": "Philip Morris International Inc.", "SBUX": "Starbucks Corp.",
    "CVX": "Chevron Corp.", "XOM": "Exxon Mobil Corp."
}

# -------------------------------
# Prepare Test Data Function
# -------------------------------
def prepare_test_data(tickers, unroll_length=60):
    all_scalers = {}
    X_all, y_all, idx_all = [], [], []

    for i, symbol in enumerate(tickers):
        try:
            data = yf.download(symbol, start="2015-01-01", end="2025-01-01", progress=False)
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
            scaler = MinMaxScaler()
            scaled = scaler.fit_transform(data)
            all_scalers[symbol] = scaler

            for j in range(unroll_length, len(scaled)):
                X_all.append(scaled[j - unroll_length:j])
                y_all.append(scaled[j, 3])
                idx_all.append(i)
        except Exception as e:
            st.warning(f"⚠ Skipping {symbol}: {e}")

    return np.array(X_all), np.array(y_all), np.array(idx_all), all_scalers

# -------------------------------
# Compute Results
# -------------------------------
@st.cache_data
def compute_results(model, companies):
    X_all, y_all, idx_all, scalers = prepare_test_data(companies)
    split = int(0.8 * len(X_all))
    X_test, y_test, idx_test = X_all[split:], y_all[split:], idx_all[split:]

    preds = model.predict([X_test, idx_test])
    results = []

    for i, ticker in enumerate(companies):
        mask = idx_test == i
        if np.sum(mask) == 0:
            continue

        preds_t, y_t = preds[mask], y_test[mask]
        scaler = scalers[ticker]
        dummy = np.zeros((len(preds_t), 5))

        dummy[:, 3] = preds_t[:, 0]
        preds_real = scaler.inverse_transform(dummy)[:, 3]

        dummy[:, 3] = y_t
        actual_real = scaler.inverse_transform(dummy)[:, 3]

        actual_cum_return = ((actual_real[-1] - actual_real[0]) / actual_real[0]) * 100
        predicted_cum_return = ((preds_real[-1] - preds_real[0]) / preds_real[0]) * 100

        return_diff = np.abs(predicted_cum_return - actual_cum_return)

        results.append((
            company_mapping[ticker],
            return_diff,
            actual_cum_return,
            predicted_cum_return
        ))

    df = pd.DataFrame(results, columns=[
        "Company Name",
        "Return Difference (%)",
        "Actual Cumulative Return (%)",
        "Predicted Cumulative Return (%)"
    ])
    df_sorted = df.sort_values(by="Predicted Cumulative Return (%)", ascending=False).reset_index(drop=True)
    return df_sorted

# -------------------------------
# Run Evaluation
# -------------------------------
if model:
    companies = list(company_mapping.keys())
    st.info("⏳ Fetching data and evaluating predictions... (may take a few minutes)")
    df_sorted = compute_results(model, companies)

    # Show top 10
    top10 = df_sorted.head(10)
    st.subheader("🏅 Top 10 Companies by Predicted Cumulative Return")
    st.dataframe(top10.style.format({
        "Return Difference (%)": "{:.2f}",
        "Actual Cumulative Return (%)": "{:.2f}",
        "Predicted Cumulative Return (%)": "{:.2f}"
    }))

    # -------------------------------
    # Visualization
    # -------------------------------
    st.subheader("📈 Actual vs Predicted Cumulative Return (Top 10)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(top10["Company Name"], top10["Actual Cumulative Return (%)"], label="Actual Return (%)")
    ax.bar(top10["Company Name"], top10["Predicted Cumulative Return (%)"], label="Predicted Return (%)", alpha=0.7)
    ax.set_ylabel("Cumulative Return (%)")
    ax.set_xlabel("Company Name")
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    st.pyplot(fig)