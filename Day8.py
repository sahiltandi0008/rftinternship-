import pandas as pd

data = {
    "Name": ["A", "B", "C", "D"],
    "Dept": ["IT", "HR", "IT", "HR"],
    "Salary": [50000, 40000, 60000, 45000]
}

df = pd.DataFrame(data)


avg_salary = df.groupby("Dept")["Salary"].mean()
print("Average Salary:\n", avg_salary)


highest_paid = df.loc[df.groupby("Dept")["Salary"].idxmax()]
print("\nHighest Paid Employee:\n", highest_paid)


count_emp = df.groupby("Dept")["Name"].count()
print("\nEmployee Count:\n", count_emp)


sorted_avg = avg_salary.sort_values(ascending=False)
print("\nSorted by Avg Salary:\n", sorted_avg)