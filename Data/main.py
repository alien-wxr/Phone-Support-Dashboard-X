##############################################
#   main.py
#   Phone-Support-Dashboard-X/Data
#
#   Function:
#       the main.py for the data processing
#
#   Created by Xiaorong Wang on 2019/10/11.
###############################################





import time
import os
import getCurrentState

localtime = time.localtime(time.time())
itemLen = [16,2,8,18,9,11,8,8,21,6]

#   only run between 9 AM and 6 PM
if (localtime[3] >= 9 and localtime[3] <= 18):
    print('working time')

    #   Code has been run today
    if (os.path.exists("./Data/currentState.txt")):
        #   read data
        f = open("./Data/currentState.txt","r")
        oldtime =   f.readline()
        freeNum =   f.readline()
        busyNum =   f.readline()
        awayNum =   f.readline()
        allTalks=   f.readline()
        lines = f.readlines()
        i = 0
        state = []
        while (i!=len(lines)):
            j = 0
            item = []
            while (j < len(itemLen)):
                item.append(lines[i])
                i = i+1
                j = j+1
            state.append(item)
            
        print(oldtime)
        
        f.close()
        #   processing

        #   save data
        f = open("./Data/currentState.txt","w")
        
        f.write(str(int(time.time()))+'\n')
        xml = getCurrentState.get()
        for item in xml:
            i = 0
            while (i < 10):
                f.write(item[i].ljust(itemLen[i],' ')+'|')
                i = i+1
            f.write('\n')
        f.close()
    #   Code hasn't been run today
    else:
        f = open("./Data/currentState.txt","w")
        f.write(str(int(time.time()))+'\n')
        xml = getCurrentState.get()
        for item in xml:
            i = 0
            while (i < 10):
                f.write(item[i].ljust(itemLen[i],' ')+'|')
                i = i+1
            f.write('\n')
        f.close()
else:
    os.remove("./Data/currentState.txt")
    print('off work')