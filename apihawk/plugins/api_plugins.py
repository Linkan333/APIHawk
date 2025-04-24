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
        response = await client.post(url, json=payload)  # Fixed: GET -> POST
        headers = response.headers
        is_json = 'application/json' in headers.get('Content-Type', '')
        is_graphql_response = is_json and ('data' in response.json() or 'errors' in response.json())
        if response.status_code in (200, 201, 400, 403) and is_graphql_response:
            logging.info(f"The URL {url} has GraphQL API characteristics.")
            return True
        else:
            logging.warning(f"The URL {url} does not have GraphQL API characteristics.")  # Fixed: loggin -> logging
            return False
    except (httpx.RequestError, json.JSONDecodeError) as e:
        logging.error(f"Err @ graphql plugin: {e}")
        return False
    
async def is_rest_api(url, client):
    """
    Check if the given URL is a REST API.
    """
    try:
        response = await client.get(url)
        headers = response.headers
        is_json_or_xml = any(ct in headers.get('Content-Type', '') for ct in ['application/json', 'application/xml'])
        is_restful_url = bool(re.match(r'^/(api/|v\d+/)?[\w-]+(/[\w-]+)*$', urlparse(url).path))
        
        if response.status_code in (200, 201, 400, 403) and is_json_or_xml and is_restful_url:
            logging.info(f"The URL {url} has REST API characteristics.")
            return True
        else:
            logging.warning(f"The URL {url} does not have REST API characteristics.")
            return False
    except httpx.RequestError as e:
        logging.error(f"Err @ rest plugin: {e}")
        return False

async def get_api_endpoints(base_url, auth_headers=None):
    """
    Discover API endpoints for gRPC, GraphQL, and REST.
    Returns a dictionary with detected API types and their endpoints.
    """
    common_endpoints = {
        'grpc': [
            '/grpc.health.v1.Health/Check',
            '/UserService/GetUser',
            '/OrderService/CreateOrder',
            '/ProductService/ListProducts',
            '/PaymentService/ProcessPayment'
        ],
        'graphql': [
            '/graphql',
            '/api/graphql',
            '/query',
            '/v1/graphql',
            '/gql',
            '/graph'
        ],
        'rest': [
            '/api/v1/users',
            '/api/v2/orders',
            '/api/products',
            '/v1/customers',
            '/api/v1/auth'
        ]
    }
    
    results = {'grpc': [], 'graphql': [], 'rest': []}
    
    async with httpx.AsyncClient(http2=True, headers=auth_headers, timeout=5) as client:
        for api_type, endpoints in common_endpoints.items():
            for endpoint in endpoints:
                endpoint_url = base_url.rstrip('/') + endpoint
                if api_type == 'grpc' and await is_grpc_api(endpoint_url, client):
                    results['grpc'].append(endpoint_url)
                elif api_type == 'graphql' and await is_graphql_api(endpoint_url, client):
                    results['graphql'].append(endpoint_url)
                elif api_type == 'rest' and await is_rest_api(endpoint_url, client):
                    results['rest'].append(endpoint_url)
    return {
        'url': base_url,
        'apis_detected': {
            'grpc': results['grpc'],
            'graphql': results['graphql'],
            'rest': results['rest']
        }
    }