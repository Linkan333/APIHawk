# tests/test_cases.py
import pytest
import httpx
import pytest_asyncio
from unittest.mock import patch, Mock, mock_open
from apihawk.core.fuzzer import fuzz_endpoint
from apihawk.plugins.api_plugins import is_grpc_api, is_graphql_api, is_rest_api
from apihawk.cli import main

# Mock wordlist for fuzzer tests
WORDLIST_CONTENT = "users\nposts\ngraphql\nhealth\ncheck"

@pytest_asyncio.fixture
async def http_client():
    async with httpx.AsyncClient(http2=True, timeout=5) as client:
        yield client

@pytest.fixture
def mock_open_wordlist():
    with patch("builtins.open", mock_open(read_data=WORDLIST_CONTENT)) as m:
        yield m

# gRPC Tests
@pytest.mark.asyncio
async def test_grpc_api_google_cloud(http_client):
    """Test detection of a gRPC API (Google Cloud Pub/Sub)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/grpc"}
    mock_response.http_version = "HTTP/2"

    with patch.object(httpx.AsyncClient, "get", return_value=mock_response):
        result = await is_grpc_api("https://pubsub.googleapis.com/google.pubsub.v1.Publisher/Publish", http_client)
        assert result is True

@pytest.mark.asyncio
async def test_invalid_grpc_api(http_client):
    """Test detection of a non-gRPC API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.http_version = "HTTP/1.1"

    with patch.object(httpx.AsyncClient, "get", return_value=mock_response):
        result = await is_grpc_api("https://example.com", http_client)
        assert result is False

# GraphQL Tests
@pytest.mark.asyncio
async def test_graphql_api_github(http_client):
    """Test detection of GitHub's GraphQL API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"data": {"__schema": {"types": [{"name": "Query"}]}}}

    with patch.object(httpx.AsyncClient, "post", return_value=mock_response):
        result = await is_graphql_api("https://api.github.com/graphql", http_client)
        assert result is True

@pytest.mark.asyncio
async def test_invalid_graphql_api(http_client):
    """Test detection of a non-GraphQL API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"message": "Not a GraphQL API"}

    with patch.object(httpx.AsyncClient, "post", return_value=mock_response):
        result = await is_graphql_api("https://api.github.com", http_client)
        assert result is False

# REST Tests
@pytest.mark.asyncio
async def test_rest_api_jsonplaceholder(http_client):
    """Test detection of JSONPlaceholder's REST API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = [{"id": 1, "name": "Leanne Graham"}]

    with patch.object(httpx.AsyncClient, "get", return_value=mock_response):
        result = await is_rest_api("https://jsonplaceholder.typicode.com/users", http_client)
        assert result is True

@pytest.mark.asyncio
async def test_invalid_rest_api(http_client):
    """Test detection of a non-REST API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html"}

    with patch.object(httpx.AsyncClient, "get", return_value=mock_response):
        result = await is_rest_api("https://example.com", http_client)
        assert result is False

# Fuzzer Tests
@pytest.mark.asyncio
async def test_fuzz_rest_jsonplaceholder(mock_open_wordlist, http_client):
    """Test fuzzer on JSONPlaceholder REST API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = [{"id": 1, "name": "Leanne Graham"}]
    mock_response.content = b"Mock content"

    with patch.object(httpx.AsyncClient, "get", return_value=mock_response):
        with patch.object(httpx.AsyncClient, "post", return_value=mock_response):  # For GraphQL detection
            result = await fuzz_endpoint("https://jsonplaceholder.typicode.com/FUZZ", "wordlist.txt", "GET", client=http_client)
            assert isinstance(result, list)
            assert any(r["url"] == "https://jsonplaceholder.typicode.com/users" and r["type"] == "REST" for r in result)

@pytest.mark.asyncio
async def test_fuzz_graphql_github(mock_open_wordlist, http_client):
    """Test fuzzer on GitHub GraphQL API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"data": {"__schema": {"types": [{"name": "Query"}]}}}
    mock_response.content = b"Mock content"

    with patch.object(httpx.AsyncClient, "post", return_value=mock_response):
        with patch.object(httpx.AsyncClient, "get", return_value=mock_response):  # For REST detection
            result = await fuzz_endpoint("https://api.github.com/FUZZ", "wordlist.txt", "POST", client=http_client)
            assert isinstance(result, list)
            assert any(r["url"] == "https://api.github.com/graphql" and r["type"] == "GraphQL" for r in result)

@pytest.mark.asyncio
async def test_invalid_wordlist(http_client):
    """Test fuzzer with nonexistent wordlist."""
    result = await fuzz_endpoint("https://example.com/FUZZ", "nonexistent.txt", "GET", client=http_client)
    assert result is None

@pytest.mark.asyncio
async def test_invalid_url(http_client):
    """Test fuzzer with invalid URL."""
    result = await fuzz_endpoint("http://invalid-url..com/FUZZ", "wordlist.txt", "POST", client=http_client)
    assert result is None

@pytest.mark.asyncio
async def test_invalid_method(http_client):
    """Test fuzzer with invalid HTTP method."""
    result = await fuzz_endpoint("https://example.com/FUZZ", "wordlist.txt", "INVALID", client=http_client)
    assert result is None

