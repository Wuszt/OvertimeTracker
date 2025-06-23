from os import write
import os
import subprocess
import time
import datetime
from plyer import notification

def IsLocked():
    process_name='LogonUI.exe'
    callall='TASKLIST'
    outputall=subprocess.check_output(callall, creationflags=subprocess.CREATE_NO_WINDOW)
    outputstringall=str(outputall)
    return process_name in outputstringall

fileName = os.environ["LOCALAPPDATA"] + "\\" + "OvertimeTracker.txt"
currTime = 0

try:
    readFile = open(fileName, "r")
    date = readFile.readline().strip()
    if date == datetime.datetime.utcnow().strftime('%d-%m-%Y'):
        currTxt = readFile.readline()
        if len(currTxt) > 0:
            currTime = int(currTxt)
    readFile.close()
except:
    pass

printedWarning = False
printedAlert = False
overTimeStart = 8 * 60 * 60
while(True):
    lastTime = datetime.datetime.utcnow().timestamp()
    time.sleep(5 * 60)
    if not IsLocked():
        today = datetime.datetime.utcnow().strftime('%d-%m-%Y')
        newTime = datetime.datetime.utcnow().timestamp()
        currTime += int(newTime - lastTime)
        writeFile = open(fileName, "w")
        writeFile.write(today)
        writeFile.write('\n')
        writeFile.write(str(currTime))
        writeFile.close()
        if currTime > overTimeStart:
            if printedAlert:
                notification.notify(title = "OVERTIME ALERT",message="YOU'RE DOING OVERTIME FOR " + str(int((currTime - overTimeStart) / 60)) + " MINUTES" , timeout=5)
            else:
                notification.notify(title = "OVERTIME ALERT",message="YOU STARTED OVERTIME!", timeout=5)
                printedAlert = True
        elif overTimeStart - currTime < 30 * 60 and not printedWarning:
            printedWarning = True
            notification.notify(title = "OVERTIME WARNING",message="30 minutes left" , timeout=5)