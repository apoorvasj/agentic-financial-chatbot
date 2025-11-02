import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Learn About Stocks", layout="wide")
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

st.title("📈 Learn About Stocks")
st.write("Welcome to your beginner-friendly guide to understanding the stock market!")

# --- Sidebar ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["🎥 YouTube Tutorials", "📄 Stock Market Guides", "🧠 Quiz Yourself"])

# --- YouTube Links ---
if page == "🎥 YouTube Tutorials":
    st.header("Educational YouTube Videos")
    st.write("Here are some great beginner-friendly videos to learn about investing and stock markets:")

    videos = {
        "Stock Market for Beginners – Simplified": "https://www.youtube.com/watch?v=p7HKvqRI_Bo",
        "How Does the Stock Market Work?": "https://www.youtube.com/watch?v=F3QpgXBtDeo",
        "Investing 101: Stock Market Course for Beginners": "https://www.youtube.com/watch?v=9-PQm9yVuS0",
        "Understanding IPOs and How Companies Go Public": "https://www.youtube.com/watch?v=1mKAv3r2O3E",
        "ETFs vs Mutual Funds Explained": "https://www.youtube.com/watch?v=Ff9Aq3T1Awk",
        "Technical vs Fundamental Analysis": "https://www.youtube.com/watch?v=O8zK-z2Z_7I",
    }

    for title, link in videos.items():
        st.markdown(f"🔗 [{title}]({link})")

# --- Documentation Links ---
elif page == "📄 Stock Market Guides":
    st.header("📄 Beginner-Friendly Stock Market Documentation")
    st.write("Learn the basics with these beginner resources:")

    docs = {
        "Investopedia: Stock Basics": "https://www.investopedia.com/articles/basics/06/invest1000.asp",
        " NSE India: How to Invest in Stocks": "https://www.nseindia.com/learn/invest-basics",
        " SEBI Investor Education": "https://investor.sebi.gov.in/",
        " Yahoo Finance – Market Data": "https://finance.yahoo.com/",
        " Khan Academy: Stocks and Bonds": "https://www.khanacademy.org/economics-finance-domain/core-finance/stock-and-bonds",
    }

    for title, link in docs.items():
        st.markdown(f"🔗 [{title}]({link})")

# --- Quiz Section ---
elif page == "🧠 Quiz Yourself":
    st.header("Stock Market Quiz")
    st.write("Test your knowledge after learning!")

    questions = [
        {
            "q": "1️⃣ What is a stock?",
            "options": ["A loan to a company", "A share of ownership in a company", "A government bond"],
            "answer": "A share of ownership in a company",
        },
        {
            "q": "2️⃣ What does IPO stand for?",
            "options": ["Initial Public Offering", "Investment Purchase Option", "Index Price Operation"],
            "answer": "Initial Public Offering",
        },
        {
            "q": "3️⃣ Which of the following represents a stock exchange in India?",
            "options": ["NASDAQ", "NYSE", "NSE"],
            "answer": "NSE",
        },
        {
            "q": "4️⃣ What does ‘diversification’ mean in investing?",
            "options": ["Investing in a single stock", "Spreading investments across assets", "Selling all stocks"],
            "answer": "Spreading investments across assets",
        },
        {
            "q": "5️⃣ What is the purpose of a mutual fund?",
            "options": ["To loan money to businesses", "To pool money from investors to buy securities", "To guarantee fixed returns"],
            "answer": "To pool money from investors to buy securities",
        },
        {
            "q": "6️⃣ What does a higher P/E ratio generally indicate?",
            "options": ["The stock is undervalued", "The stock might be overvalued", "The company has no earnings"],
            "answer": "The stock might be overvalued",
        },
    ]

    score = 0
    for i, q in enumerate(questions):
        answer = st.radio(q["q"], q["options"], key=i)
        if answer == q["answer"]:
            score += 1

    if st.button("Submit Quiz"):
        st.success(f"🎉 You scored {score}/6!")
        if score == 6:
            st.balloons()
        elif score >= 4:
            st.info("Great job! You’ve got a good grasp of stock basics.")
        else:
            st.warning("Keep learning! Check the video and documentation sections above.")