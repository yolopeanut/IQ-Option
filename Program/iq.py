import logging
import time
from iqoptionapi.stable_api import IQ_Option
import numpy as np
import pandas as pd

def login(verbose=False, iq=None, checkConnection=False):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

    if iq == None:
        print("Trying to connect to IqOption")
        iq = IQ_Option('brandonqltan2001@gmail.com', 'Ru$tydog2001')  # YOU HAVE TO ADD YOUR USERNAME AND PASSWORD
        iq.connect()

    if iq != None:
        while True:
            if iq.check_connect() == False:
                print('Error when trying to connect')
                print(iq)
                print("Retrying")
                iq.connect()
            else:
                if not checkConnection:
                    print('Successfully Connected!')
                break
            time.sleep(3)

    iq.change_balance("PRACTICE")  # or real
    return iq


def higher(iq, Money, Actives):
    done, id = iq.buy(Money, Actives, "call", 1)
    print(Money, id)
    if not done:
        print('Error call')
        print(done, id)
        exit(0)

    return id


def lower(iq, Money, Actives):
    done, id = iq.buy(Money, Actives, "put", 1)
    print(Money, id)

    if not done:
        print('Error put')
        print(done, id)
        exit(0)

    return id


def get_balance(iq):
    return iq.get_balance()


def get_profit(iq):
    return iq.get_all_profit()['EURUSD']['turbo']

def get_candles(iq,pair, candle_freq):
    candles = iq.get_realtime_candles(pair, candle_freq)
    values = {'open': np.array([]),
              'high': np.array([]),
              'low': np.array([]),
              'close': np.array([]),
              'volume': np.array([])}

    for x in candles:
        values['open'] = np.append(values['open'], candles[x]['open'])
        values['high'] = np.append(values['high'], candles[x]['max'])
        values['low'] = np.append(values['low'], candles[x]['min'])
        values['close'] = np.append(values['close'], candles[x]['close'])
        values['volume'] = np.append(values['volume'], candles[x]['volume'])

    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in values.items()]))
    return df, values