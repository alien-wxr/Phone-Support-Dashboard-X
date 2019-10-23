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
import getCallinQueue

localtime = time.localtime(time.time())

try:
    #   only run between 9 AM and 6 PM
    if (localtime[3] >= 9 and localtime[3] <= 18):

        #   Code has been run today
        if (os.path.exists("./Data/currentState.txt")):

            #   read data
            f = open("./Data/currentState.txt","r")
            oldTime =   int(f.readline().replace('\r','').replace('\n',''))
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
                oldStateDict['FullName'] = lines[i].replace('\r','').replace('\n','')
                i = i+1
                oldStateDict['AgentState'] = lines[i].replace('\r','').replace('\n','')
                i = i+1
                oldStateDict['TimeInState'] = lines[i].replace('\r','').replace('\n','')
                i = i+1
                oldStateDict['OnShift'] = lines[i].replace('\r','').replace('\n','')
                i = i+1
                oldStateDict['CurrentState'] = lines[i].replace('\r','').replace('\n','')
                i = i+1
                oldStateDict['CurrentStatePeriod'] = lines[i].replace('\r','').replace('\n','')
                i = i+1
                oldStateDict['Talks'] = lines[i].replace('\r','').replace('\n','')
                i = i+1
                oldStateList.append(oldStateDict)
            print(oldTime)
            f.close()

            #   pre-processing
            currentTime = int(time.time())
            xml =  getCurrentState.get()
            waitNum = getCallinQueue.get()
            stateList = []
            for item in xml:
                stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9],'CurrentState':'','CurrentStatePeriod':'0','Talks':'0'}
                stateList.append(stateDict)
            freeNum = 0
            busyNum = 0
            awayNum = 0
            for stateDict in stateList:
                if stateDict['OnShift']=='true':
                    if stateDict['AgentState']=='Ready':
                        stateDict['CurrentState']='Free'
                        freeNum = freeNum+1
                    elif stateDict['AgentState']=='Talking' or stateDict['AgentState']=='Work Ready':
                        stateDict['CurrentState']='Busy'
                        busyNum = busyNum+1
                    elif stateDict['AgentState']=='Not Ready':
                        stateDict['CurrentState']='Away'
                        awayNum = awayNum+1
                    else:
                        stateDict['CurrentState']='ErrState'
                else:
                    stateDict['CurrentState']='Offline'
            
            #   processing
            for stateDict in stateList:
                flag = True
                for oldStateDict in oldStateList:
                    if stateDict['FullName']==oldStateDict['FullName']:
                        flag = False
                        #   Talks Recording
                        if oldStateDict['CurrentState']=='Free' and stateDict['CurrentState']=='Busy':
                            allTalks = allTalks+1
                            stateDict['Talks'] = str(int(oldStateDict['Talks'])+1)
                        else:
                            stateDict['Talks'] = oldStateDict['Talks']
                        #   Current State Period Calculating
                        if stateDict['AgentState']==oldStateDict['AgentState'] and stateDict['OnShift']==oldStateDict['OnShift']:
                            #   no state changing
                            if oldStateDict['CurrentStatePeriod']=='NULL':
                                stateDict['CurrentStatePeriod'] = 'NULL'
                            else:
                                stateDict['CurrentStatePeriod'] = str(int(oldStateDict['CurrentStatePeriod'])+currentTime-oldTime)
                        elif stateDict['AgentState']=='Work Ready' and oldStateDict['AgentState']=='Talking':
                            #   change from talking to work ready
                            stateDict['CurrentStatePeriod'] = str(int(oldStateDict['CurrentStatePeriod'])+currentTime-oldTime)
                        else:
                            stateDict['CurrentStatePeriod'] = stateDict['TimeInState']
                #   cannot find the same AE data from oldStateList
                if flag:
                    #   Talks Recording
                    if stateDict['AgentState']=='Busy':
                        allTalks = allTalks+1
                        stateDict['Talks'] = stateDict['Talks']+1
                    #   Current State Period Calculating
                    stateDict['CurrentStatePeriod'] = stateDict['TimeInState']
            
            #   save data
            f = open("./Data/currentState.txt","w")
            f.write(str(currentTime)+'\n')
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
            currentTime = int(time.time())
            xml =  getCurrentState.get()
            waitNum = getCallinQueue.get()
            
            for item in xml:
                stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9],'CurrentState':'','CurrentStatePeriod':'0','Talks':'0'}
                stateList.append(stateDict)

            for stateDict in stateList:
                if stateDict['TimeInState']=='NULL':
                    stateDict['CurrentStatePeriod']='NULL'
                else:
                    stateDict['CurrentStatePeriod']=stateDict['TimeInState']
                if stateDict['OnShift']=='true':
                    if stateDict['AgentState']=='Ready':
                        stateDict['CurrentState']='Free'
                        freeNum = freeNum+1
                    elif stateDict['AgentState']=='Talking' or stateDict['AgentState']=='Work Ready':
                        stateDict['CurrentState']='Busy'
                        busyNum = busyNum+1
                        allTalks = allTalks+1
                        stateDict['Talks']=str(int(stateDict['Talks'])+1)
                    elif stateDict['AgentState']=='Not Ready':
                        stateDict['CurrentState']='Away'
                        awayNum = awayNum+1
                    else:
                        stateDict['CurrentState']='ErrState'
                else:
                    stateDict['CurrentState']='Offline'

            #   save data
            f = open("./Data/currentState.txt","w")
            f.write(str(currentTime)+'\n')
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
except:
    f = open("./Data/errorLog.txt","w")
    f.write("error")
    f.close()
    print('error')