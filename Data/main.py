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

#   only run between 9 AM and 6 PM
if (localtime[3] >= 9 and localtime[3] <= 18):
    print('working time')

    #   Code has been run today
    if (os.path.exists("./Data/currentState.txt")):
        #   read data
        f = open("./Data/currentState.txt","r")
        oldtime = f.readline()
        print(oldtime)
        
        f.close()
        #   processing

        #   save data
        f = open("./Data/currentState.txt","w")
        
        f.write(str(int(time.time()))+'\n')
        xml = getCurrentState.get()
        len = [16,2,8,18,9,11,8,8,21,6]
        for item in xml:
            i = 0
            while (i < 10):
                f.write(item[i].ljust(len[i],' ')+'|')
                i = i+1
            f.write('\n')
        f.close()
    #   Code hasn't been run today
    else:
        f = open("./Data/currentState.txt","w")
        f.write(str(int(time.time()))+'\n')
        xml = getCurrentState.get()
        len = [16,2,8,18,9,11,8,8,21,6]
        for item in xml:
            i = 0
            while (i < 10):
                f.write(item[i].ljust(len[i],' ')+'|')
                i = i+1
            f.write('\n')
        f.close()
else:
    os.remove("./Data/currentState.txt")
    print('off work')