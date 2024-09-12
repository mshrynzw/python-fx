import plotly.graph_objects as go
from src.common import set_common
from src.database import fetch_data


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