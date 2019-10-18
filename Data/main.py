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
itemLen = 6

#   only run between 9 AM and 6 PM
if (localtime[3] >= 9 and localtime[3] <= 18):
    print('working time')

    #   Code has been run today
    if (os.path.exists("./Data/currentState.txt")):

        #   read data
        f = open("./Data/currentState.txt","r")
        oldtime =   int(f.readline().replace('\r','').replace('\n',''))
        freeNum =   int(f.readline().replace('\r','').replace('\n',''))
        busyNum =   int(f.readline().replace('\r','').replace('\n',''))
        awayNum =   int(f.readline().replace('\r','').replace('\n',''))
        allTalks=   int(f.readline().replace('\r','').replace('\n',''))
        waitNum =   int(f.readline().replace('\r','').replace('\n',''))
        lines = f.readlines()
        i = 0
        oldStateList = []
        while (i!=len(lines)):
            j = 0
            oldStateDict = {}
            oldStateDict = {'FullName':lines[i].replace('\r','').replace('\n','')}
            i = i+1
            oldStateDict = {'AgentState':lines[i].replace('\r','').replace('\n','')}
            i = i+1
            oldStateDict = {'TimeInState':lines[i].replace('\r','').replace('\n','')}
            i = i+1
            oldStateDict = {'OnShift':lines[i].replace('\r','').replace('\n','')}
            i = i+1
            oldStateDict = {'CurrentStatePeriod':lines[i].replace('\r','').replace('\n','')}
            i = i+1
            oldStateDict = {'Talks':lines[i].replace('\r','').replace('\n','')}
            i = i+1
            oldStateList.append(oldStateDict)
        print(oldtime)
        f.close()

        #   processing
        xml =  getCurrentState.get()
        stateList = []
        for item in xml:
            stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9],'CurrentStatePeriod':'0','Talks':'0'}
            stateList.append(stateDict)
        
        for stateDict in stateList:
            if stateDict['OnShift']=='true':
                if stateDict['AgentState']=='Ready':
                    stateDict['AgentState']='Free'
                    freeNum = freeNum+1
                elif stateDict['AgentState']=='Talking' or stateDict['AgentState']=='Work Ready':
                    stateDict['AgentState']='Busy'
                    busyNum = busyNum+1
                    allTalks = allTalks+1
                elif stateDict['AgentState']=='Not Ready':
                    stateDict['AgentState']='Away'
                    awayNum = awayNum+1
                else:
                    stateDict['AgentState']='ErrState'
            else:
                stateDict['AgentState']='Offline'
        
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
        for stateDict in stateList:
            item = stateDict.values()
            for item2 in item:
                print(item2.ljust(20,' '), end='|')
            print()

    #   Code hasn't been run today
    else:
        #   initializing
        stateList = []
        freeNum   = 0
        busyNum   = 0
        awayNum   = 0
        allTalks  = 0
        waitNum   = 0

        #   processing
        xml =  getCurrentState.get()
        
        for item in xml:
            stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9],'CurrentStatePeriod':'0','Talks':'0'}
            stateList.append(stateDict)

        for stateDict in stateList:
            if stateDict['OnShift']=='true':
                if stateDict['AgentState']=='Ready':
                    stateDict['AgentState']='Free'
                    freeNum = freeNum+1
                elif stateDict['AgentState']=='Talking' or stateDict['AgentState']=='Work Ready':
                    stateDict['AgentState']='Busy'
                    busyNum = busyNum+1
                    allTalks = allTalks+1
                elif stateDict['AgentState']=='Not Ready':
                    stateDict['AgentState']='Away'
                    awayNum = awayNum+1
                else:
                    stateDict['AgentState']='ErrState'
            else:
                stateDict['AgentState']='Offline'

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
        #   for debug
        for stateDict in stateList:
            item = stateDict.values()
            for item2 in item:
                print(item2.ljust(20,' '), end='|')
            print()
else:
    os.remove("./Data/currentState.txt")
    print('off work')