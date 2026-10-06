import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Fraud Detection System", layout="wide")

st.title("💳 Fraud Detection & Transaction Analysis System")

uploaded_file = st.file_uploader("Upload Transaction CSV File", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Amount"] = pd.to_numeric(df["Amount"])

    duplicate_count = df.duplicated().sum()

    duplicates = df[df.duplicated(keep=False)]

    threshold = st.number_input(
        "Enter High-Value Transaction Threshold",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    high_value = df[df["Amount"] > threshold]

    account_frequency = df["Account"].value_counts()

    frequency_threshold = st.number_input(
        "Suspicious Account Transaction Count",
        min_value=1,
        value=5,
        step=1
    )

    suspicious_accounts = account_frequency[
        account_frequency >= frequency_threshold
    ].index

    suspicious_account_transactions = df[
        df["Account"].isin(suspicious_accounts)
    ]

    df["Risk Score"] = 0

    df.loc[df["Amount"] > threshold, "Risk Score"] += 40

    df.loc[df["Account"].isin(suspicious_accounts), "Risk Score"] += 30

    df.loc[df.duplicated(keep=False), "Risk Score"] += 30

    df["Risk Level"] = pd.cut(
        df["Risk Score"],
        bins=[-1, 29, 59, 100],
        labels=["Low", "Medium", "High"]
    )

    suspicious_transactions = df[df["Risk Score"] >= 40]

    st.subheader("📊 Transaction Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", len(df))
    col2.metric("Duplicate Transactions", duplicate_count)
    col3.metric("High-Value Transactions", len(high_value))
    col4.metric("Suspicious Transactions", len(suspicious_transactions))

    st.subheader("🔎 Search & Filters")

    search = st.text_input("Search Account or Category")

    risk_filter = st.multiselect(
        "Select Risk Level",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )

    category_filter = st.multiselect(
        "Select Category",
        df["Category"].unique(),
        default=list(df["Category"].unique())
    )

    filtered_df = df[
        (df["Risk Level"].isin(risk_filter)) &
        (df["Category"].isin(category_filter))
    ]

    if search:
        filtered_df = filtered_df[
            filtered_df["Account"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
            |
            filtered_df["Category"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(filtered_df)

    st.subheader("📊 Transaction Category Chart")

    category_data = df["Category"].value_counts()

    fig1, ax1 = plt.subplots()

    ax1.bar(
        category_data.index,
        category_data.values
    )

    ax1.set_xlabel("Category")
    ax1.set_ylabel("Number of Transactions")
    ax1.set_title("Transaction Category Distribution")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)

    st.subheader("📈 Daily Transaction Trend")

    daily_transactions = df.groupby("Date")["Amount"].sum()

    fig2, ax2 = plt.subplots()

    ax2.plot(
        daily_transactions.index,
        daily_transactions.values,
        marker="o"
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Total Transaction Amount")
    ax2.set_title("Daily Transaction Trend")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    st.subheader("💰 Top 10 Highest Transactions")

    top_10 = df.nlargest(10, "Amount")

    fig3, ax3 = plt.subplots()

    ax3.barh(
        top_10["Account"].astype(str),
        top_10["Amount"]
    )

    ax3.set_xlabel("Transaction Amount")
    ax3.set_ylabel("Account")
    ax3.set_title("Top 10 Highest Transactions")

    plt.tight_layout()

    st.pyplot(fig3)

    st.subheader("⚠️ Suspicious Accounts")

    suspicious_account_table = (
        account_frequency[
            account_frequency >= frequency_threshold
        ]
        .reset_index()
    )

    suspicious_account_table.columns = [
        "Account",
        "Transaction Count"
    ]

    st.dataframe(suspicious_account_table)

    st.subheader("🚨 Suspicious Transactions")

    st.dataframe(suspicious_transactions)

    st.subheader("📥 Export Suspicious Transactions")

    suspicious_csv = suspicious_transactions.to_csv(index=False)

    st.download_button(
        label="Download Suspicious Transactions CSV",
        data=suspicious_csv,
        file_name="suspicious_transactions.csv",
        mime="text/csv"
    )

    st.subheader("📥 Export Complete Analysis")

    complete_csv = df.to_csv(index=False)

    st.download_button(
        label="Download Complete Transaction Report",
        data=complete_csv,
        file_name="fraud_detection_report.csv",
        mime="text/csv"
    )

