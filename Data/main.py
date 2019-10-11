import getXML
from bs4 import BeautifulSoup

soup = getXML.getXML('./Data/url.txt')

print(soup)