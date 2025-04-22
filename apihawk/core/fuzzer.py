import requests



def fuzz_endpoint(url, wordlist, method, cookies=None, headers=None, timeout=5, proxies=None, verbose=False):
    url = f"{url}/{wordlist}"
    response = requests.get(url, timeout=timeout)
    if url.endswith("FUZZ"):
        url.replace("FUZZ", {wordlist})
    if response != 404:
        print(f"Found {url}")