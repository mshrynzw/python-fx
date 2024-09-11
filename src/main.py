# -*- coding: utf-8 -*-
from common import set_log, set_common
from logging import getLogger, config
import yfinance as yf


log_conf = set_log()
config.dictConfig(log_conf)
logger = getLogger(__name__)

common_conf = set_common()

if __name__ == '__main__':
    usdjpy = yf.Ticker("USDJPY=X")
    data = usdjpy.history(period="3mo")
    logger.info("Open:\n{}\nClose:\n{}\nHigh:\n{}\nLow:\n{}".format(
        data['Open'].to_string(),
        data['Close'].to_string(),
        data['High'].to_string(),
        data['Low'].to_string()
    ))