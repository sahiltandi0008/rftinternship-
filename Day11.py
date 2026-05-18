import matplotlib.pyplot as plt

dates = ["MON", "TUE", "WED", "THU", "FRI"]
sales = [200, 250, 300, 280, 350]

highest_sale = max(sales)
lowest_sale = min(sales)

highest_day = dates[sales.index(highest_sale)]
lowest_day = dates[sales.index(lowest_sale)]

plt.plot(dates, sales, marker='o', linewidth=2)

plt.scatter(highest_day, highest_sale, label="Highest Sale")
plt.scatter(lowest_day, lowest_sale, label="Lowest Sale")

plt.title("Sales Trend Analysis")
plt.xlabel("Days")
plt.ylabel("Sales")

for i in range(len(dates)):
    plt.text(dates[i], sales[i], sales[i])

plt.legend()

plt.grid(True)

plt.show()