
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Smart Expense Tracker",
    layout="wide"
)

st.title("💰 Smart Expense Tracker & Budget Analyzer")

uploaded_file = st.file_uploader(
    "Upload Monthly Expense CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    ).fillna(0)

    def categorize_expense(description):
        text = str(description).lower()

        if any(word in text for word in [
            "food", "restaurant", "grocery",
            "swiggy", "zomato", "milk"
        ]):
            return "Food"

        if any(word in text for word in [
            "uber", "ola", "bus", "train",
            "fuel", "petrol", "transport"
        ]):
            return "Transport"

        if any(word in text for word in [
            "rent", "electricity", "water",
            "internet", "wifi", "recharge"
        ]):
            return "Bills"

        if any(word in text for word in [
            "movie", "game", "shopping",
            "amazon", "flipkart", "entertainment"
        ]):
            return "Entertainment"

        if any(word in text for word in [
            "medicine", "hospital", "doctor",
            "medical", "pharmacy"
        ]):
            return "Healthcare"

        if any(word in text for word in [
            "school", "college", "course",
            "education", "book"
        ]):
            return "Education"

        return "Other"

    df["Category"] = df["Description"].apply(
        categorize_expense
    )

    monthly_expense = df["Amount"].sum()

    st.sidebar.header("Budget Settings")

    monthly_income = st.sidebar.number_input(
        "Monthly Income",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    budget = st.sidebar.number_input(
        "Monthly Expense Budget",
        min_value=0.0,
        value=30000.0,
        step=1000.0
    )

    monthly_savings = (
        monthly_income -
        monthly_expense
    )

    savings_percentage = (
        monthly_savings /
        monthly_income * 100
        if monthly_income > 0
        else 0
    )

    budget_remaining = budget - monthly_expense

    st.subheader("📊 Monthly Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Monthly Income",
        f"₹{monthly_income:,.2f}"
    )

    col2.metric(
        "Total Expenses",
        f"₹{monthly_expense:,.2f}"
    )

    col3.metric(
        "Monthly Savings",
        f"₹{monthly_savings:,.2f}"
    )

    col4.metric(
        "Savings Rate",
        f"{savings_percentage:.2f}%"
    )

    if budget_remaining >= 0:
        st.success(
            f"₹{budget_remaining:,.2f} remaining in your budget."
        )
    else:
        st.error(
            f"Budget exceeded by ₹{abs(budget_remaining):,.2f}."
        )

    st.subheader("📋 Expense Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("🔎 Search & Filters")

    search = st.text_input(
        "Search Expense Description"
    )

    category_filter = st.multiselect(
        "Select Categories",
        df["Category"].unique(),
        default=list(df["Category"].unique())
    )

    filtered_df = df[
        df["Category"].isin(category_filter)
    ]

    if search:

        filtered_df = filtered_df[
            filtered_df["Description"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.subheader("💳 Category-wise Spending")

    category_expense = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots()

    ax1.bar(
        category_expense.index,
        category_expense.values
    )

    ax1.set_xlabel("Category")
    ax1.set_ylabel("Amount")
    ax1.set_title("Category-wise Spending")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)

    st.subheader("📈 Spending Trends")

    daily_expense = (
        df.groupby("Date")["Amount"]
        .sum()
    )

    fig2, ax2 = plt.subplots()

    ax2.plot(
        daily_expense.index,
        daily_expense.values,
        marker="o"
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Expense")
    ax2.set_title("Daily Spending Trend")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    st.subheader("🥧 Expense Distribution")

    fig3, ax3 = plt.subplots()

    ax3.pie(
        category_expense.values,
        labels=category_expense.index,
        autopct="%1.1f%%"
    )

    ax3.set_title("Expense Category Distribution")

    st.pyplot(fig3)

    st.subheader("⭐ Expense Prediction")

    daily_values = (
        df.groupby("Date")["Amount"]
        .sum()
    )

    if len(daily_values) >= 3:

        moving_average = (
            daily_values
            .tail(3)
            .mean()
        )

        predicted_monthly_expense = (
            moving_average *
            30
        )

        predicted_savings = (
            monthly_income -
            predicted_monthly_expense
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "3-Day Average Expense",
            f"₹{moving_average:,.2f}"
        )

        col2.metric(
            "Predicted Monthly Expense",
            f"₹{predicted_monthly_expense:,.2f}"
        )

        col3.metric(
            "Predicted Monthly Savings",
            f"₹{predicted_savings:,.2f}"
        )

        if predicted_monthly_expense > budget:
            st.warning(
                "⚠️ Predicted expenses may exceed your budget."
            )
        else:
            st.success(
                "✅ Predicted expenses are within your budget."
            )

    st.subheader("📊 Budget Summary")

    budget_summary = pd.DataFrame({
        "Metric": [
            "Monthly Income",
            "Total Expenses",
            "Monthly Savings",
            "Expense Budget",
            "Budget Remaining",
            "Savings Percentage"
        ],
        "Amount": [
            monthly_income,
            monthly_expense,
            monthly_savings,
            budget,
            budget_remaining,
            savings_percentage
        ]
    })

    st.dataframe(
        budget_summary,
        use_container_width=True
    )

    st.subheader("📥 Export Final Report")

    report = df.copy()

    report["Monthly Income"] = monthly_income
    report["Monthly Budget"] = budget
    report["Monthly Savings"] = monthly_savings
    report["Savings Percentage"] = savings_percentage

    report_csv = report.to_csv(
        index=False
    )

    st.download_button(
        label="Download Final Expense Report",
        data=report_csv,
        file_name="expense_analysis_report.csv",
        mime="text/csv"
    )




