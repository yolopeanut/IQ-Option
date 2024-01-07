from datetime import datetime
from datetime import date
from iq import login, higher,lower
from generate import gene2
import time

print("Signal IQOPTION")
bet_money = int(input("Enter amount of money per trade: "))

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


#While sigs still exist
while(len(sigs) != 0):
    print("===============================")
    current_time = datetime.now().strftime("%H:%M")
    print(current_time)
    if trade == False:
        if sigs[0][2] == current_time: #Check if current time matches
        # if sigs[0][2] == sigs[0][2]:  # Check if current time matches
            print("Same Time")

            if sigs[0][3] == "CALL":
                print(sigs[0][1])
                id = higher(iq, bet_money, sigs[0][1])
                trade = True
            elif sigs[0][3] == "PUT":
                id = lower(iq, bet_money, sigs[0][1])
                trade = True

        else:
            print("Curr time: ", current_time)
            print("Next time: ", sigs[0][2] )

            time.sleep(10)
    else:
        sigsstr = ' '.join([x for x in sigs[0]])
        wl = iq.check_win_v3(id)

        #First wl = Win
        if wl>0:
            n_str = sigsstr + " " + str(bet_money)+ " " + str(iq.get_balance()) + " Win\n"
            print(n_str)
            file.write(n_str)
            trade = False

        #First wl = Draw
        elif wl == 0:
            if sigs[0][3] == "CALL":
                id = higher(iq, bet_money, sigs[0][1])
                wl2 = iq.check_win_v3(id)
                if wl2 > 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " DrawWin\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 == 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " DrawDraw\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 < 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " DrawLose\n"
                    print(n_str)
                    file.write(n_str)

            elif sigs[0][3] == "PUT":
                id = lower(iq, bet_money, sigs[0][1])
                wl2 = iq.check_win_v3(id)
                if wl2 > 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " DrawWin\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 == 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " DrawDraw\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 < 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " DrawLose\n"
                    print(n_str)
                    file.write(n_str)


        #First wl = Lose
        else:
            if sigs[0][3] == "CALL":
                id = higher(iq, bet_money*2, sigs[0][1])
                wl2 = iq.check_win_v3(id)
                if wl2 > 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " LoseWin\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 == 0 and wl <0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " LoseDraw\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 < 0 and wl <0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " LoseLose\n"
                    print(n_str)
                    file.write(n_str)

            elif sigs[0][3] == "PUT":
                id = lower(iq, bet_money*2, sigs[0][1])
                wl2 = iq.check_win_v3(id)
                if wl2 > 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " LoseWin\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 == 0 and wl < 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " LoseDraw\n"
                    print(n_str)
                    file.write(n_str)
                elif wl2 < 0 and wl < 0:
                    n_str = sigsstr + " " + str(bet_money) + " " + str(iq.get_balance()) + " LoseLose\n"
                    print(n_str)
                    file.write(n_str)



        file.close()
        file = open("D:/School Files/Program/Logs/" + d1str, "a+")
        sigsDone.append(sigs[0])
        sigs.pop(0)
        trade = False
