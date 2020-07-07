##############################################
#   getCallinQueue.py
#   Phone-Support-Dashboard-X/Data
#
#   Function:
#       get the Call in Queue data from the 
#       xmltype permalink
#
#   Created by Xiaorong Wang on 2019/10/11.
###############################################




from Data import spider
from bs4 import BeautifulSoup
import operator

def get():

    soup = spider.spider('./Data/url2.txt')

    waitNum = 0
    for row_tag in soup.report.children:
        for col_tag in row_tag.children:
            if col_tag['name']=='Call in Queue':
                waitNum = waitNum+int(col_tag.contents[0])
    
    return waitNum
