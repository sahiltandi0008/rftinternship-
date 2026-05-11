import pandas as pd

df = pd.read_csv("sales.csv")

df["TOTAL"] = df["QUANTITY"] * df["PRICE"]


product_sales = df.groupby("PRODUCT", as_index=False)["TOTAL"].sum()


total_revenue = df["TOTAL"].sum()


top_product = product_sales.loc[product_sales["TOTAL"].idxmax(), "PRODUCT"]


sorted_df = df.sort_values(by="TOTAL", ascending=False)


print("Sales per product:\n", product_sales)
print("\nTotal Revenue:", total_revenue)
print("Top-selling product:", top_product)
print("\nSorted by revenue:\n", sorted_df)