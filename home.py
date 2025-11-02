import streamlit as st

st.set_page_config(page_title="Smart Stock Learning", page_icon="📊")
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

st.title("🏠 Welcome to Smart Stock Learning and Prediction")
st.write("Navigate through the sidebar to explore different features.")

