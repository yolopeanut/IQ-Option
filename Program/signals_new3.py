from datetime import datetime
from datetime import date
from iq import login, higher, lower, get_candles
from generate import gene2
import time
from keltBollinger import bollinger, keltner


def init():
    iq = login()  # Login to iqoptions
    gene2()  # Generate list
    print("List generated!")
    # Reading signal file
    with open(r"D:\School Files\Program\sigs.txt", 'r') as fp:
        sigs = [line.rstrip('\n').split(" - ") for line in fp]
    print("Done appending into sigs")

    # Initialising file that will log history
    # ==========================================
    today = date.today()
    d1 = today.strftime("%d.%m")
    d1str = d1 + ".txt"
    file = open("D:/School Files/Program/Logs/" + d1str, "a+")
    file_real_acc = open("D:/School Files/Program/Logs/Real/" + d1str, "a+")
    print("Done adding log file")
    # ==========================================

    iq.start_candles_stream("EURUSD", 60, 280)

    return iq, sigs, file, file_real_acc, d1str


def removePastTime(sigs):
    while (True):
        current_time_tmp = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
        time = datetime.strptime(sigs[0][2], "%H:%M")
        if time < current_time_tmp:
            sigs.pop(0)
        else:
            return sigs


def checkTime(sigs):
    current_time = datetime.now().strftime("%H:%M")

    while current_time != sigs[0][2]:
        # while current_time != current_time:
        current_time = datetime.now().strftime("%H:%M")
        print("===============================")
        print("Curr time: ", current_time)
        print("Next time: ", sigs[0][2])
        time.sleep(10)


def checkGreater():
    # ============================================
    # For checking squeeze
    df, values = get_candles(iq,"EURUSD", 60)
    close = df.at[df.index[-2], 'close']
    upperb, lowerb, ema = keltner(values)
    upperband, middleband, lowerband = bollinger(values)
    upperb = round(upperb[-2],5)
    lowerb = round(lowerb[-2],5)
    upperband = round(upperband[-2],5)
    lowerband = round(lowerband[-2],5)

    print(f"     Close: {close}")
    print(f"Upper Band K: {upperb}")
    print(f"Lower Band K: {lowerb}")
    print(f"Upper Band BB: {upperband}")
    print(f"Lower Band BB: {lowerband}")

    if upperb > upperband and lowerb < lowerband:
        print(True)
        return True
    else:
        print(False)
        return False
    # ============================================


# Only does 2 at a time
def call_put(iq, signals, bet_money, num_times):
    def helper(iq, signals, bet_money):
        if call_or_put == "CALL":
            print(signals[0][1])
            result = None
            while result is None:
                try:
                    ids = higher(iq, bet_money, signals[0][1])
                    result = True
                except:
                    pass
            print(signals[0][3])
        else:
            print(signals[0][1])
            result = None
            while result is None:
                try:
                    ids = higher(iq, bet_money, signals[0][1])
                    result = True
                except:
                    pass
            print(signals[0][3])

        return ids

    def helper_checker(wl, ret, bet_money):
        ret2 = ret
        if wl > 0:
            ret2 = ret2 + "Win "
            return ret2, None
        elif wl == 0:
            ret2 = ret2 + "Draw "
            id1 = helper(iq, signals, bet_money)
        elif wl < 0:
            ret2 = ret2 + "Lose "
            id1 = helper(iq, signals, bet_money * 2)
        return ret2, id1

    def helper3(wl, ret, bet_money2, num_times):
        wl_temp = wl
        tries = 1
        bet_money = bet_money2
        while tries != num_times:
            if tries % 2 == 0 and tries != 0:
                signals.pop(0)
                checkTime(signals)

            if checkGreater() == True:

                ret, id = helper_checker(wl_temp, ret, bet_money)  # Second Bet
                wl_temp = iq.check_win_v3(id)  # Check Second bet win

                if wl_temp > 0:
                    ret = ret + "Win "
                    return ret, signals
                elif wl_temp == 0:
                    tries -= 1
                elif wl_temp < 0:
                    bet_money = bet_money * 2

                tries += 1
            else:
                removePastTime(sigs)

        if wl_temp < 0:
            ret = ret + "Lose "

        return ret, signals

    call_or_put = signals[0][3]
    ret = ""

    id = helper(iq, signals, bet_money)  # First bet
    wl = iq.check_win_v3(id)  # Check First bet win

    if wl > 0:
        ret = "Win "
        return ret, signals
    elif wl == 0:
        ret, signals = helper3(wl, ret, bet_money, num_times)
    elif wl < 0:
        ret, signals = helper3(wl, ret, bet_money, num_times)

    return ret, signals


iq, sigs, file, file_real_acc, d1str = init()
sigs = removePastTime(sigs)
num_tries = 4
real_acc = False

print("Signal IQOPTION")
bet_money = int(input("Enter amount of money per trade: "))

while len(sigs) != 1:
    checkTime(sigs)
    current_time = datetime.now().strftime("%H:%M")

    if sigs[0][2] == current_time and checkGreater():
        # if sigs[0][2] == sigs[0][2]:
        print("===============================")
        print("Same Time")
        ret, sigs = call_put(iq, sigs, bet_money, num_tries)
        ret = ret[:-1]
        sigsstr = ' '.join([x for x in sigs[0]])
        n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " " + str(ret) + "\n"
        print(n_str)

        if real_acc == True:
            file_real_acc.write(n_str)
            real_acc = False
        else:
            file.write(n_str)

        if ret.split(" ").count('Lose') == 4:
            real_acc = True
            print("Real account!")
            # iq.change_balance("REAL")

    sigs = removePastTime(sigs)
    file.close()
    file_real_acc.close()
    file = open("D:/School Files/Program/Logs/" + d1str, "a+")
    file_real_acc = open("D:/School Files/Program/Logs/Real/" + d1str, "a+")

    sigs.pop(0)
    trade = False
