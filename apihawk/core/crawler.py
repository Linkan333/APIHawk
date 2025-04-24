import requests
import logging
import time
from bs4 import BeautifulSoup

def crawl_api(url, method, params=None, headers=None, timeout=5, proxies=None, verbose=False):
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f"Reached the URL: {url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        link = []
        for link in soup.find_all('<a>'):
            href = link.get('href="')
            if href:
                url.append(href)
            
            for link in url:
                if link.startswith('api'):
                    logging.info(f"Found API endpoint: {link}")
                    url.append(link)
                elif '{' in link:
                    logging.info(f"Found possible API endpoint: {link}")
                    url.append(link)
                if 'api' in response.content:
                    logging.info(f"Found possible API endpoint: {link}")
                    url.append(link)
                if link.endswith('.json'):
                    logging.info(f"Found possible API endpoint: {link}")
                    url.append(link)
                if link.endswith('.xml'):
                    logging.info(f"Found possible API endpoint: {link}")
                    url.append(link)
                if link.endswith('.txt'):
                    logging.info(f"Found possible sensitive file: {link}")
                    url.append(link)
                if link.endswith('.log'):
                    logging.info(f"Found possible log file: {link}")
                    url.append(link)
                if link.endswith('.bak'):
                    logging.info(f"Found possible backup file: {link}")
                    url.append(link)
                if link.endswith('.zip'):
                    logging.info(f"Found possible zip file: {link}")
                    url.append(link)
        return url
    