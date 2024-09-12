# -*- coding: utf-8 -*-
from common import set_log, set_common
from logging import getLogger, config
from src.chart import create_candlestick_chart
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

    for symbol in common_conf['symbols']:
        for timeframe in common_conf['timeframes']:
            create_candlestick_chart(common_conf['database'], symbol, timeframe, '2020-01-01', '2024-09-11')