# Agent-Based System for Smart Stock Investment

This project implements an **agent-based architecture** designed to assist users with **smart stock investment decisions** by combining **real-time financial data**, **regulatory knowledge**, and **conversational intelligence**.

---

## System Overview

The system is built around **two specialized agents**, coordinated by a **Router (LLM)** that intelligently decides how to handle each user query.

<img width="2354" height="800" alt="image" src="https://github.com/user-attachments/assets/48ae41d8-aaad-402a-9c98-dbceb6f21eeb" />


### Core Agents

<img width="1500" height="1226" alt="image" src="https://github.com/user-attachments/assets/545dd1ac-6830-4954-baa4-fba8e63d4a1e" />


#### 1. RAG Agent (Retrieval-Augmented Generation)
- Retrieves and explains:
  - **SEBI regulations**
  - **Zerodha rulebooks and guides**
  - **Beginner-friendly financial documentation**
- Ensures **accurate, trusted responses** by grounding answers in verified sources.
- Minimizes hallucinations by relying on structured regulatory and educational data.

#### 2. Financial Agent
- Fetches **real-time stock market data** using live APIs:
  - **Financial Modeling Prep (FMP)**
  - **Alpha Vantage**
- Provides up-to-date insights such as:
  - Stock prices
  - Profit margins
  - Market indicators
  - Financial ratios

---

## Router Architecture
<img width="2603" height="976" alt="image" src="https://github.com/user-attachments/assets/9f1678f3-b434-4240-a62d-bfe150fd6682" />


At the heart of the system is a **Router (LLM)** that:
- Acts as a **central decision-maker**
- Analyzes each user query
- Routes the request to:
  - **Live Financial Data Tool** (for real-time analysis), or
  - **RAG Agent** (for regulatory or knowledge-based questions)

### Routing Paths

- **Live Financial Data Tool Call**
  - Used for real-time queries (e.g., stock price, company performance)
  - Executes API calls to financial data providers

- **RAG (Retrieval-Augmented Generation)**
  - Used for compliance, rules, and conceptual learning
  - Sources data from SEBI regulations, Zerodha documentation, and curated rulebooks

---

## Key Features

- **Multi-turn conversational learning**
-  **Memory-enabled interactions** using session history
-  **Real-time financial data analysis** via API integrations
-  **Trusted knowledge retrieval** using RAG to reduce hallucinations
-  **PostgreSQL integration** for long-term memory and persistent user context

---

## Use Cases

- Beginners learning stock market rules and compliance
- Investors checking live stock data and metrics
- Interactive financial education with regulatory grounding
- Intelligent query handling across data and documentation

---
