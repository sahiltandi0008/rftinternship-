import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

st.set_page_config(page_title="Weather Data Analytics", layout="wide")

st.title("🌦 Weather Data Analytics System")

file = st.file_uploader("Upload Weather CSV File", type=["csv"])

if file is not None:

    df = pd.read_csv(file)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    st.subheader("Weather Data")
    st.dataframe(df)

    average_temperature = df.groupby("City")["Temperature"].mean().sort_values(ascending=False)

    hottest_city = average_temperature.idxmax()
    hottest_temperature = average_temperature.max()

    coldest_city = average_temperature.idxmin()
    coldest_temperature = average_temperature.min()

    rainy_days = (df["Weather"].str.lower() == "rainy").sum()
    sunny_days = (df["Weather"].str.lower() == "sunny").sum()

    st.subheader("Weather Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Hottest City", hottest_city)
    col2.metric("Hottest Temperature", f"{hottest_temperature:.2f} °C")
    col3.metric("Coldest City", coldest_city)
    col4.metric("Coldest Temperature", f"{coldest_temperature:.2f} °C")

    st.write("Rainy Days:", rainy_days)
    st.write("Sunny Days:", sunny_days)

    st.subheader("🌡 Temperature Trend")

    fig1, ax1 = plt.subplots()

    for city in df["City"].unique():
        city_data = df[df["City"] == city]
        ax1.plot(
            city_data["Date"],
            city_data["Temperature"],
            marker="o",
            label=city
        )

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title("Temperature Trend")
    ax1.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)

    st.subheader("🌧 Weather Distribution")

    weather_distribution = df["Weather"].value_counts()

    fig2, ax2 = plt.subplots()

    ax2.pie(
        weather_distribution.values,
        labels=weather_distribution.index,
        autopct="%1.1f%%"
    )

    ax2.set_title("Weather Distribution")

    st.pyplot(fig2)

    st.subheader("📊 Average Temperature per City")

    fig3, ax3 = plt.subplots()

    ax3.bar(
        average_temperature.index,
        average_temperature.values
    )

    ax3.set_xlabel("City")
    ax3.set_ylabel("Average Temperature (°C)")
    ax3.set_title("Average Temperature per City")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig3)

    st.subheader("⭐ Tomorrow's Temperature Prediction")

    predictions = []

    for city in df["City"].unique():

        city_data = df[df["City"] == city]

        moving_average = city_data["Temperature"].tail(3).mean()

        predictions.append({
            "City": city,
            "Average Temperature": city_data["Temperature"].mean(),
            "Tomorrow Prediction": moving_average
        })

    report = pd.DataFrame(predictions)

    st.dataframe(report)

    selected_city = st.selectbox(
        "Select City for Tomorrow's Prediction",
        df["City"].unique()
    )

    selected_data = df[df["City"] == selected_city]

    prediction = selected_data["Temperature"].tail(3).mean()

    st.success(
        f"Predicted temperature for {selected_city} tomorrow: "
        f"{prediction:.2f} °C"
    )

    st.subheader("📥 Export Final Report")

    report["Hottest City"] = hottest_city
    report["Coldest City"] = coldest_city
    report["Rainy Days"] = rainy_days
    report["Sunny Days"] = sunny_days

    csv = report.to_csv(index=False)

    st.download_button(
        label="Download Final Weather Report",
        data=csv,
        file_name="weather_final_report.csv",
        mime="text/csv"
    )