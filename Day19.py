import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Date': [
        '2024-01-01','2024-01-02','2024-01-03','2024-01-04',
        '2024-01-05','2024-01-06','2024-01-07','2024-01-08',
        '2024-01-09','2024-01-10'
    ],
    'Stock_Price': [100, 102, 101, 105, 107, 106, 110, 108, 111, 115]
}

df = pd.DataFrame(data)

df['Date'] = pd.to_datetime(df['Date'])

df['Moving_Average'] = df['Stock_Price'].rolling(window=3).mean()

peak = df[df['Stock_Price'] == df['Stock_Price'].max()]
drop = df[df['Stock_Price'] == df['Stock_Price'].min()]

print("Peak Price:")
print(peak)

print("\nLowest Price:")
print(drop)

volatility = df['Stock_Price'].std()
print("\nVolatility:", volatility)

plt.figure(figsize=(10,5))

plt.plot(df['Date'], df['Stock_Price'], marker='o', label='Stock Price')
plt.plot(df['Date'], df['Moving_Average'], marker='s', label='Moving Average')

plt.title("Stock Price Time Series Analysis")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)

plt.show()