import random
from fake_useragent import UserAgent
import requests

# Initialize UserAgent for rotating user agents
ua = UserAgent()

# Example proxy pool (replace these with actual working proxies)
proxies = [
    'http://88.99.171.90:7003',
    'http://44.215.100.135:8118',
    'http://8.209.200.126:3389',
    'http://45.140.143.77:18080',
    'http://27.79.236.245:16000',
    'http://184.168.124.233:5402',
    'http://172.233.78.254:7890',
    'http://18.135.133.116:80',
    'http://27.79.237.17:16000',
    'http://113.160.132.195:8080'
]


# Function to get a random proxy from the pool
def get_random_proxy():
    return random.choice(proxies)

# Function to get a random user-agent
def get_random_user_agent():
    return ua.random

# Make a request with rotating proxies and user agents
def make_request(url):
    # Get random user agent and proxy
    headers = {
        "User-Agent": get_random_user_agent()
    }
    proxy = get_random_proxy()

    # Set up the proxy for the request
    proxy_dict = {
        "http": proxy,
        "https": proxy
    }

    # Make the request
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"Request Status Code: {r.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

# Example URL
id = "1176843235135774720"
url = f"https://cdn.syndication.twimg.com/tweet-result?id={id}&token=a"

# Send the request with rotating user agent and proxy
make_request(url)
