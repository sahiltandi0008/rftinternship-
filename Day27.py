import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(
    page_title="Social Media Trend Analyzer",
    layout="wide"
)

st.title("📱 Social Media Trend Analyzer")

uploaded_file = st.file_uploader(
    "Upload Social Media CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Likes"] = pd.to_numeric(df["Likes"], errors="coerce").fillna(0)
    df["Comments"] = pd.to_numeric(df["Comments"], errors="coerce").fillna(0)
    df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce").fillna(0)

    df["Engagement"] = (
        df["Likes"] +
        df["Comments"] +
        df["Shares"]
    )

    def extract_hashtags(text):
        return re.findall(r"#\w+", str(text).lower())

    all_hashtags = []

    for text in df["Hashtags"]:
        all_hashtags.extend(extract_hashtags(text))

    hashtag_counts = pd.Series(all_hashtags).value_counts()

    top_hashtags = hashtag_counts.head(10)

    active_users = df["User"].value_counts()

    top_active_users = active_users.head(10)

    total_likes = int(df["Likes"].sum())
    total_comments = int(df["Comments"].sum())
    total_shares = int(df["Shares"].sum())
    total_engagement = int(df["Engagement"].sum())

    posting_time = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce")

    df["Posting Hour"] = posting_time.dt.hour

    popular_time = df["Posting Hour"].value_counts().idxmax()

    daily_engagement = df.groupby("Date")["Engagement"].sum()

    category_distribution = df["Category"].value_counts()

    positive_words = [
        "good",
        "great",
        "amazing",
        "excellent",
        "happy",
        "love",
        "awesome",
        "best",
        "wonderful",
        "success",
        "beautiful",
        "fantastic"
    ]

    negative_words = [
        "bad",
        "worst",
        "hate",
        "sad",
        "angry",
        "poor",
        "terrible",
        "awful",
        "disappointed",
        "fail",
        "failure",
        "boring"
    ]

    def sentiment_analysis(text):
        text = str(text).lower()

        positive_score = sum(
            word in text for word in positive_words
        )

        negative_score = sum(
            word in text for word in negative_words
        )

        if positive_score > negative_score:
            return "Positive"

        if negative_score > positive_score:
            return "Negative"

        return "Neutral"

    df["Sentiment"] = df["Text"].apply(sentiment_analysis)

    sentiment_distribution = df["Sentiment"].value_counts()

    st.subheader("📊 Social Media Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Posts",
        len(df)
    )

    col2.metric(
        "Total Likes",
        total_likes
    )

    col3.metric(
        "Total Comments",
        total_comments
    )

    col4.metric(
        "Total Shares",
        total_shares
    )

    st.metric(
        "Total Engagement",
        total_engagement
    )

    st.metric(
        "Most Popular Posting Hour",
        f"{popular_time}:00"
    )

    st.subheader("🔎 Search & Filters")

    search = st.text_input(
        "Search User, Hashtag or Post"
    )

    category_filter = st.multiselect(
        "Select Content Categories",
        df["Category"].unique(),
        default=list(df["Category"].unique())
    )

    sentiment_filter = st.multiselect(
        "Select Sentiment",
        ["Positive", "Neutral", "Negative"],
        default=["Positive", "Neutral", "Negative"]
    )

    filtered_df = df[
        (df["Category"].isin(category_filter)) &
        (df["Sentiment"].isin(sentiment_filter))
    ]

    if search:

        search_mask = (
            filtered_df["User"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
            |
            filtered_df["Hashtags"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
            |
            filtered_df["Text"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
        )

        filtered_df = filtered_df[search_mask]

    st.subheader("📋 Filtered Posts")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.subheader("🔥 Top Trending Hashtags")

    st.dataframe(
        top_hashtags.reset_index(
            name="Posts"
        ),
        use_container_width=True
    )

    fig1, ax1 = plt.subplots()

    ax1.bar(
        top_hashtags.index,
        top_hashtags.values
    )

    ax1.set_xlabel("Hashtag")
    ax1.set_ylabel("Number of Posts")
    ax1.set_title("Top 10 Trending Hashtags")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)

    st.subheader("👥 Most Active Users")

    st.dataframe(
        top_active_users.reset_index(
            name="Post Count"
        ),
        use_container_width=True
    )

    st.subheader("📈 Daily Engagement Trend")

    fig2, ax2 = plt.subplots()

    ax2.plot(
        daily_engagement.index,
        daily_engagement.values,
        marker="o"
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Engagement")
    ax2.set_title("Daily Engagement Trend")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    st.subheader("🥧 Content Category Distribution")

    fig3, ax3 = plt.subplots()

    ax3.pie(
        category_distribution.values,
        labels=category_distribution.index,
        autopct="%1.1f%%"
    )

    ax3.set_title("Content Category Distribution")

    st.pyplot(fig3)

    st.subheader("😊 Sentiment Analysis")

    st.dataframe(
        sentiment_distribution.reset_index(
            name="Post Count"
        ),
        use_container_width=True
    )

    fig4, ax4 = plt.subplots()

    ax4.bar(
        sentiment_distribution.index,
        sentiment_distribution.values
    )

    ax4.set_xlabel("Sentiment")
    ax4.set_ylabel("Number of Posts")
    ax4.set_title("Sentiment Distribution")

    st.pyplot(fig4)

    st.subheader("📊 Engagement Analysis")

    engagement_report = pd.DataFrame({
        "Metric": [
            "Likes",
            "Comments",
            "Shares"
        ],
        "Total": [
            total_likes,
            total_comments,
            total_shares
        ]
    })

    st.dataframe(
        engagement_report,
        use_container_width=True
    )

    st.subheader("📥 Export Analytics Report")

    analytics_report = df.copy()

    report_csv = analytics_report.to_csv(
        index=False
    )

    st.download_button(
        label="Download Analytics Report",
        data=report_csv,
        file_name="social_media_analytics_report.csv",
        mime="text/csv"
    )

