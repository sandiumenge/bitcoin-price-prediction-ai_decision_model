import requests
import re
import json

def get_tweet_json(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}

    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the page")
        return None
    
    html = response.text
    
    # Look for embedded JSON data (this may change if Twitter updates its structure)
    match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', html, re.DOTALL)
    if match:
        raw_json = match.group(1)
        try:
            parsed_json = json.loads(raw_json)
            return parsed_json
        except json.JSONDecodeError:
            print("Error decoding JSON")
    
    return None

# Example usage
url = "https://x.com/manusporny/status/19107730769"
tweet_data = get_tweet_json(url)

if tweet_data:
    print(json.dumps(tweet_data, indent=2))
else:
    print("Tweet JSON not found.")
