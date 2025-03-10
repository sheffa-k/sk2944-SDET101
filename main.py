#Sheffa Kochay
#SDET 101
#February 24, 2025

#6
# this Python script fetches and visualizes stock price data for Kohl's Corporation using the Alpha Vantage API, 
# retrieves the last 30 days of closing prices, calculates the average closing price, and plots the trend on a graph


#import libraries   
import os #access enviornment variables
import requests #data from API
import matplotlib.pyplot as plt #data visualization 
from dotenv import load_dotenv #load API keys from my .env file

# Load API keys from .env file
load_dotenv() #retrieve API key from a separate.env file. This keeps sensitive information secure instead of hardcoding it in the script
API_KEY = os.getenv("ALPHA_VANTAGE_KEY") #fetches api of the variable alpha vantage key from my .env file
SYMBOL = "KSS"  # Kohl's Corp, selected stock, defining stock symbol

# Fetch stock data 
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"
response = requests.get(url).json()

# Check if the response contains the expected data
if "Time Series (Daily)" in response:
    time_series = response["Time Series (Daily)"]
    dates = list(time_series.keys())[:30]  # Get last 30 days if the data is found
    closing_prices = [float(time_series[date]["4. close"]) for date in dates]

    # Calculate average closing price
    avg_price = sum(closing_prices) / len(closing_prices)

    # Plot stock prices, using matplotlib
    plt.plot(dates[::-1], closing_prices[::-1], marker="o", label="Closing Price") #plot the closing prices over time with markers 
    plt.axhline(avg_price, color="red", linestyle="dashed", label=f"Avg Price: ${avg_price:.2f}") #add a dashed red line to indicate the average closing price for better visualization
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.title(f"{SYMBOL} Stock Prices (Last 30 Days)")
    plt.legend()
    plt.show()
else:
    print("Error fetching stock data:", response) #handling errors, if API request fails or doesn't return expected data, error message returns instead of crashing

# Analysis of stock price trends:
# Kohl's (KSS) stock has had ups and downs recently. These changes could be because of things like earnings reports, news about the company, or changes in the economy.
# Big price jumps usually happen when there’s important news or reports about the company’s performance.
# Looking at these changes can help us understand what’s affecting the stock price right now.

# graph shows patterns in Kohl's stock movement, over the last 30 days, red dashed line represents the average closing price
#subplot configuration tool is built in feature of matplotlib in VS Code
