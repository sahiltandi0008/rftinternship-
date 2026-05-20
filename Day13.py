import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


marks = [45, 56, 67, 78, 89, 90, 55, 60, 72, 85,
         95, 40, 50, 65, 70, 88, 92, 58, 76, 81]


df = pd.DataFrame({"Marks": marks})

print(df)

plt.figure(figsize=(8,5))

sns.histplot(df["Marks"], kde=True, bins=8)

plt.title("Distribution of Student Marks")
plt.xlabel("Marks")
plt.ylabel("Frequency")

plt.show()

skewness = df["Marks"].skew()

print("Skewness Value:", skewness)

if skewness > 0:
    print("The data is Positively Skewed")
elif skewness < 0:
    print("The data is Negatively Skewed")
else:
    print("The data is Normally Distributed")