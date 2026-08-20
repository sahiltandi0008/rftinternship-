import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("employee_performance.csv")

print("\n===== EMPLOYEE PERFORMANCE DATA =====")
print(df)

df = df.drop_duplicates()

df = df.dropna()

print("\n===== CLEANED DATA =====")
print(df)


department_avg = (
    df.groupby("Department")["Performance_Score"]
    .mean()
    .sort_values(ascending=False)
)

print("\n===== DEPARTMENT-WISE AVERAGE PERFORMANCE =====")
print(department_avg)


top_10 = df.sort_values(
    by="Performance_Score",
    ascending=False
).head(10)

print("\n===== TOP 10 PERFORMERS =====")
print(top_10[
    ["Employee_ID", "Employee_Name",
     "Department", "Performance_Score", "Attendance"]
])


low_attendance = df[df["Attendance"] < 75]

print("\n===== EMPLOYEES WITH ATTENDANCE BELOW 75% =====")
print(low_attendance[
    ["Employee_ID", "Employee_Name",
     "Department", "Attendance"]
])


plt.figure(figsize=(10, 6))

plt.bar(
    df["Employee_Name"],
    df["Performance_Score"]
)

plt.title("Employee Performance Comparison")
plt.xlabel("Employee")
plt.ylabel("Performance Score")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("performance_comparison.png")
plt.show()


plt.figure(figsize=(10, 6))

plt.plot(
    df["Employee_Name"],
    df["Attendance"],
    marker="o"
)

plt.axhline(
    y=75,
    linestyle="--",
    label="75% Attendance"
)

plt.title("Employee Attendance Trend")
plt.xlabel("Employee")
plt.ylabel("Attendance (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("attendance_trend.png")
plt.show()


department_count = df["Department"].value_counts()

plt.figure(figsize=(7, 7))

plt.pie(
    department_count,
    labels=department_count.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Department Distribution")
plt.tight_layout()

plt.savefig("department_distribution.png")
plt.show()


df["Performance_Category"] = pd.cut(
    df["Performance_Score"],
    bins=[0, 60, 75, 90, 100],
    labels=[
        "Poor",
        "Average",
        "Good",
        "Excellent"
    ]
)

df["Attendance_Status"] = df["Attendance"].apply(
    lambda x: "Low Attendance" if x < 75 else "Good Attendance"
)

df.to_csv(
    "employee_performance_final_report.csv",
    index=False
)

print("\n===================================")
print("FINAL REPORT EXPORTED SUCCESSFULLY!")
print("File: employee_performance_final_report.csv")
print("===================================")