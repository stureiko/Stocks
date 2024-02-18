import datetime as dt
import json
import requests
import pandas as pd
from dateutil.relativedelta import relativedelta


def get_binance_data(symbol='ETHUSDT', interval='1h', start_date: str = None):
    # Define the start and end times for the data
    if start_date:
        start_time = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end_time = start_time + relativedelta(months=1)
    else:
        end_time = dt.datetime.now()
        start_time = end_time + relativedelta(months=-1)

    # Convert the times to Unix timestamps in milliseconds
    start_timestamp = int(start_time.timestamp() * 1000)
    end_timestamp = int(end_time.timestamp() * 1000)

    # Define the Binance API endpoint for K-line data
    endpoint = 'https://api.binance.com/api/v3/klines'

    # Define the parameters for the API request
    symbol = symbol
    interval = interval
    limit = 10000
    params = {'symbol': symbol, 'interval': interval, 'startTime': start_timestamp, 'endTime': end_timestamp,
              'limit': limit}

    response = requests.get(endpoint, params=params)
    klines = json.loads(response.text)
    data = pd.DataFrame(klines)
    data.columns = ['open_time',
                    'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'qav', 'num_trades',
                    'taker_base_vol', 'taker_quote_vol', 'ignore']
    data.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in data.open_time]
    data['open_time'] = [dt.datetime.fromtimestamp(x / 1000.) for x in data.open_time]
    data['close_time'] = [dt.datetime.fromtimestamp(x / 1000.) for x in data.close_time]
    data.drop(data.tail(1).index, inplace=True)
    return data


def load_data():
    start_date = (dt.datetime.today() - relativedelta(months=1)).__str__().split(' ')[0][:-2] + '01'
    while int(start_date[:4]) > 2017:
        df = get_binance_data(symbol='BTCUSDT', start_date=start_date)
        file_name = '../data/raw/btc-usdt/' + start_date + '.csv'
        df.to_csv(file_name)
        print(f'file {file_name} wrote.')
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(months=-1)
        start_date = start_date.__str__().split(' ')[0][:-2] + '01'


def main():
    load_data()


if __name__ == '__main__':
    main()
