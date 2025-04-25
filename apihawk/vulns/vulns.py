import asyncio
import requests
import json
from typing import Optional, List

async def vuln_functionality(
    url: str,
    wordlist: List[str],
    method: str,
    cookie: Optional[str] = None,
    header: Optional[str] = None,
    timeout: int = 5,
    proxies: Optional[dict] = None,
    verbose: bool = False,
    delay: float = 0.1
) -> dict:
    """
    Perform API vulnerability scanning for GraphQL endpoints.
    
    Args:
        url (str): The target URL to scan.
        wordlist (List[str]): List of payloads or endpoints to test.
        method (str): HTTP method to use (GET, POST, PUT, DELETE).
        cookie (str): Cookie to use for requests.
        header (str): Header to use for requests.
        timeout (int): Request timeout in seconds.
        proxies (dict): Proxy settings for requests.
        verbose (bool): Print detailed output.
        delay (float): Delay between requests to avoid rate-limiting.
    
    Returns:
        dict: Scan results with detected vulnerabilities.
    """
    results = {
        "url": url,
        "vulnerabilities": [],
        "errors": []
    }

    headers = {"Content-Type": "application/json"}
    if header:
        headers.update(json.loads(header))
    if cookie:
        headers["Cookie"] = cookie

    async def send_request(payload: str) -> Optional[dict]:
        """Helper to send HTTP request asynchronously."""
        try:
            if method.upper() == "GET":
                response = requests.get(
                    url, params={"query": payload}, headers=headers, timeout=timeout, proxies=proxies
                )
            else:
                response = requests.request(
                    method.upper(), url, json={"query": payload}, headers=headers, timeout=timeout, proxies=proxies
                )
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            results["errors"].append(f"Request failed for payload {payload}: {str(e)}")
            return None
        finally:
            await asyncio.sleep(delay)

    # Vulnscan 1: Instrospection Query Exposure
    async def test_introspection():
        introspection_query = """
        query { __schema { types { name fields { name } } } }
        """
        response = await send_request(introspection_query)
        if response and "__schema" in response.get("data", {}):
            results["vulnerabilities"].append({
                "type": "Introspection Exposure",
                "details": "Introspection query returned schema details.",
                "payload": introspection_query
            })
            if verbose:
                print(f"[!] Introspection vulnerability found at {url}")
    
    # Vulnscan 2: IDOR (Insecure Direct Object Reference)
    async def test_idor():
        idor_query = """
        query { user(id: "%s") { id name email} }
        """

        for id in ["1", "2", "9999"]:
            response = await send_request(idor_query % id)
            if response and response.get("data", {}).get("user"):
                user_data = response["data"]["user"]
                if user_data.get("email"):
                    results["vulnerabilities"].append({
                        "type": "IDOR",
                        "details": f"Unauthorized access to user data with ID {id}",
                        "payload": idor_query % id
                    })
                    if verbose:
                        print(f"[!] IDOR Vulnerability found for ID {id} at {url}")

    # Vulnscan 3: Verbose Error Messages
    async def test_verbose_errors():
        malformed_query = """
        query { invalidField { name } }
        """
        response = await send_request(malformed_query)
        if response and "errors" in response:
            for error in response["errors"]:
                if any(keyword in error.get("message", "").lower() for keyword in ["stacktrace", "sql", "exception"]):
                    results["vulnerabilities"].append({
                        "type": "Verbose Error Messages",
                        "details": "Error message contains sensitive information.",
                        "payload": malformed_query
                    })
                    if verbose:
                        print(f"[!] Verbose error vulnerability found at {url}")
    
    # Vulnscan 4: DoS via Complex Queries
    async def test_dos_complexity():
        complex_query = """
        query { user(id: "1") { friends { friends { friends { name } } } } }
        """
        start_time = asyncio.get_event_loop().time()
        response = await send_request(complex_query)
        elapsed_time = asyncio.get_event_loop().time() - start_time
        if elapsed_time > timeout or (response and "errors" in response and "timeout" in str(response["errors"]).lower()):
            results["vulnerabilities"].append({
                "type": "DoS via Complex Queries",
                "details": f"Complex query caused high latency or timeout (elapsed: {elapsed_time:.2f}s).",
                "payload": complex_query
            })
            if verbose:
                print(f"[!] DoS vulnerability found at {url}")


    await asyncio.gather(
        test_introspection(),
        test_idor(),
        test_verbose_errors(),
        test_dos_complexity()
    )

    return results


"""
async def main():
    url = "http://example.com/graphql"
    wordlist = []  # Not used in this example, but could include payloads
    results = await vuln_functionality(
        url=url,
        wordlist=wordlist,
        method="POST",
        verbose=True
    )
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
"""