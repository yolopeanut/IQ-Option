from datetime import datetime,timedelta
import random

def randoms(lst, n):
    # print(lst)
    for i in range(n):
        lst.pop(random.randint(0,len(lst)-1))
    return lst


def gene2():
    arr = []

    # min_round = round(datetime.now().minute,-1)+10
    min_round = datetime.now().minute+1
    if min_round>=60:
        start = str(datetime.now().replace(hour=datetime.now().hour+1, minute=00).strftime("%H:%M"))
    else:
        start = str(datetime.now().strftime("%H:") + str(min_round))
    end = "23:00:00"
    delta = timedelta(minutes=7)
    start = datetime.strptime(start, '%H:%M')
    end = datetime.strptime(end, '%H:%M:%S')
    t = start
    while t <= end:
        arr.append("M5 - EURUSD - " + datetime.strftime(t, '%H:%M') + " - " + random.choice(["CALL", "PUT"]))
        t += delta

    lst = randoms(arr, random.randint(0,int(len(arr)/100)))
    print(lst)
    textfile = open("sigs.txt", "w")
    for element in lst:
        textfile.write(element + "\n")
    textfile.close()