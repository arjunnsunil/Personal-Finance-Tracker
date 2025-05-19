# 🧠 Personal Finance Tracker with LLAMA

This is a Streamlit-based personal finance tracker that allows users to:
- Upload their transaction data (CSV)
- View monthly summaries, category-wise breakdowns
- Set budgets and receive overspending alerts
- Ask custom finance-related questions
- Get smart insights powered by a local LLAMA model (like Mistral)

---

## 📸 Features

- 🔍 Raw transaction preview
- 📈 Monthly summaries with income, expense, and net savings
- 🧾 Category-wise expense breakdown with totals
- 🛑 Overspending alerts based on user-defined budgets
- 🧠 AI advisor to provide financial feedback and answer finance queries
- 🗣️ Supports category/month extraction from user questions

---

## 📂 Project Structure

Personal-Finance-Tracker-LLAMA/
├── app/
│ ├── main.py # Streamlit app
│ ├── llm_provider.py # LLAMA LLM integration
│
├── data/
│ └── transactions_5months.csv # Sample data
│
├── test_llama.py # Script to test LLAMA model separately
├── requirements.txt
├── README.md
└── .gitignore

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Personal-Finance-Tracker-LLAMA.git
cd Personal-Finance-Tracker-LLAMA

---

### 2. Setup a virtual environment

```bash
python -m venv llama_env
source llama_env/bin/activate      # For Linux/macOS
llama_env\Scripts\activate         # For Windows

### 3. Install required dependencies

```bash
pip install -r requirements.txt

### 4. Add your LLM model

```bash