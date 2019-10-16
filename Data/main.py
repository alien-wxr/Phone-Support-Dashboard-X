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
itemLen = [16,2,8,18]

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
        waitNum =   f.readline()
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

        #processing
        xml =  getCurrentState.get()
        stateList = []
        freeNum   = 0
        busyNum   = 0
        awayNum   = 0
        allTalks  = 0
        waitNum   = 0
        for item in xml:
            stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9]}
            stateList.append(stateDict)
        #   save data
        f = open("./Data/currentState.txt","w")
        f.write(str(int(time.time()))+'\n')
        f.write(str(freeNum)+'\n')
        f.write(str(busyNum)+'\n')
        f.write(str(awayNum)+'\n')
        f.write(str(allTalks)+'\n')
        f.write(str(waitNum)+'\n')
        for stateDict in stateList:
            item = stateDict.values()
            for item2 in item:
                f.write(item2+'\n')
        f.close()
    #   Code hasn't been run today
    else:
        #processing
        xml =  getCurrentState.get()
        stateList = []
        freeNum   = 0
        busyNum   = 0
        awayNum   = 0
        allTalks  = 0
        waitNum   = 0
        for item in xml:
            stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9]}
            stateList.append(stateDict)
        #   save data
        f = open("./Data/currentState.txt","w")
        f.write(str(int(time.time()))+'\n')
        f.write(str(freeNum)+'\n')
        f.write(str(busyNum)+'\n')
        f.write(str(awayNum)+'\n')
        f.write(str(allTalks)+'\n')
        f.write(str(waitNum)+'\n')
        for stateDict in stateList:
            item = stateDict.values()
            for item2 in item:
                f.write(item2+'\n')
        f.close()
else:
    os.remove("./Data/currentState.txt")
    print('off work')