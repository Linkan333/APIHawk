import requests



def fuzz_endpoint(url, wordlist, method, cookie=None, header=None, timeout=5, proxies=None, verbose=False):
    results = []
    try:
        with open(wordlist, 'r') as f:
            fuzzer_urls = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Could not find wordlist file: {wordlist}")
        return
    
    for payload in fuzzer_urls:
        target_url = url.replace("FUZZ", payload) if "FUZZ" in url else f"{url}/{payload}"
        if verbose:
            print(f"Testing {target_url}")
        
        try:
            response = requests.request(
                method.upper(),
                target_url,
                cookies=cookie,
                headers=header,
                timeout=timeout,
                proxies=proxies
            )
            if response.status_code != 404:
                result = (target_url, response.status_code, len(response.content))
                print(f"Found {result[0]} - Status: {result[1]} - Length {result[2]}")
                results.append(result)
        except requests.exceptions.RequestException as e;:
            if verbose:
                print(f"Error @ {target_url}: {e}")
            continue
    return results