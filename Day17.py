import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Customer_ID": [101,102,103,104,105,106,107,108,109,110],
    "Age": [22,35,26,45,52,23,40,36,28,50],
    "Spending": [2000,7000,3000,12000,15000,2500,8000,6000,4000,14000],
    "Visits": [5,12,4,20,25,3,15,10,6,22]
}

df = pd.DataFrame(data)

print("Customer Dataset:\n")
print(df)

def segment(spending):
    if spending >= 10000:
        return "High"
    elif spending >= 5000:
        return "Medium"
    else:
        return "Low"

df["Segment"] = df["Spending"].apply(segment)

print("\nCustomer Segments:\n")
print(df[["Customer_ID", "Spending", "Segment"]])

high_value = df[df["Segment"] == "High"]

print("\nHigh Value Customers:\n")
print(high_value)

low_engagement = df[df["Visits"] < 5]

print("\nLow Engagement Users:\n")
print(low_engagement)

group_data = df.groupby("Segment")["Spending"].mean()

print("\nAverage Spending by Segment:\n")
print(group_data)

plt.figure(figsize=(7,5))
plt.hist(df["Spending"], bins=5)
plt.title("Spending Distribution")
plt.xlabel("Spending")
plt.ylabel("Number of Customers")
plt.show()

segment_count = df["Segment"].value_counts()

plt.figure(figsize=(6,6))
plt.pie(segment_count, labels=segment_count.index, autopct='%1.1f%%')
plt.title("Customer Categories")
plt.show()

print("\nBusiness Strategies:")
print("1. Offer premium rewards to High-value customers.")
print("2. Give discounts and offers to Medium customers.")
print("3. Run engagement campaigns for Low-engagement users.")
print("4. Provide personalized recommendations based on spending behavior.")