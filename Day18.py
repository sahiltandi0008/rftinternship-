import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Movie_Name": ["Inception", "Avatar", "Titanic", "Joker", "Avengers"],
    "Rating": [8.8, 7.9, 7.8, 8.4, 8.5],
    "Genre": ["Sci-Fi", "Action", "Romance", "Drama", "Action"],
    "Revenue": [836, 2847, 2201, 1074, 2798]
}

df = pd.DataFrame(data)

print("Movie Dataset:\n")
print(df)

highest_rated = df.sort_values(by="Rating", ascending=False)
print("\nHighest Rated Movies:\n")
print(highest_rated[["Movie_Name", "Rating"]])

genre_revenue = df.groupby("Genre")["Revenue"].sum()
print("\nMost Profitable Genres:\n")
print(genre_revenue)

top5 = df.sort_values(by="Revenue", ascending=False).head(5)
print("\nTop 5 Movies by Revenue:\n")
print(top5[["Movie_Name", "Revenue"]])

correlation = df["Rating"].corr(df["Revenue"])
print("\nCorrelation between Rating and Revenue:", correlation)

plt.figure(figsize=(6,5))
genre_revenue.plot(kind="bar")
plt.title("Genre vs Revenue")
plt.xlabel("Genre")
plt.ylabel("Revenue")
plt.show()

plt.figure(figsize=(6,5))
plt.hist(df["Rating"], bins=5)
plt.title("Rating Distribution")
plt.xlabel("Ratings")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(6,5))
plt.scatter(df["Rating"], df["Revenue"])
plt.title("Rating vs Revenue")
plt.xlabel("Rating")
plt.ylabel("Revenue")
plt.show()