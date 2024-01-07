from datetime import datetime, date
from iq import login, higher, lower, get_candles


def init():
    # iq = login()  # Login to iqoptions
    # gene2()  # Generate list
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

    # iq.start_candles_stream("EURUSD", 60, 280)


    return sigs, file,file_real_acc, d1str

sigs, file, file_real_acc, d1str = init()
# print(sigs)
while(True):
    current_time_tmp = datetime.strptime(datetime.now().strftime("%H:%M"),"%H:%M")
    time = datetime.strptime(sigs[0][2], "%H:%M")
    print(current_time_tmp,time)
    if time < current_time_tmp:
        sigs.pop(0)
    else:
        print(sigs)
        break