import pandas as pd


data = {
    "Name": ["AMIT", "RIYA", "JOHN"],
    "Math": [80, 90, 60],
    "Science": [70, 88, 65],
    "English": [85, 92, 70]
}

df = pd.DataFrame(data)


df["Average"] = df[["Math", "Science", "English"]].mean(axis=1)


topper = df.loc[df["Average"].idxmax()]


class_avg = df["Average"].mean()
above_avg_count = df[df["Average"] > class_avg].shape[0]


def assign_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    else:
        return "D"

df["Grade"] = df["Average"].apply(assign_grade)

subject_avg = df[["Math", "Science", "English"]].mean()

print("Final DataFrame:\n", df)
print("\nTopper:\n", topper["Name"], "with avg =", topper["Average"])
print("\nStudents above class average:", above_avg_count)
print("\nSubject-wise Average:\n", subject_avg)