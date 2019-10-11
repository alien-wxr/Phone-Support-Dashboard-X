###############################################
#   getXML.py
#   Phone-Support-Dashboard-X/Data
#
#   Function:
#       get the data from the xmltype permalink
#
#   Created by Xiaorong Wang on 2019/10/11.
###############################################

import requests
import re
from bs4 import BeautifulSoup
import time
import operator

def getXML(file):
    with open(file,'r') as f:
        url = f.readline()
        f.close()
    
    #Web spider
    xml = requests.get(url, verify = False)

    soup = BeautifulSoup(xml.text, "xml")

    return soup