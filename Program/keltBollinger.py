from talib import ATR, EMA, BBANDS


def atr(values, period):
    return ATR(values['high'], values['low'], values['close'],period)

def keltner(values):
    period = 20
    offset = 1.2
    ema = EMA(values['close'], timeperiod=period)
    upperb = ema + offset * atr(values, period)
    lowerb = ema - offset * atr(values, period)
    return upperb, lowerb, ema

def bollinger(values):
    upperband, middleband, lowerband = BBANDS(values['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    return upperband,middleband,lowerband

