import pandas as pd
from pathlib import Path
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import concurrent.futures
import os
import threading
from datetime import datetime

bitcoin_dates_path = Path("amazon_dates.txt")

good_dates = []

if bitcoin_dates_path.exists():
    bitcoin_dates = [date.strip() for date in open(bitcoin_dates_path).readlines()]

for date in bitcoin_dates:
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")

    updated_dt = dt.replace(hour=1, minute=0, second=0, microsecond=0)

    good_dates.append(updated_dt.strftime("%Y-%m-%d %H:%M:%S.%f"))

    print(updated_dt.strftime("%Y-%m-%d %H:%M:%S.%f"))

stock_type = ["AMAZON"] * len(bitcoin_dates)

precentage_change = []

lock = threading.Lock()

def get_stock_info(date):
    try:
        curr_date_info = get_data("amzn", start_date=date, end_date=date, index_as_date=True, interval="1d")
        if curr_date_info.empty:
            print(f"No data for on {date} (likely a non-trading day or holiday).")
        start_price = curr_date_info["open"].values[0]
        end_price = curr_date_info["close"].values[0]

        result = "decrease" if start_price > end_price else "increase"

        with lock:
            precentage_change.append(result)

    except Exception as e:
       print("error")
       with lock:
            precentage_change.append("error")

with concurrent.futures.ThreadPoolExecutor(50) as executor:
     executor.map(get_stock_info, good_dates)

data_dict = {'hour': good_dates, 'stock type': stock_type, "precentage change" : precentage_change}

print(len(bitcoin_dates))
print(len(precentage_change))
print(len(stock_type))

data = pd.DataFrame(data_dict)
data.to_csv(os.getenv('DESTINATION_FILE'))