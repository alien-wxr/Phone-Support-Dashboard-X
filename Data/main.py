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

localtime = time.localtime(time.time())

#   only run between 9 AM and 6 PM
if (localtime[3] >= 9 and localtime[3] <= 18):
    print('working time')

    #   Code has been run today
    if (os.path.exists("./Data/currentState.txt")):
        f = open("./Data/currentState.txt","w")
        f.write("test1")
        f.close()
    #   Code hasn't been run today
    else:
        f = open("./Data/currentState.txt","w")
        f.write("test2")
        f.close()
else:
    os.remove("./Data/currentState.txt")
    print('off work')