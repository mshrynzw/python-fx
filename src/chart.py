import plotly.graph_objects as go
from src.common import set_common
from src.database import fetch_data


def find_uptrend(df, logger):
    # 単純化のため、20期間の移動平均を使用してトレンドを判断
    df['MA20'] = df['close'].rolling(window=20).mean()
    
    # 上昇トレンドの開始点と終了点を格納するリスト
    uptrends = []
    
    start_idx = None
    for i in range(1, len(df)):
        if df['MA20'].iloc[i] > df['MA20'].iloc[i-1] and start_idx is None:
            start_idx = i
        elif df['MA20'].iloc[i] < df['MA20'].iloc[i-1] and start_idx is not None:
            uptrends.append((start_idx, i-1))
            start_idx = None
    
    if start_idx is not None:
        logger.debug(f'上昇トレンドの終了点を追加します。（開始点: {start_idx} / 終了点: {len(df)-1}')
        uptrends.append((start_idx, len(df)-1))
    
    return uptrends


def create_candlestick_chart(db, symbol, timeframe, start_date, end_date):
    common_conf = set_common()

    df = fetch_data(db, symbol, timeframe, start_date, end_date)

    for sma in common_conf['smas']:
        df['SMA' + str(sma['window'])] = df['close'].rolling(window=sma['window']).mean()
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])

    for sma in common_conf['smas']:
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['SMA' + str(sma['window'])],
            line=dict(color=sma['color'], width=1),
            name='SMA' + str(sma['window'])
        ))
    
    fig.update_layout(
        title=f'{symbol.upper()} {timeframe}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )
    
    fig.show()


def create_candlestick_chart_trend(db, symbol, timeframe, start_date, end_date, logger):
    df = fetch_data(db, symbol, timeframe, start_date, end_date)
    
    # 25日単純移動平均線を計算
    df['SMA25'] = df['close'].rolling(window=25).mean()
    
    # 上昇トレンドを見つける
    uptrends = find_uptrend(df, logger)
    
    fig = go.Figure()

    # ローソク足を追加
    fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='USD/JPY'
    ))

    # 25 SMAを追加
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['SMA25'],
        line=dict(color='blue', width=1),
        name='25 SMA'
    ))
    
    # 上昇トレンドの高値と安値に横線を追加
    for start, end in uptrends:
        trend_high = df['high'].iloc[start:end+1].max()
        trend_low = df['low'].iloc[start:end+1].min()
        
        fig.add_shape(
            type="line",
            x0=df['time'].iloc[start],
            y0=trend_high,
            x1=df['time'].iloc[end],
            y1=trend_high,
            line=dict(color="green", width=2),
            name="Trend High"
        )
        
        fig.add_shape(
            type="line",
            x0=df['time'].iloc[start],
            y0=trend_low,
            x1=df['time'].iloc[end],
            y1=trend_low,
            line=dict(color="red", width=2),
            name="Trend Low"
        )
    
    fig.update_layout(
        title=f'USD/JPY {timeframe} Candlestick Chart with 25 SMA and Uptrends',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    fig.show()