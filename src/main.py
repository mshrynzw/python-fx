# -*- coding: utf-8 -*-
from datetime import datetime
from common import set_log, set_common
from logging import getLogger, config
from src.chart import create_candlestick_chart, create_candlestick_chart_trend
from src.database import create_database, create_symbol_table, upsert_data
from src.metatrader5 import read_data

log_conf = set_log()
config.dictConfig(log_conf)
logger = getLogger(__name__)

common_conf = set_common()

if __name__ == '__main__':
    create_database(common_conf['database'], logger)

    for symbol in common_conf['symbols']:
        create_symbol_table(common_conf['database'], logger, symbol)

    for symbol in common_conf['symbols']:
        for timeframe in common_conf['timeframes']:
            df = read_data(common_conf['num_bars'], common_conf['start_pos'], symbol, timeframe)
            upsert_data(df, logger, symbol, timeframe)

    today = datetime.now().strftime("%Y-%m-%d")
    for symbol in common_conf['symbols']:
        for timeframe in common_conf['timeframes']:
            create_candlestick_chart(common_conf['database'], symbol, timeframe, common_conf['start_date'], today)
            create_candlestick_chart_trend(common_conf['database'], symbol, timeframe, common_conf['start_date'], today, logger)