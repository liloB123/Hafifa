import pandas as pd
from pathlib import Path
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import concurrent.futures
import os
from enum import Enum
import threading

class Stocks(Enum):
    AMAZON = "amzn"
    BITCOIN = "BTC-USD"
    GOOGLE = "GOOG"

def get_dates(stock: Stocks):
    dates_path = Path(os.getenv(stock.name + "_DATES"))

    if dates_path.exists():
        dates = [date.strip() for date in open(dates_path).readlines()]

    for date in dates:
        date = date.replace()
    
    return dates

stock_type = []
precentage_change = []
hour = []

lock = threading.Lock()

def get_stock_info(stock, date):
    try:
        curr_date_info = get_data(stock, start_date=date, end_date=date, index_as_date=True, interval="1d")
        start_price = curr_date_info["open"].values[0]
        end_price = curr_date_info["close"].values[0]

        result = "decrease" if start_price > end_price else "increase"

        with lock:
            precentage_change.append(result)
            stock_type.append(stock)
            hour.append(date)
    
    except Exception as e:
       print(f"Error occurred while fetching data for {stock} on {date}: {e}")
       with lock:
            precentage_change.append("error")
            stock_type.append("error")
            hour.append("error")

def add_stock(stock: Stocks):
    dates = get_dates(stock)
    stock_date_pairs = [(stock.value, date) for date in dates]
    with concurrent.futures.ThreadPoolExecutor(50) as executor:
        executor.map(lambda args: get_stock_info(args[0], args[1]), stock_date_pairs)

with concurrent.futures.ThreadPoolExecutor(50) as executor:
    executor.map(add_stock, Stocks)

data_dict = {'hour': hour, 'stock type': stock_type, "precentage change" : precentage_change}

print(len(hour))
print(len(stock_type))
print(len(precentage_change))

data = pd.DataFrame(data_dict)
data.to_csv(os.getenv('DESTINATION_FILE'))