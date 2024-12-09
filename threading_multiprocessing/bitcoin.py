import pandas as pd
from pathlib import Path
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import concurrent.futures
import os

bitcoin_dates_path = Path(os.getenv('HOURS_PATH'))

if bitcoin_dates_path.exists():
    bitcoin_dates = [date.strip() for date in open(bitcoin_dates_path).readlines()]

stock_type = ["Bitcoin"] * len(bitcoin_dates)

precentage_change = []

def get_stock_info(date):
    curr_date_info = get_data("BTC-USD", start_date=date, end_date=date, index_as_date=True, interval="1d")
    start_price = curr_date_info["open"].values[0]
    end_price = curr_date_info["close"].values[0]

    if start_price > end_price:
        precentage_change.append("decrease")
    else:
        precentage_change.append("increase")

with concurrent.futures.ThreadPoolExecutor(50) as executor:
    executor.map(get_stock_info, bitcoin_dates)

data_dict = {'hour': bitcoin_dates, 'stock type': stock_type, "precentage change" : precentage_change}

data = pd.DataFrame(data_dict)
data.to_csv(os.getenv('DESTINATION_FILE'))