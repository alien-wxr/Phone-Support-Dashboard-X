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




import spider
from bs4 import BeautifulSoup
import operator

soup = spider.spider('./Data/url2.txt')

xml = []

for row_tag in soup.report.children:
    l = []
    for col_tag in row_tag.children:
        if (len(col_tag.contents) != 0):
            l.append(col_tag.contents[0])
        else:
            l.append('NULL')
    xml.append(l)

#xml = [list(t) for t in set(tuple(_) for _ in xml)]
#xml.sort(key=operator.itemgetter(3))

for item in xml:
    for item2 in item:
        print(item2.ljust(20,' '), end='|')
    print()
