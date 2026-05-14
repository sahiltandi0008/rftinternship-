import pandas as pd

data = {
    "Name": ["Aman", "Riya", "Karan", "Neha", "Raj"],
    "Age": [25, 32, 28, 24, 35],
    "Salary": [60000, 45000, 52000, 70000, 48000]
}

df = pd.DataFrame(data)


filtered_df = df[(df["Salary"] > 50000) & (df["Age"] < 30)]


print("Filtered Data:")
print(filtered_df)


filtered_df.to_csv("filtered_data.csv", index=False)