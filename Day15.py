import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [120, 150, 180, 170, 200, 350]   
}

df = pd.DataFrame(data)

plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.plot(df["Month"], df["Sales"], marker='o')
plt.title("Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

max_sale = df["Sales"].max()
max_month = df[df["Sales"] == max_sale]["Month"].values[0]

plt.annotate(
    "Outlier",
    xy=(max_month, max_sale),
    xytext=(max_month, max_sale - 80),
    arrowprops=dict(facecolor='black', shrink=0.05)
)

plt.subplot(1, 3, 2)
plt.bar(df["Month"], df["Sales"])
plt.title("Sales Comparison")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.subplot(1, 3, 3)
plt.hist(df["Sales"], bins=5)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")

plt.tight_layout()

plt.show()