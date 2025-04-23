import requests



def fuzz_endpoint(url, wordlist, method, cookies=None, headers=None, timeout=5, proxies=None, verbose=False):
    url = f"{url}/{wordlist}"
    response = requests.get(url, timeout=timeout)
    #if url.endswith("FUZZ"):
        #url.replace("FUZZ", {wordlist})
    #lay in bed an thought about this problem but a better solution would be following:
    # this will tho copy the whole wordlist so i am going to make an for line in lines.. functiob
    url.replace("FUZZ", wordlist)
    if response != 404:
        print(f"Found {url}")