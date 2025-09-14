import asyncio
import aiohttp
import aiofiles
import os
import json
import random
from fake_useragent import UserAgent
from pyspark.sql import SparkSession

CONCURRENCY = 10  # Maximum concurrent requests
RATE_LIMIT_SLEEP = 60  # Seconds to sleep on rate limit
BASE_URL = "https://cdn.syndication.twimg.com/tweet-result?id={id}&token=a"
USER_AGENT = UserAgent()  # Initialize user agent rotation
PROXIES = [
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
semaphore = asyncio.Semaphore(CONCURRENCY)

# Function to get random user agent
def get_random_user_agent():
    return USER_AGENT.random

# Function to get random proxy
def get_random_proxy():
    return random.choice(PROXIES)

async def fetch(session, id):
    url = BASE_URL.format(id=id)
    headers = {"User-Agent": get_random_user_agent()}
    proxy = get_random_proxy()

    async with semaphore:
        try:
            # Setup proxy for request
            proxy_dict = {
                "http": proxy,
                "https": proxy
            }
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.text()
                    return id, data
                elif response.status == 429:
                    print(f"Rate limited on ID {id}. Sleeping for {RATE_LIMIT_SLEEP} seconds.")
                    await asyncio.sleep(RATE_LIMIT_SLEEP)
                    return await fetch(session, id)  # Retry after delay
                else:
                    print(f"Error {response.status} on ID {id}, retrying with another proxy.")
                    return await fetch(session, id)  # Retry with another proxy
        except Exception as e:
            print(f"Exception on ID {id}: {e}, retrying with another proxy.")
            return await fetch(session, id)  # Retry with another proxy

async def process_ids(id_list, checkpoint_file, output_file):
    # Load already processed IDs to resume progress if available
    processed_ids = set()
    if os.path.exists(checkpoint_file):
        async with aiofiles.open(checkpoint_file, mode='r') as chk_in:
            async for line in chk_in:
                processed_ids.add(line.strip())
    
    async with aiohttp.ClientSession() as session, \
               aiofiles.open(output_file, mode='a') as out_f, \
               aiofiles.open(checkpoint_file, mode='a') as chk_out:
        
        tasks = []
        for id in id_list:
            id_str = str(id)
            if id_str in processed_ids:
                continue
            tasks.append(fetch(session, id))
            # Process in batches according to the concurrency limit
            if len(tasks) >= CONCURRENCY:
                results = await asyncio.gather(*tasks)
                for id_val, data in results:
                    if data is not None:
                        await out_f.write(json.dumps({id_val: data}) + "\n")
                    await chk_out.write(str(id_val) + "\n")
                tasks = []
        # Process any remaining tasks
        if tasks:
            results = await asyncio.gather(*tasks)
            for id_val, data in results:
                if data is not None:
                    await out_f.write(json.dumps({id_val: data}) + "\n")
                await chk_out.write(str(id_val) + "\n")

def main(id_list):
    checkpoint_file = "checkpoint.txt"
    output_file = "results.txt"
    asyncio.run(process_ids(id_list, checkpoint_file, output_file))

if __name__ == "__main__":
    # Assume you've already collected your id_list from PySpark as shown above
    spark = SparkSession.builder \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "2g") \
        .appName("CSV Date Occurrence Analysis") \
        .getOrCreate()

    initialDF = spark.read.option("recursiveFileLookup", "true").csv(
        "10_000_tweet_subset.csv", 
        header=True,  # Use the first row as column names
        inferSchema=True,  # Infer data types
        multiLine=True,  # Handle newlines within fields
        escape='\\',  # Escape character for double quotes
        quote='"',  # Define the quote character
        sep=",",  # Specify the correct delimiter
        mode="PERMISSIVE"  # Handle malformed rows gracefully
    )
    print("read!")
    id_list = [row["id"] for row in initialDF.select("id").collect()]
    main(id_list)
