import os
import pandas as pd

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

df = pd.DataFrame()
for stateDict in oldStateList:
    new = pd.DataFrame([stateDict])
    df = df.append(new)

print(df)
df.to_csv("stateList.csv", index=None)