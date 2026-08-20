import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("sale_data.csv")

print("Original Dataset:")
print(df.head())

print("\nDataset Information:")
print(df.info())


print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna()

df = df.drop_duplicates()

print("\nDataset after Cleaning:")
print(df.head())

print("\nTotal Rows after Cleaning:", len(df))


df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")


total_sales = df["Sales"].sum()
average_revenue = df["Revenue"].mean()

print("\n--- Sales Summary ---")
print("Total Sales:", total_sales)
print("Average Revenue:", round(average_revenue, 2))


top_customers = (
    df.groupby("Customer")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\n--- Top 5 Customers ---")
print(top_customers)


sales_trend = df.groupby("Date")["Sales"].sum()

plt.figure(figsize=(10, 5))
plt.plot(sales_trend.index, sales_trend.values, marker="o")

plt.title("Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 5))
plt.bar(top_products.index, top_products.values)

plt.title("Top Products by Sales")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


category_distribution = df.groupby("Category")["Sales"].sum()

plt.figure(figsize=(7, 7))
plt.pie(
    category_distribution.values,
    labels=category_distribution.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Category Distribution")
plt.tight_layout()
plt.show()


best_customer = top_customers.index[0]
best_product = top_products.index[0]
best_category = category_distribution.idxmax()

best_sales_date = sales_trend.idxmax()
highest_daily_sales = sales_trend.max()

print("\n========== 5 BUSINESS INSIGHTS ==========")

print(
    f"1. {best_customer} is the top customer based on total revenue."
)

print(
    f"2. {best_product} is the best-selling product based on total sales."
)

print(
    f"3. {best_category} is the highest-performing product category."
)

print(
    f"4. The highest sales were recorded on {best_sales_date.date()}, "
    f"with total sales of {highest_daily_sales:.2f}."
)

print(
    f"5. The average revenue per transaction is "
    f"{average_revenue:.2f}."
)