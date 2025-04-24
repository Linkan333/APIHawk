# apihawk/core/fuzzer.py
import httpx
import os
import logging
from ..plugins.api_plugins import is_grpc_api, is_graphql_api, is_rest_api

async def fuzz_endpoint(url, wordlist, method, client=None, cookie=None, header=None, timeout=5, proxies=None, verbose=False):
    """
    Fuzz a URL with a wordlist to discover API endpoints.
    Returns a list of dictionaries with URL and API type.
    """
    if "FUZZ" not in url:
        logging.error("No FUZZ placeholder in URL")
        return None
    if method.upper() not in ("GET", "POST", "PUT", "DELETE"):
        logging.error(f"Invalid HTTP method: {method}")
        return None
    if not os.path.exists(wordlist):
        logging.error(f"Wordlist file not found: {wordlist}")
        return None

    try:
        with open(wordlist, 'r') as f:
            fuzzer_urls = [line.strip() for line in f if line.strip()]
    except IOError as e:
        logging.error(f"Error reading wordlist: {e}")
        return None

    headers = header or {}
    if cookie:
        headers['Cookie'] = cookie

    client = client or httpx.AsyncClient(http2=True, timeout=timeout, proxies=proxies)
    results = []

    for payload in fuzzer_urls:
        target_url = url.replace("FUZZ", payload)
        if verbose:
            logging.info(f"Testing {target_url}")

        try:
            if method.upper() == "POST":
                payload_data = {"query": "query { __schema { types { name } } }"} if "graphql" in target_url.lower() else {}
                response = await client.request(method.upper(), target_url, json=payload_data, headers=headers)
            else:
                response = await client.request(method.upper(), target_url, headers=headers)

            if response.status_code in (200, 201, 400, 403):
                api_type = None
                if await is_grpc_api(target_url, client):
                    api_type = "gRPC"
                elif await is_graphql_api(target_url, client):
                    api_type = "GraphQL"
                elif await is_rest_api(target_url, client):
                    api_type = "REST"
                
                if api_type:
                    result = {"url": target_url, "type": api_type, "status": response.status_code, "content_length": len(response.content)}
                    logging.info(f"Found {result['url']} - Type: {result['type']} - Status: {result['status']} - Length: {result['content_length']}")
                    results.append(result)
        except httpx.RequestError as e:
            if verbose:
                logging.error(f"Error @ {target_url}: {e}")
            continue

    return results if results else None