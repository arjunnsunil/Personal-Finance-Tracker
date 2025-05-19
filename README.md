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

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Personal-Finance-Tracker-LLAMA.git
cd Personal-Finance-Tracker-LLAMA
```

### 2. Setup a virtual environment

```bash
python -m venv llama_env
source llama_env/bin/activate      # For Linux/macOS
llama_env\Scripts\activate         # For Windows
```

### 3. Install required dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your LLaMA GGUF Model

Download a mistral-7b-instruct-v0.1.Q4_0.gguf or similar model file and place it here:
```bash
C:\llama_models\mistral-7b-instruct-v0.1.Q4_0.gguf
```
You can change the path in llm_provider.py if needed.

### 5. Run the Streamlit App

```bash
streamlit run app/main.py
```

---

## 📌 Sample CSV Format

Your input file must have the following columns:
- Date (e.g., 2025-01-05)
- Type (Income or Expense)
- Category (e.g., Food, Rent, Travel)
- Amount (e.g., 2500)

---

## 🧠 AI Assistant Usage
The app uses a local LLaMA model via llama-cpp-python to:
- Analyze your top expenses
- Suggest saving tips
- Answer budget questions from user input

---

## ✅ Future Improvements
- Export reports to PDF
- Support for investment tracking
- Integration with online bank APIs