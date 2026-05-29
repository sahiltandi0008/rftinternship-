import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sales_data.csv')

print(df.isnull().sum())
df.drop(columns=["Region_and_Sales_Rep"],inplace=True)

df['Sale_Date']=pd.to_datetime(df['Sale_Date'])
print("Cleaned dataset:\n",df)


print("Total sales:",df["Sales_Amount"].sum())
print("Total quantity sold:",df["Quantity_Sold"].sum())

region_sales=df.groupby("Region")["Sales_Amount"].sum()
print("REGION-WISE SALES:\n",region_sales)

top_sold=df.groupby("Product_Category")["Sales_Amount"].sum()
print("TOP SOLD CATEGORIES:\n",top_sold)

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
top_sold.plot(kind="pie",autopct="%1.1f%%")
plt.legend()

plt.subplot(1,2,2)
region_sales.plot(kind='bar',color='yellow')
plt.title("REGION - WISE SALES")
plt.xlabel("Region")
plt.ylabel("Sales_Amount")
plt.tight_layout()
plt.show()

print("INSIGHTS:")
print("1.CLOTHING CATEGORY HAS HIGHEST SALE")
print("2.FOOD CATEGORY HAS LEAST SALES")
print("3.NORTH REGION HAS HIGHEST SALES")
print("4.SOUTH REGION HAS LEAST SALES")