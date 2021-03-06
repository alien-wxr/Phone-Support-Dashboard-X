##############################################
#   getCurrentState.py
#   Phone-Support-Dashboard-X/Data
#
#   Function:
#       get the currentState data from the 
#       xmltype permalink
#
#   Created by Xiaorong Wang on 2019/10/11.
###############################################




from Data import spider
from bs4 import BeautifulSoup
import operator

def get():

    soup = spider.spider('./Data/url.txt')

    xml = []

    for row_tag in soup.report.children:
        l = []
        for col_tag in row_tag.children:
            if (col_tag['name']=='PQName'):
                l.append('0')
            elif (col_tag['name']=='PQStep'):
                l.append('0')
            elif (len(col_tag.contents) != 0):
                l.append(col_tag.contents[0])
            else:
                l.append('NULL')
        xml.append(l)

    xml = [list(t) for t in set(tuple(_) for _ in xml)]
    xml.sort(key=operator.itemgetter(3))

    return xml