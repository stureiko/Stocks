import pandas as pd
import yaml
import mysql.connector
import os


def save_data_to_db():
    config = yaml.load(open('../Keys/MySQL.key'), Loader=yaml.SafeLoader)[0]

    main_path = '../data/raw/'

    for symbol_name in ['eth-usdt', 'btc-usdt']:
        for file_name in [f for f in os.listdir(main_path + symbol_name + '/') if
                          os.path.isfile(main_path + symbol_name + '/' + f)]:
            data_path = main_path + symbol_name + '/' + file_name
            df = pd.read_csv(data_path, index_col=0)

            df.drop(columns=['close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'], axis=1,
                    inplace=True)
            df = df.rename(columns={'open_time': 'date'})

            mydb = mysql.connector.connect(**config)
            cursor = mydb.cursor()

            sql_q = "insert into stocks_data ("
            sql_q += 'symbol, '
            for ind, name in enumerate(df.columns):
                sql_q += str(name)
                if ind != len(df.columns) - 1:
                    sql_q += ', '

            sql_q += ') values (' + '%s, ' * (len(df.columns)) + '%s)'
            try:
                for i in range(0, df.shape[0]):
                    val = [symbol_name]
                    val += tuple(df.iloc[i].values)
                    cursor.execute(sql_q, val)

            finally:
                mydb.commit()
                cursor.close()
                mydb.close()


def main():
    save_data_to_db()


if __name__ == "__main__":
    main()
