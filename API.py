import requests
import json
import time

# Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"  # Replace with your actual API key


# Function to fetch stock data from Alpha Vantage
def fetch_stock_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "GLOBAL_QUOTE"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if "Global Quote" in data:
            return data["Global Quote"]
        else:
            print(f"No data found for {symbol}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching stock data for {symbol}: {e}")
        return None


# Fetch data for all available stock symbols and store it in a dictionary
all_stock_symbols = [
    "AAPL",
    "GOOGL",
    "MSFT",
    "AMZN",
    "TSLA",
    "FB",
    "NVDA",
    "NFLX",
    "PYPL",
    "V",
]
stock_data = {}

for symbol in all_stock_symbols:
    data = fetch_stock_data(symbol)
    if data:
        stock_price = data.get("05. price")
        if stock_price:
            stock_data[symbol] = {
                "name": symbol,  # Replace with the actual stock name if available
                "price": float(stock_price),
            }
        else:
            print(f"No stock price found for {symbol}")
    else:
        print(f"Skipping {symbol}")

    time.sleep(15)  # Pause for a short time to avoid exceeding API rate limit

# Save the fetched data to a local JSON file
with open("stock_data2.json", "w") as file:
    json.dump(stock_data, file, indent=2)

print("Stock data fetched and saved to stock_data.json")
