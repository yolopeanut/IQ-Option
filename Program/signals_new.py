from datetime import datetime
from datetime import date
from iq import login, higher,lower
from generate import gene2
import time


print("Signal IQOPTION")
bet_money = int(input("Enter amount of money per trade: "))

num_tries = 4
sigs = []       #List containing split signals
sigsDone = []   #List to contain the completed signals
iq = login()    #Login to iqoptions
bets =[]
trade = False


gene2() #Generate list
print("List generated!")


#Reading signal file
with open(r"D:\School Files\Program\sigs.txt", 'r') as fp:
    sigs = [line.rstrip('\n').split(" - ") for line in fp]

print("Done appending into sigs")

#Initialising file that will log history
#==========================================
today = date.today()
d1 = today.strftime("%d.%m")
d1str = d1 +".txt"
file = open("D:/School Files/Program/Logs/" + d1str, "a+")
print("Done adding log file")
#==========================================

def mtgale(num_tries, wl):
    tried = 0
    if wl <0:
        tried = 1
    elif wl == 0:
        tried = 0

    while tried != num_tries:
        id = higher(iq, bet_money, sigs[0][1])
        tried += 1
        wl = iq.check_win_v3(id)

        if wl > 0:
            return 0
        elif wl == 0:
            tried -=1
        elif wl < 0:
            pass

    if tried == num_tries:
        return 1


def func_trade(sigs, current_time):
    trading = False
    id = None
    if sigs[0][2] == current_time:  # Check if current time matches
        print("Same Time")
        if sigs[0][3] == "CALL":
            print(sigs[0][1])
            id = higher(iq, bet_money, sigs[0][1])
            trading = True
        elif sigs[0][3] == "PUT":
            id = lower(iq, bet_money, sigs[0][1])
            trading = True
    else:
        print("Curr time: ", current_time)
        print("Next time: ", sigs[0][2])

        time.sleep(10)

    return trading,id

def join_str(sigs):
    sigsstr = ' '.join([x for x in sigs[0]])
    wl = iq.check_win_v3(id)
    if wl > 0:
        pass
    elif wl == 0 or wl < 0:
        value = mtgale(num_tries, wl)

value = None
#While sigs still exist
while(len(sigs) != 0):
    current_time = datetime.now().strftime("%H:%M")
    print(current_time)

    if trade == False and value != 1:
        print("Making call on practice account")
        iq.change_balance("PRACTICE")
        trade,id = func_trade(sigs,current_time)

    else:
        sigsstr = ' '.join([x for x in sigs[0]])
        wl = iq.check_win_v3(id)
        if wl > 0:
            pass
        elif wl == 0 or wl <0:
            value = mtgale(num_tries,wl)



    if trade == False and value == 1:
        print("Making call on real account")
        iq.change_balance("REAL")
        # iq.change_balance("TOURNAMENT")
        trade, id = func_trade(sigs, current_time)
    else:
        sigsstr = ' '.join([x for x in sigs[0]])
        wl = iq.check_win_v3(id)
        if wl > 0:
            pass
        elif wl == 0 or wl <0:
            value = mtgale(num_tries,wl)




