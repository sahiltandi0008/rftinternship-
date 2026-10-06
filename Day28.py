
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Market Portfolio Analyzer",
    layout="wide"
)

st.title("📈 Stock Market Portfolio Analyzer")

uploaded_file = st.file_uploader(
    "Upload Stock Price CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Buy Price"] = pd.to_numeric(df["Buy Price"], errors="coerce")
    df["Sell Price"] = pd.to_numeric(df["Sell Price"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    df["Investment"] = df["Buy Price"] * df["Quantity"]

    df["Current Value"] = df["Sell Price"] * df["Quantity"]

    df["Profit/Loss"] = (
        df["Current Value"] -
        df["Investment"]
    )

    df["Return %"] = (
        df["Profit/Loss"] /
        df["Investment"]
    ) * 100

    stock_performance = (
        df.groupby("Stock")
        .agg({
            "Investment": "sum",
            "Current Value": "sum",
            "Profit/Loss": "sum"
        })
        .reset_index()
    )

    stock_performance["Return %"] = (
        stock_performance["Profit/Loss"] /
        stock_performance["Investment"]
    ) * 100

    best_stock = stock_performance.loc[
        stock_performance["Return %"].idxmax()
    ]

    worst_stock = stock_performance.loc[
        stock_performance["Return %"].idxmin()
    ]

    total_investment = df["Investment"].sum()

    total_current_value = df["Current Value"].sum()

    total_profit_loss = (
        total_current_value -
        total_investment
    )

    overall_return = (
        total_profit_loss /
        total_investment
    ) * 100

    df = df.sort_values("Date")

    daily_portfolio = (
        df.groupby("Date")["Current Value"]
        .sum()
        .reset_index()
    )

    daily_portfolio["Daily Return %"] = (
        daily_portfolio["Current Value"]
        .pct_change() * 100
    )

    daily_portfolio["Daily Return %"] = (
        daily_portfolio["Daily Return %"].fillna(0)
    )

    daily_portfolio["Moving Average"] = (
        daily_portfolio["Current Value"]
        .rolling(3)
        .mean()
    )

    latest_value = daily_portfolio["Current Value"].iloc[-1]

    moving_average = (
        daily_portfolio["Current Value"]
        .tail(3)
        .mean()
    )

    if latest_value > moving_average:
        predicted_trend = "📈 Upward Trend"
    elif latest_value < moving_average:
        predicted_trend = "📉 Downward Trend"
    else:
        predicted_trend = "➡️ Stable Trend"

    st.subheader("📊 Portfolio Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Investment",
        f"₹{total_investment:,.2f}"
    )

    col2.metric(
        "Current Value",
        f"₹{total_current_value:,.2f}"
    )

    col3.metric(
        "Profit / Loss",
        f"₹{total_profit_loss:,.2f}"
    )

    col4.metric(
        "Overall Return",
        f"{overall_return:.2f}%"
    )

    st.subheader("🏆 Best & Worst Performing Stocks")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"Best Stock: {best_stock['Stock']} | "
            f"Return: {best_stock['Return %']:.2f}%"
        )

    with col2:
        st.error(
            f"Worst Stock: {worst_stock['Stock']} | "
            f"Return: {worst_stock['Return %']:.2f}%"
        )

    st.subheader("📋 Stock-wise Profit / Loss")

    st.dataframe(
        stock_performance,
        use_container_width=True
    )

    st.subheader("📈 Portfolio Growth Chart")

    fig1, ax1 = plt.subplots()

    ax1.plot(
        daily_portfolio["Date"],
        daily_portfolio["Current Value"],
        marker="o"
    )

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Portfolio Value")
    ax1.set_title("Portfolio Growth")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)

    st.subheader("📊 Sector-wise Investment")

    sector_investment = (
        df.groupby("Sector")["Investment"]
        .sum()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots()

    ax2.bar(
        sector_investment.index,
        sector_investment.values
    )

    ax2.set_xlabel("Sector")
    ax2.set_ylabel("Investment")
    ax2.set_title("Sector-wise Investment")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    st.subheader("📉 Daily Return Analysis")

    fig3, ax3 = plt.subplots()

    ax3.plot(
        daily_portfolio["Date"],
        daily_portfolio["Daily Return %"],
        marker="o"
    )

    ax3.axhline(
        0,
        linestyle="--"
    )

    ax3.set_xlabel("Date")
    ax3.set_ylabel("Daily Return (%)")
    ax3.set_title("Daily Portfolio Return")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig3)

    st.subheader("⭐ Next Day Trend Prediction")

    st.metric(
        "Predicted Trend",
        predicted_trend
    )

    st.write(
        f"Latest Portfolio Value: ₹{latest_value:,.2f}"
    )

    st.write(
        f"3-Day Moving Average: ₹{moving_average:,.2f}"
    )

    st.subheader("📈 Moving Average Analysis")

    fig4, ax4 = plt.subplots()

    ax4.plot(
        daily_portfolio["Date"],
        daily_portfolio["Current Value"],
        marker="o",
        label="Portfolio Value"
    )

    ax4.plot(
        daily_portfolio["Date"],
        daily_portfolio["Moving Average"],
        linestyle="--",
        label="3-Day Moving Average"
    )

    ax4.set_xlabel("Date")
    ax4.set_ylabel("Portfolio Value")
    ax4.set_title("Portfolio Value vs Moving Average")
    ax4.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig4)

    st.subheader("🔎 Search & Filters")

    stock_filter = st.multiselect(
        "Select Stocks",
        df["Stock"].unique(),
        default=list(df["Stock"].unique())
    )

    sector_filter = st.multiselect(
        "Select Sectors",
        df["Sector"].unique(),
        default=list(df["Sector"].unique())
    )

    filtered_df = df[
        (df["Stock"].isin(stock_filter)) &
        (df["Sector"].isin(sector_filter))
    ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.subheader("📥 Export Portfolio Report")

    report_csv = stock_performance.to_csv(
        index=False
    )

    st.download_button(
        label="Download Portfolio Report",
        data=report_csv,
        file_name="stock_portfolio_report.csv",
        mime="text/csv"
    )




