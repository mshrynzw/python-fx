import pandas as pd
import MetaTrader5 as mt5


def read_data(num_bars, start_pos, symbol, timeframe):
    # MT5に接続
    if not mt5.initialize():
        print("MT5への接続に失敗しました")
        quit()

    # シンボルとタイムフレームを指定してデータを取得
    rates = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, num_bars)

    # データをPandasのDataFrameに変換
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # MT5との接続を閉じる
    mt5.shutdown()

    return df