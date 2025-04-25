# APIHawk User Guide

This guide will help you get started with APIHawk and explore its features in detail.

## Table of Contents
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Installation

### System Requirements
- Python 3.8 or higher
- pip package manager
- Required disk space: ~100MB
- Memory: 256MB minimum, 512MB recommended

### Installation Methods

#### From Source
```bash
git clone https://github.com/yourusername/APIHawk.git
cd APIHawk
pip install -e .
```

#### Using pip (Coming Soon)
```bash
pip install apihawk
```

## Basic Usage

### Command Line Interface
APIHawk provides a command-line interface with several subcommands:

#### Scan Command
Used for comprehensive API endpoint scanning:
```bash
python -m apihawk.cli scan --url https://api.example.com --method GET --wordlist wordlists/common.txt
```

Options:
- `--url, -u`: Target URL to scan
- `--method, -m`: HTTP method (GET, POST, PUT, DELETE)
- `--wordlist, -w`: Path to wordlist file
- `--timeout, -t`: Request timeout in seconds
- `--verbose, -v`: Enable verbose output
- `--cookie, -c`: Cookie string for requests
- `--header, -H`: Custom header for requests
- `--proxies`: Proxy configuration file

#### Fuzz Command
For endpoint fuzzing and discovery:
```bash
python -m apihawk.cli fuzz --url https://api.example.com/FUZZ --method GET --wordlist wordlists/common.txt
```

Options: (Same as scan command)

### API Type Detection
APIHawk automatically detects the type of API:
- REST APIs
- GraphQL APIs
- gRPC Services

## Advanced Features

### Rate Limiting
APIHawk implements smart rate limiting to avoid triggering API defenses:
```bash
python -m apihawk.cli scan --url https://api.example.com --method GET --wordlist wordlists/common.txt --delay 0.5
```

### Authentication Testing
Test various authentication mechanisms:
```bash
python -m apihawk.cli auth --url https://api.example.com/auth --wordlist wordlists/auth.txt
```

### Custom Wordlists
Create and use custom wordlists for specific targets:
1. Create a text file with one endpoint per line
2. Use the file with the --wordlist parameter

## Configuration

### Config File
Create a `config.yaml` file in your project directory:
```yaml
timeout: 5
headers:
  User-Agent: "APIHawk/1.0.0"
delay: 0.1
proxies:
  http: "http://proxy.example.com:8080"
  https: "https://proxy.example.com:8080"
```

### Environment Variables
APIHawk supports configuration via environment variables:
- `APIHAWK_TIMEOUT`: Default request timeout
- `APIHAWK_USER_AGENT`: Custom User-Agent string
- `APIHAWK_PROXY`: Proxy server URL

## Troubleshooting

### Common Issues

1. Connection Errors
```
Error: Could not reach base URL
Solution: Check network connectivity and proxy settings
```

2. Rate Limiting
```
Error: Too many requests
Solution: Increase delay between requests using --delay parameter
```

3. Authentication Failures
```
Error: 401 Unauthorized
Solution: Verify credentials and token validity
```

### Logging
Enable verbose logging for detailed output:
```bash
python -m apihawk.cli scan --url https://api.example.com --verbose
```

### Getting Help
- Create an issue on GitHub
- Check existing issues for solutions
- Join the community discussion