@pytest.mark.asyncio
async def test_invalid_fuzz(http_client):
    """Test fuzzer with URL lacking FUZZ."""
    result = await fuzz_endpoint("https://example.com/", "wordlist.txt", "GET", client=http_client)
    assert result is None
    
    
# ----- CLI TESTS -----
@pytest.fixture
def mock_client():
    client = Mock()
    
    async def mock_request(*args, **kwargs):
        return Mock(
            status_code=200,
            headers={"Content-Type": "application/json"},
            json=lambda: {"data": {"test": "success"}},
            content=b"test content",
            http_version="HTTP/2"
        )
    
    async def mock_get(*args, **kwargs):
        return await mock_request(*args, **kwargs)
        
    async def mock_post(*args, **kwargs):
        return await mock_request(*args, **kwargs)
        
    client.request = mock_request
    client.get = mock_get
    client.post = mock_post
    return client

@pytest.fixture
def mock_fuzz_endpoint():
    async def mock_fuzz(*args, **kwargs):
        return [
            {"url": "http://example.com/api/v1", "status": 200, "type": "endpoint"},
            {"url": "http://example.com/api/v2", "status": 404, "type": "endpoint"}
        ]
    return mock_fuzz

@pytest.mark.asyncio
async def test_fuzz_command(mock_client, mock_fuzz_endpoint, capsys):
    # Arrange
    test_args = [
        "fuzz",
        "--url", "http://example.com/api/FUZZ",
        "--method", "GET",
        "--wordlist", "tests/fixtures/sample_wordlist.txt",
        "--verbose"
    ]
    
    with patch("sys.argv", ["apihawk"] + test_args), \
         patch("apihawk.core.fuzzer.fuzz_endpoint", mock_fuzz_endpoint), \
         patch("httpx.AsyncClient") as mock_async_client:
        
        mock_async_client.return_value.__aenter__.return_value = mock_client
        
        # Act
        await main()
        
        # Assert
        captured = capsys.readouterr()
        assert "Found: " in captured.out
        assert "http://example.com/api/v1" in captured.out
        assert "http://example.com/api/v2" in captured.out

@pytest.mark.asyncio
async def test_fuzz_command_no_results(mock_client, capsys):
    # Arrange
    async def mock_empty_fuzz(*args, **kwargs):
        return []

    test_args = [
        "fuzz",
        "--url", "http://example.com",
        "--method", "GET",
        "--wordlist", "tests/fixtures/sample_wordlist.txt"
    ]
    
    with patch("sys.argv", ["apihawk"] + test_args), \
         patch("apihawk.core.fuzzer.fuzz_endpoint", mock_empty_fuzz), \
         patch("httpx.AsyncClient") as mock_async_client:
        
        mock_async_client.return_value.__aenter__.return_value = mock_client
        
        # Act
        await main()
        
        # Assert
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

@pytest.mark.asyncio
async def test_fuzz_command_with_invalid_url():
    # Arrange
    test_args = [
        "fuzz",
        "--url", "invalid-url",
        "--method", "GET",
        "--wordlist", "tests/fixtures/sample_wordlist.txt"
    ]
    
    with patch("sys.argv", ["apihawk"] + test_args), \
         patch("httpx.AsyncClient") as mock_async_client:
        
        mock_async_client.return_value.__aenter__.side_effect = httpx.RequestError("Invalid URL")
        
        # Act & Assert
        with pytest.raises(httpx.RequestError):
            await main()
            
#############
#           #
# SCAN TEST #
#           #
#############
@pytest.fixture
def mock_scan_endpoint():
    async def mock_scan(*args, **kwargs):
        return [
            {"url": "http://example.com/", "status": 200, "type": "endpoint"},
            {"url": "http://example.com/", "status": 404, "type": "endpoint"}
        ]
    return mock_scan

@pytest.mark.asyncio
async def test_scan_command(mock_client, mock_scan_endpoint, capsys):
    # Arrange
    test_args = [
        "scan",
        "--url", "http://example.com/",
        "--method", "GET",
        "--wordlist", "tests/fixtures/sample_wordlist.txt",
        "--verbose"
    ]
    
    with patch("sys.argv", ["apihawk"] + test_args), \
         patch("apihawk.core.scanner.scanner", mock_scan_endpoint), \
         patch("httpx.AsyncClient") as mock_async_client:
        
        mock_async_client.return_value.__aenter__.return_value = mock_client
        
        # Act
        await main()
        
        # Assert
        captured = capsys.readouterr()
        assert "Found: " in captured.out
        assert "http://example.com/" in captured.out
        assert "http://example.com/" in captured.out

@pytest.mark.asyncio
async def test_scan_command_with_invalid_url():
    # Arrange
    test_args = [
        "scan",
        "--url", "invalid-url",
        "--method", "GET",
        "--wordlist", "tests/fixtures/sample_wordlist.txt"
    ]
    
    with patch("sys.argv", ["apihawk"] + test_args), \
         patch("httpx.AsyncClient") as mock_async_client:
        
        mock_async_client.return_value.__aenter__.side_effect = httpx.RequestError("Invalid URL")
        
        # Act & Assert
        with pytest.raises(httpx.RequestError):
            await main()

#############
#           #
# CRAWL TEST#
#           #
#############