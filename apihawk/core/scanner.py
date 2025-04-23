import requests
import logging
import time

def scanner(url, wordlist, method, cookie=None, header=None, timeout=5, proxies=None, verbose=False):
    """
    Scanner function to perform API reconassiance
    """
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f"Reached the URL: {url}")
        logging.info(f"Starting scanner with wordlist: {wordlist}")
        try:
            with open(wordlist, 'r') as f:
                api_urls = [line.strip() for line in f]
        except FileNotFoundError:
            logging.error(f"Could not find wordlist file: {wordlist}")
            return
        for endpoint in api_urls:
            target_url = url
            
    pass