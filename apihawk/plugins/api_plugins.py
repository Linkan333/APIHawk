import httpx
import re
import json
from urllib.parse import urlparse
import logging

async def is_grpc_api(url, client):
    """
    Check if the given URL is a gRPC API.
    """
    try:
        response = await client.get(url)
        headers = response.headers
        is_http2 = response.http_version == "HTTP/2"
        is_grpc_content = "application/grpc" in headers.get("Content-Type", "")
        has_grpc_headers = any(h.lower().startswith("grpc-") for h in headers)
        
        
        if response.status_code in (200, 201, 400, 403) and is_http2 and (is_grpc_content or has_grpc_headers):
            logging.info(f"The URL {url} has gRPC API characteristics.")
            return True
        else:
            logging.warning(f"The URL {url} does not have gRPC API characteristics.")
            return False
    except httpx.RequestError as e:
        logging.error(f"Err @ grpc plugin: {e}")
        return False

async def is_graphql_api(url, client):
    """
    Check if the given URL is a GraphQL API.
    """
    payload = {"query": "query { __schema { types { name } } }"}
    try:
        response = await client.get(url)
        headers = response.headers
        is_json = 'application/json' in headers.get('Content-Type', '')
        is_graphql_response = is_json and ('data' in response.json() or 'errors' in response.json())
        if response.status_code in (200, 201, 400, 403) and is_graphql_response:
            logging.info(f"The URL {url} has GraphQL API characteristics.")
            return True
        else:
            loggin.warning(f"The URL {url} does not have GraphQL API characteristics")
            return False
    except httpx.RequestError as e:
        logging.error(f"Err @ graphql plugin: {e}")
        return False
    
async def is_rest_api(url, client):
    """
    Checks if the given URL is a GraphQL API.
    """
    try:
        response = await client.get(url)
        headers = response.headers
        is_json_or_xml = any(ct in headers.get('Content-Type', '') for ct in ['application/json', 'application/xml'])
        is_restful_url = bool(re.match(r'^/api/?(v\d+)?/?[\w-]+(/[\w-]+)*$', urlparse(url).path))
        
        if response.status_code in (200, 201, 400, 403) and is_json_or_xml and is_restful_url:
            logging.info("The URL {url} has RESTful characteristics")
            return True
        else:
            logging.warning("The URL {url} does not have RESTful characteristics")
    except httpx.RequestError as e:
        logging.errro(f"Err @ restful plugin: {e}")
        return False
    
