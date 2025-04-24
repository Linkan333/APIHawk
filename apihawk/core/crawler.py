import requests
import logging
import time
from bs4 import BeautifulSoup

def crawl_api(url, method, params=None, headers=None, timeout=5, proxies=None, verbose=False):
    response = requests.get(url)
    if response.status_code == 200:
        loggin.info(f"Reached the URL: {url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        link = []
        for link in soup.find_all('<a>'):
            href = link.get('href="')
            if href:
                urls.append(href)
            
            for link in urls:
                if link.startswith('api'):
                    loggin.info(f"Found API endpoint: {link}")
                    urls.append(link)
                elif '{' in link:
                    loggin.info(f"Found possible API endpoint: {link}")
                    urls.append(link)
                if 'api' in response.content:
                    loggin.info(f"Found possible API endpoint: {link}")
                    urls.append(link)
                if link.endswith('.json'):
                    loggin.info(f"Found possible API endpoint: {link}")
                    urls.append(link)
                if link.endswith('.xml'):
                    loggin.info(f"Found possible API endpoint: {link}")
                    urls.append(link)
                if link.endswith('.txt'):
                    loggin.info(f"Found possible sensitive file: {link}")
                    urls.append(link)
                if link.endswith('.log'):
                    loggin.info(f"Found possible log file: {link}")
                    urls.append(link)
                if link.endswith('.bak'):
                    loggin.info(f"Found possible backup file: {link}")
                    urls.append(link)
                if link.endswith('.zip'):
                    loggin.info(f"Found possible zip file: {link}")
                    urls.append(link)
        return urls
    