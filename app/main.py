import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from llm_provider import get_response

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("📊 Personal Finance Tracker")

uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["Category"] = df["Category"].astype(str)
    df["Type"] = df["Type"].astype(str)


    # Preprocessing
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by="Date")
    df['Month'] = df['Date'].dt.to_period('M').astype(str)

    st.subheader("🔍 Raw Transaction Data")
    st.dataframe(df, use_container_width=True)

    # ========== STEP 3 Starts Here ========== #

    # Key Metrics
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    net_savings = total_income - total_expense

    st.markdown("### 📈 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.0f}")
    col2.metric("Total Expenses", f"₹{total_expense:,.0f}")
    col3.metric("Net Savings", f"₹{net_savings:,.0f}", delta=f"{net_savings:,.0f}")

    # Monthly Summary
    monthly_summary = df.groupby(['Month', 'Type'])['Amount'].sum().unstack().fillna(0)
    monthly_summary['Net Savings'] = monthly_summary['Income'] - monthly_summary['Expense']

    st.markdown("### 🗓️ Monthly Financial Summary")
    st.dataframe(monthly_summary, use_container_width=True)

    #Monthly Category Summary
    st.markdown("### 🧾 Monthly Category-Wise Expense Summary")

    # Filter for only expenses 
    expense_df = df[df["Type"] == "Expense"]

    # Pivot table: Rows = Month, Columns = Category, Values = Sum of Amount
    monthly_cat_summary = pd.pivot_table(
        expense_df,
        values="Amount",
        index="Month",
        columns="Category",
        aggfunc="sum",
        fill_value=0
    )

    # Add a "Total" column
    monthly_cat_summary["Total"] = monthly_cat_summary.sum(axis=1)

    # Show the table
    st.dataframe(monthly_cat_summary.style.format("₹{:.0f}"), use_container_width=True)

    # Income vs Expense Bar Chart
    st.markdown("### 📊 Income vs Expenses Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_summary[['Income', 'Expense']].plot(kind='bar', ax=ax)
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Monthly Income vs Expenses")
    st.pyplot(fig)
    
    #Create Budget Inputs
    st.markdown("### 💸 Set Your Monthly Budgets")

    # Extract unique categories
    expense_categories = df[df["Type"] == "Expense"]["Category"].unique()
    
    # Dictionary to store user budgets
    user_budgets = {}

    for category in expense_categories:
        budget = st.number_input(f"Set budget for {category} (₹)", min_value=0, value=5000, step=500, key=f"budget_{category}")
        user_budgets[category] = budget

    # Expense by Category Pie Chart
    st.markdown("### 🥧 Expense Distribution by Category")
    category_summary = df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
    fig2, ax2 = plt.subplots()
    ax2.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    st.pyplot(fig2)

    # Calculate Category Spend vs Budget
    st.markdown("### 🚨 Overspending Alerts")

    # Group expenses by category and month
    monthly_expense_by_cat = df[df["Type"] == "Expense"].groupby(["Month", "Category"])["Amount"].sum().reset_index()

    # Check for budget violations
    alerts = []

    for _, row in monthly_expense_by_cat.iterrows():
        month = row["Month"]
        category = row["Category"]
        spent = row["Amount"]
        budget = user_budgets.get(category, 0)

        if spent > budget:
            # Convert "2025-01" to "January 2025"
            formatted_month = pd.to_datetime(month).strftime("%B %Y")
            alerts.append(f"🔴 {category} exceeded budget in {formatted_month}: ₹{spent:,.0f} > ₹{budget:,.0f}")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("✅ No overspending detected for any category.")

    
    # AI
    st.markdown("### 🤖 AI Financial Advisor")

    if st.button("Generate AI Insights"):
        with st.spinner("Analyzing your financial habits..."):
            # Prepare summary stats for LLM
            total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
            total_income = df[df['Type'] == 'Income']['Amount'].sum()
            top_categories = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3)

            summary_text = f"""
            Total income: ₹{total_income:,.0f}
            Total expenses: ₹{total_expense:,.0f}
            Net savings: ₹{total_income - total_expense:,.0f}
            Top spending categories: {', '.join(f"{cat} (₹{amt:,.0f})" for cat, amt in top_categories.items())}
            """

            # Prompt for LLM
            SYSTEM_PROMPT = """
            You are a smart and honest AI financial advisor.

            You will receive a user's financial summary including income, expenses, savings, and spending by category.

            Your task is to:
            - Assess if the user is saving enough
            - Identify any overspending trends
            - Suggest practical ways to cut unnecessary spending
            - Give budgeting tips and long-term financial advice

            Do NOT make up data. Be helpful, realistic, and encouraging.

            Respond in under 150 words.
            """

            prompt = f"""{SYSTEM_PROMPT}

            User's Financial Summary:
            {summary_text}

            Your advice:
            """


            try:
                advice = get_response(prompt)
                st.success("AI Insights Generated ✅")
                st.markdown(advice)
            except Exception as e:
                st.error(f"LLM Error: {e}")

    # Custom Questions
    st.markdown("### 💬 Ask Custom Finance Questions")

    user_question = st.text_area("Ask your finance question:")

    month_map = {
      "1st": "2025-01",
      "2nd": "2025-02",
      "3rd": "2025-03",
      "4th": "2025-04",
      "5th": "2025-05",
      "last": "2025-05"  # latest month in your table
    }

    # Expanded category synonym map
    category_synonyms = {
        "education": ["education", "tuition", "learning", "courses", "school", "college", "books"],
        "entertainment": ["entertainment", "fun", "leisure", "movies", "netflix", "gaming", "recreation"],
        "food": ["food", "groceries", "eating", "dining", "meals", "snacks", "restaurants", "cafe"],
        "travel": ["travel", "transportation", "commute", "taxi", "uber", "bus", "train", "flight", "ride", "car"],
        "utilities": ["utilities", "bills", "electricity", "water", "internet", "gas", "mobile", "phone", "recharge", "wifi"],
        "health": ["health", "medical", "doctor", "hospital", "medicine", "pharmacy", "clinic"],
        "shopping": ["shopping", "clothes", "apparel", "fashion", "online shopping", "amazon", "flipkart"],
        "rent": ["rent", "housing", "apartment", "flat", "room", "lease"],
        "others": ["others", "miscellaneous", "other", "etc"]
    }

    def extract_category_and_month(question):
        question = question.lower()
        category = None
        month = None

        for true_cat, synonyms in category_synonyms.items():
            for word in synonyms:
                if word in question:
                    category = true_cat
                    break
            if category:
                break

        for key, val in month_map.items():
            if key in question:
                month = val
                break

        return category, month


    if st.button("Get Advice"):
        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    category, month = extract_category_and_month(user_question)
                    st.write("🔍 Detected:", category, month)
                    if category and month:
                        filtered_amount = df[
                            (df["Type"] == "Expense") &
                            (df["Category"].str.lower() == category) &
                            (df["Date"].dt.to_period("M").astype(str) == month)
                        ]["Amount"].sum()

                        st.success(f"✅ You spent ₹{filtered_amount:,.0f} on {category.capitalize()} in {month}.")
                    else:
                        # Fallback to LLM
                        custom_prompt = f"""
                        You are a helpful and precise AI financial assistant.

                        The user may ask a question related to budgeting, savings, expenses, investments, or general personal finance.

                        Always respond clearly and realistically. If you need more data to answer fully, explain what’s missing.

                        Use Indian Rupees (₹) in all your answers.

                        User Question: {user_question.strip()}
                        Answer:
                        """.strip()

                        answer = get_response(custom_prompt)
                        st.write(answer)
                except Exception as e:
                    st.error(f"LLM Error: {e}")


else:
    st.info("Please upload a CSV file to begin.")