# -*- coding: utf-8 -*-
from common import set_log, set_common
from logging import getLogger, config
import MetaTrader5 as mt5

from src.chart import create_candlestick_chart
from src.database import create_database, create_symbol_table, upsert_data
from src.metatrader5 import read_data

log_conf = set_log()
config.dictConfig(log_conf)
logger = getLogger(__name__)

common_conf = set_common()

if __name__ == '__main__':
    # create_database(logger)

    # create_symbol_table(logger, "usdjpy")

    # df = read_data(1000, 0, "USDJPY", mt5.TIMEFRAME_D1)
    # upsert_data(df, logger, "usdjpy", "D1")
    create_candlestick_chart('D1', '2020-01-01', '2024-09-11')