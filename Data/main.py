##################################################
#   main.py
#   Phone-Support-Dashboard-X/Data
#
#   Function:
#       the main.py for the data processing
#
#   Created by Xiaorong Wang on 2019/10/11.
##################################################

##################################################
#   Variable Illustration
#   
#   oldStateDict and stateDict are all Dictionary
#   including following keys:
#       'FullName'              :   TSE's FullName, data directly from the PermaLink.
#       'AgentState'            :   TSE's AgentState, data directly from the PermaLink. 
#                                   Value includes Ready, Not Ready, Talking, Work Ready, Logged Off.
#       'TimeInState'           :   TSE's TimeInState, data directly from the PeramLink.
#                                   Time in the current AgentState showed in seconds.
#       'OnShift'               :   If TSE is OnShift, data directly from the PermaLink.
#       'CurrentState'          :   TSE's CurrentState, data have been processed.
#                                   Processing method is illustrated from line 92 and 195.
#       'CurrentStatePeriod'    :   TSE's CurrentStatePeriod, data have been processed.
#                                   Time in CurrentState showed in seconds.
#       'Talks'                 :   TSE's talks counter. Times in Talking state.
#
##################################################


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
            lines = f.readlines()       #   read the left 7*N lines
            i = 0
            oldStateList = []           #   a List of Dictionary
            while (i!=len(lines)):
                j = 0
                oldStateDict = {}
                oldStateDict['FullName'] = lines[i].replace('\r','').replace('\n','')
                i += 1
                oldStateDict['AgentState'] = lines[i].replace('\r','').replace('\n','')
                i += 1
                oldStateDict['TimeInState'] = lines[i].replace('\r','').replace('\n','')
                i += 1
                oldStateDict['OnShift'] = lines[i].replace('\r','').replace('\n','')
                i += 1
                oldStateDict['CurrentState'] = lines[i].replace('\r','').replace('\n','')
                i += 1
                oldStateDict['CurrentStatePeriod'] = lines[i].replace('\r','').replace('\n','')
                i += 1
                oldStateDict['Talks'] = lines[i].replace('\r','').replace('\n','')
                i += 1
                oldStateList.append(oldStateDict)
            print(oldTime)
            f.close()

            #   initializing
            stateList = []                      #   new state list
            freeNum   = 0
            busyNum   = 0
            awayNum   = 0

            #   pre-processing
            currentTime = int(time.time())      #   get current time
            xml =  getCurrentState.get()        #   get current state xml
            waitNum = getCallinQueue.get()      #   get current call in queue

            for item in xml:
                stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9],'CurrentState':'','CurrentStatePeriod':'0','Talks':'0'}
                stateList.append(stateDict)

            ###########################################
            #   state convert
            #       OnShift + Ready         --> Free
            #       OnShift + Talking       --> Busy
            #       OnShift + Work Ready    --> Busy
            #       OnShift + Not Ready     --> Away
            #       OnShift + Else          --> ErrState
            #       ---
            #       OffShift                --> Offline
            ############################################
            for stateDict in stateList:
                if stateDict['OnShift']=='true':
                    if stateDict['AgentState']=='Ready':
                        stateDict['CurrentState']='Free'
                        freeNum += 1
                    elif stateDict['AgentState']=='Talking' or stateDict['AgentState']=='Work Ready':
                        stateDict['CurrentState']='Busy'
                        busyNum += 1
                    elif stateDict['AgentState']=='Not Ready':
                        stateDict['CurrentState']='Away'
                        awayNum += 1
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
                        if oldStateDict['CurrentState']!='Busy' and stateDict['CurrentState']=='Busy':
                            allTalks = allTalks+1
                            stateDict['Talks'] = str(int(oldStateDict['Talks'])+1)
                        else:
                            stateDict['Talks'] = oldStateDict['Talks']
                        #   Current State Period Calculating
                        if stateDict['AgentState']=='Work Ready' and oldStateDict['AgentState']=='Talking':
                            #   change from talking to work ready
                            stateDict['CurrentStatePeriod'] = str(int(oldStateDict['CurrentStatePeriod'])+currentTime-oldTime)
                        else:
                            #   the other conditions
                            stateDict['CurrentStatePeriod'] = stateDict['TimeInState']
                #   cannot find the same AE data from oldStateList
                if flag:
                    #   Talks Recording
                    if stateDict['AgentState']=='Busy':
                        allTalks += 1
                        stateDict['Talks'] = str(int(stateDict['Talks'])+1)
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

            #   save dataLog
            path = "./Data/Log/"+str(currentTime)+".txt"
            f = open(path,"w")
            f.write(str(currentTime)+'\n')
            f.write(str(freeNum)+'\n')
            f.write(str(busyNum)+'\n')
            f.write(str(awayNum)+'\n')
            f.write(str(allTalks)+'\n')
            f.write(str(waitNum)+'\n')
            for stateDict in stateList:
                item = stateDict.values()
                for item2 in item:
                    f.write(item2.ljust(17,' ') +'|')
                f.write("\n")
            f.close()

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
            currentTime = int(time.time())      #   get current time
            xml =  getCurrentState.get()        #   get current state xml
            waitNum = getCallinQueue.get()      #   get current call in queue         
            
            for item in xml:
                stateDict = {'FullName':item[3],'AgentState':item[5],'TimeInState':item[6],'OnShift':item[9],'CurrentState':'','CurrentStatePeriod':'0','Talks':'0'}
                stateList.append(stateDict)

            ###########################################
            #   state convert
            #       OnShift + Ready         --> Free
            #       OnShift + Talking       --> Busy
            #       OnShift + Work Ready    --> Busy
            #       OnShift + Not Ready     --> Away
            #       OnShift + Else          --> ErrState
            #       ---
            #       OffShift                --> Offline
            ############################################
            for stateDict in stateList:
                stateDict['CurrentStatePeriod']=stateDict['TimeInState']
                if stateDict['OnShift']=='true':
                    if stateDict['AgentState']=='Ready':
                        stateDict['CurrentState']='Free'
                        freeNum += 1
                    elif stateDict['AgentState']=='Talking' or stateDict['AgentState']=='Work Ready':
                        stateDict['CurrentState']='Busy'
                        busyNum += 1
                        allTalks += 1
                        stateDict['Talks']=str(int(stateDict['Talks'])+1)
                    elif stateDict['AgentState']=='Not Ready':
                        stateDict['CurrentState']='Away'
                        awayNum += 1
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
    else:
        os.remove("./Data/currentState.txt")
        print('off work')
except:
    f = open("./Data/errorLog.txt","w")
    f.write(str(currentTime)+": error\n")
    f.close()
    print('error')