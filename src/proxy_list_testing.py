import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures

def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text == 'elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

def retry(func, retries=50):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(2)
                attempts += 1

    return retry_wrapper

def proxy_from_txt(filename):
    with open(filename, 'r') as f:
        txt_proxies = [line.strip() for line in f]
    return txt_proxies

@retry
def url_get(proxy_choice):
    url = 'https://allbirds.com/products.json'
    p = random.choice(range(len(proxy_choice)))
    prox = proxy_choice[p]
    proxies = {
        'https': prox,
        'http': prox,
    }
    print(proxies)
    proxy_choice.pop(p)
    r = requests.get(url, proxies=proxies, timeout=15)
    data = {
        'data': [
            r.json()['products'][6]['id'],
            r.json()['products'][0]['title'],
        ],
        'proxy': proxies
    }
    print(data)


def extract(proxy):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        r = requests.get('https://x.com/manusporny/status/19107730769/', headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=2)
        if r.status_code == 200:
            print(proxy)
            # soup = BeautifulSoup(r.text, 'html.parser')
            # with open("file.txt", "a") as file:
            #     file.write(soup)
            # tweet_text = soup.find('div', {'class': 'tweet-text'}).get_text(strip=True)
            # print(tweet_text)
    except requests.ConnectionError:
        pass
        # print(proxy, "failed")

    return proxy


# URL to get proxies from ProxyScrape
PROXYSCRAPE_URL = ("https://api.proxyscrape.com/v4/free-proxy-list/get?"
                   "request=display_proxies&protocol=socks4,socks5&proxy_format=protocolipport"
                   "&format=text&timeout=20000")


def get_proxy_list():
    """
    Fetch proxy list from ProxyScrape API.
    Expected format per line: e.g. "socks5 1.2.3.4:1234"
    """
    try:
        response = requests.get(PROXYSCRAPE_URL, timeout=10)
        response.raise_for_status()
        # Each proxy is on a new line
        proxies = response.text.strip().splitlines()
        return [proxy.split("://")[1] for proxy in proxies]
    except Exception as e:
        print("Error fetching proxy list:", e)
        return []

def main():
    proxylist = getProxies()
    print(len(proxylist))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract, proxylist)

    return

if __name__ == '__main__':
    print(main())
