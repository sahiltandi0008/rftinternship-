import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Date': [
        '2025-01-01', '2025-01-05', '2025-01-10',
        '2025-02-01', '2025-02-08', '2025-03-01',
        '2025-03-10', '2025-03-15', '2025-04-01'
    ],
    
    'Product': [
        'Laptop', 'Mobile', 'Tablet',
        'Laptop', 'Mobile', 'Tablet',
        'Laptop', 'Mobile', 'Tablet'
    ],
    
    'Region': [
        'North', 'South', 'East',
        'West', 'North', 'South',
        'East', 'West', 'North'
    ],
    
    'Sales': [
        50000, 30000, None,
        45000, 35000, 25000,
        55000, None, 40000
    ]
}

df = pd.DataFrame(data)

print("Original Dataset:\n")
print(df)

df['Sales'] = df['Sales'].fillna(df['Sales'].mean())

print("\nDataset After Handling Missing Values:\n")
print(df)


product_sales = df.groupby('Product')['Sales'].sum()

print("\nTotal Sales Per Product:\n")
print(product_sales)


region_sales = df.groupby('Region')['Sales'].sum()

print("\nRegion-wise Sales Performance:\n")
print(region_sales)


df['Date'] = pd.to_datetime(df['Date'])

date_sales = df.groupby('Date')['Sales'].sum()

plt.figure(figsize=(8,5))
plt.plot(date_sales.index, date_sales.values, marker='o')
plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.grid(True)
plt.show()


plt.figure(figsize=(6,5))
product_sales.plot(kind='bar')

plt.title("Top Products by Sales")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.show()


df['Month'] = df['Date'].dt.month

monthly_sales = df.groupby('Month')['Sales'].sum()

print("\nMonthly Sales:\n")
print(monthly_sales)

growth = monthly_sales.pct_change() * 100

print("\nMonthly Growth Percentage:\n")
print(growth)


best_region = region_sales.idxmax()

print("\nBest Performing Region:", best_region)


print("\nKEY INSIGHTS:")

print("1. Laptop has the highest sales among all products.")
print("2. North region generated strong overall sales.")
print("3. Sales increased significantly in March.")
print("4. Missing values were replaced using average sales.")
print("5. West and North regions performed consistently well.")