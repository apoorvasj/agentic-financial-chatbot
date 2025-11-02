import sys
import os

# Add parent directory (project_root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import matplotlib.pyplot as plt
from langchain_groq import ChatGroq
from dotenv import load_dotenv

st.markdown("""
            <style>
                /* Background and font */
                body {
                    background-color: #f8f7fc;
                    color: #0e0e10;
                }

                /* Main container */
                .stApp {
                    background: linear-gradient(135deg, #f8f7fc, #e7e2f9);
                    color: #1a1a1a;
                    font-family: 'Segoe UI', sans-serif;
                }

                /* Sidebar styling */
                section[data-testid="stSidebar"] {
                    background-color: #f2e9fe; /* light purple */
                    color: #1a1a1a;
                }

                /* Input box */
                textarea, .stTextInput > div > input {
                    background-color: #ffffff;
                    color: #000;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }

                /* Button */
                button[kind="primary"] {
                    background-color: #6d4eff;
                    color: white;
                    border-radius: 12px;
                    padding: 0.6em 1.2em;
                }

                button[kind="primary"]:hover {
                    background-color: #563bd8;
                }

                /* Tabs and headers */
                .stTabs [role="tablist"] {
                    background-color: #eee9fc;
                    border-radius: 12px;
                }

                h1, h2, h3, h4 {
                    color: #1a1a1a;
                }

                a {
                    color: #6d4eff;
                }
            </style>
        """, unsafe_allow_html=True)
load_dotenv()

# Load Model Once
@st.cache_resource
def load_prediction_model():
    return load_model("services\models\lstm_gru.keras")

model = load_prediction_model()


# Company Mapping
companies = [
    "AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "NFLX", "JPM", "V",
    "MA", "HD", "DIS", "PYPL", "PEP", "KO", "INTC", "CSCO", "ORCL", "ADBE",
    "PFE", "MRK", "ABT", "T", "VZ", "XOM", "CVX", "WMT", "NKE", "UNH",
    "PG", "BAC", "C", "GS", "BLK", "CAT", "GE", "SBUX", "UPS", "PM",
    "LLY", "IBM", "QCOM", "BA", "MMM", "HON", "AMAT", "TMO", "RTX", "MDT"
]


# Streamlit UI
st.title("📈 AI-Powered Stock Prediction Dashboard")

user_input = st.text_input("Enter company name or ticker (e.g., Apple or AAPL):")

if st.button("Predict Stock Trend"):
    if not user_input:
        st.warning("Please enter a company name or ticker.")
    else:
        # Match company
        user_input = user_input.upper()
        matched_ticker = None

        for ticker in companies:
            if user_input in ticker or user_input in yf.Ticker(ticker).info.get("shortName", "").upper():
                matched_ticker = ticker
                break

        if not matched_ticker:
            st.error("Company not found in the top 50 list.")
        else:
            ticker = matched_ticker
            company_id = companies.index(ticker)
            st.info(f"🔹 Selected Company: {ticker}")

         
            # Fetch & Prepare Data
            data = yf.download(ticker, period="400d", interval="1d")
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
            
            scaler = MinMaxScaler()
            scaled_data = scaler.fit_transform(data)
            seq_len = 60
            X_input = scaled_data[-seq_len:].reshape(1, seq_len, scaled_data.shape[1])
            X_company = np.array([[company_id]])

            # Predict Next 30 Days
            future_days = 30
            future_predictions = []
            current_seq = X_input.copy()

            for _ in range(future_days):
                pred = model.predict([current_seq, X_company], verbose=0)
                future_predictions.append(pred[0, 0])
                next_row = current_seq[0, -1, :].copy()
                next_row[3] = pred
                current_seq = np.append(current_seq[:, 1:, :], [[next_row]], axis=1)

            dummy = np.zeros((len(future_predictions), scaled_data.shape[1]))
            dummy[:, 3] = np.array(future_predictions)
            future_prices = scaler.inverse_transform(dummy)[:, 3]


            # 🔹 Plot Chart
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data.index[-100:], data['Close'].iloc[-100:], label="Last 100 Days", color='blue')
            ax.plot(pd.date_range(data.index[-1], periods=future_days + 1, freq='B')[1:],
                    future_prices, label="Predicted Next 30 Days", color='orange', marker='o', markersize=3)
            ax.set_title(f"{ticker} - Next 30-Day Price Forecast")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price ($)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            # Return Summary Table
            last_100 = data['Close'].iloc[-100:]
            recent_start = float(last_100.iloc[0])
            recent_end = float(last_100.iloc[-1])
            pred_start = float(future_prices[0])
            pred_end = float(future_prices[-1])
            avg_change = ((pred_end - recent_end) / recent_end) * 100

            summary_df = pd.DataFrame({
                "Metric": ["Current Price", "Predicted Future Price (30 days)", "Expected % Change"],
                "Value": [recent_end, pred_end, f"{avg_change:.2f}%"]
            })
            st.subheader("Stock Summary")
            st.table(summary_df)

            #LLM Analysis
            GROQ_API_KEY = os.getenv('GROQ_API_KEY')
            llm = ChatGroq(model_name='llama-3.1-8b-instant', api_key=GROQ_API_KEY)

            summary_text = f"""
            Ticker: {ticker}
            Current Price: {recent_end:.2f}
            Predicted Future Price: {pred_end:.2f}
            Expected % Change: {avg_change:.2f}%
            """

            prompt = f"""
            You are a financial analyst AI. Analyze the following stock summary and explain to a retail investor
            whether the upcoming 30-day prediction looks favorable or risky for buying.

            Be specific about:
            - The direction of price movement
            - Whether it's a good buying opportunity or not
            - What the investor should be cautious about.

            Summary:
            {summary_text}
            """

            with st.spinner("Analyzing with LLM..."):
                response = llm.invoke(prompt)

            st.subheader("LLM Financial Insight")
            st.write(response.content)