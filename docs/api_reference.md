# APIHawk API Reference

## Core Modules

### Scanner Module
```python
async def scanner(url, wordlist, method, cookie=None, header=None, timeout=5, proxies=None, verbose=False, delay=0.1)
```
Performs comprehensive API scanning and reconnaissance.

#### Parameters
- `url` (str): Target URL to scan
- `wordlist` (str): Path to wordlist file
- `method` (str): HTTP method (GET, POST, PUT, DELETE)
- `cookie` (str, optional): Cookie string for requests
- `header` (dict, optional): Custom headers for requests
- `timeout` (int, optional): Request timeout in seconds. Default: 5
- `proxies` (dict, optional): Proxy configuration
- `verbose` (bool, optional): Enable verbose output. Default: False
- `delay` (float, optional): Delay between requests in seconds. Default: 0.1

#### Returns
List of discovered endpoints and their properties

### Fuzzer Module
```python
async def fuzz_endpoint(url, wordlist, method, client, cookie=None, header=None, timeout=5, proxies=None, verbose=False)
```
Performs endpoint fuzzing to discover hidden endpoints and parameters.

#### Parameters
Similar to scanner module, plus:
- `client` (httpx.AsyncClient): Async HTTP client instance

#### Returns
List of fuzzing results with endpoint details

### API Detection Plugins

#### REST API Detection
```python
async def is_rest_api(url, client)
```
Detects REST API endpoints by analyzing response patterns and headers.

#### GraphQL Detection
```python
async def is_graphql_api(url, client)
```
Identifies GraphQL APIs through introspection queries and response analysis.

#### gRPC Detection
```python
async def is_grpc_api(url, client)
```
Detects gRPC services by analyzing HTTP/2 and protocol-specific patterns.

## Command Line Interface

### Global Options
- `--verbose, -v`: Enable verbose output
- `--timeout, -t`: Request timeout in seconds
- `--config`: Path to configuration file

### Scan Command
```bash
apihawk scan [options]
```
Options specific to scan command:
- `--url, -u`: Target URL
- `--method, -m`: HTTP method
- `--wordlist, -w`: Wordlist path

### Fuzz Command
```bash
apihawk fuzz [options]
```
Options specific to fuzz command:
- `--url, -u`: Target URL with FUZZ placeholder
- `--method, -m`: HTTP method
- `--wordlist, -w`: Wordlist path

## Configuration File Format

### YAML Structure
```yaml
scan:
  timeout: 5
  delay: 0.1
  headers:
    User-Agent: "APIHawk/1.0.0"
  
fuzz:
  timeout: 3
  max_concurrent: 10

proxies:
  http: "http://proxy:8080"
  https: "https://proxy:8080"
```

## Error Handling

### Common Exceptions
- `ConnectionError`: Network connectivity issues
- `TimeoutError`: Request timeout
- `AuthenticationError`: Authentication failures
- `RateLimitError`: Rate limiting detected

### Response Status Codes
- 200-299: Successful responses
- 400-499: Client errors
- 500-599: Server errors