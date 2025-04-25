import requests
import logging
import time
from urllib.parse import urljoin, urlparse

async def scanner(url, wordlist, method, cookie=None, header=None, timeout=5, proxies=None, verbose=False, delay=0.1):
    """
    Scanner function to perform API reconassiance

    args:
        url (str): The target URL to scan.
        wordlist (str): path to the wordlist file.
        method (str): HTTP method to use (GET, POST, PUT, DELETE).
        cookie (str): Cookie to use for requests.
        header (str): Header to use for requests.
    """

    common_wordlist = "wordlists/common.txt"

    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            logging.error("Invalid URL format")
            return
    except Exception as e:
        logging.error(f"Error parsing URL: {e}")
        return
    
    try:
        response = requests.get(url, timeout=timeout, proxies=proxies)
        logging.info(f"Base URL {url} - Status: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Could not reach base URL: {e}")
        return
    
    try:
        with open(wordlist, 'r') as f:
            api_endpoints = [line.strip() for line in f]
        with open(common_wordlist, 'r') as f:
            common_paths = [line.strip() for line in f]
    except FileNotFoundError as e:
        logging.error(f"Wordlist file not found: {e}")
        return
    
    method = method.upper()
    for endpoint in api_endpoints:
        for common_path in common_paths:
            target_url = urljoin(url, f"{endpoint}/{common_path}")
            logging.info(f"Testing {target_url}")

            try:
                response = requests.request(
                    method,
                    target_url,
                    headers=header,
                    cookies=cookie,
                    timeout=timeout,
                    proxies=proxies
                )

                if response.status_code in (200, 201, 400, 403):
                    logging.info(f"Potential endpoint found: {target_url} - Status: {response.status_code} - Length: {len(response.content)}")
                    if verbose:
                        logging.info(f"Response: {response.text}")
                time.sleep(delay)


            except requests.RequestException as e:
                if verbose:
                    logging.error(f"Error @ {target_url}: {e}")
                continue
            
