import requests
import config

def get_stock_price(symbol, interval):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': "TIME_SERIES_INTRADAY",
        'symbol': symbol,
        'interval' : interval,
        "apikey": config.API_KEY, 
    }

    print("Getting data from api call......")
    response = requests.get(base_url, params=params)
    data = response.json()
    if "Error Message" in data:
        print(f"Error in API CALLING: {data['Error Message']}")
        return None, None 
    
    try:
        time_series_key = f"Time Series ({interval})"
        time_series_data = data[time_series_key]
        
        latest_timestamp = list(time_series_data.keys())[0]
        latest_price_entry = time_series_data[latest_timestamp]
        

        latest_price = float(latest_price_entry['4. close']) 
        
        return latest_price, latest_timestamp
    
    except KeyError:
        print(f"we Could not find key {time_series_key} in the response.")
        return None, None


if __name__ == "__main__":
    symbol = str(input("Enter your stock symbol/company name: "))
    interval = input("Enter your time interval in min: ")
    interval_string = f"{interval}min"

    # Call the function and capture its results
    price, time = get_stock_price(symbol, interval_string)
    
    if price is not None and time is not None:
        print("-" * 30)
        print(f"Latest price for {symbol.upper()} at {time} is: ${price:.2f}")
