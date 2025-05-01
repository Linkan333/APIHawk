# APIHawk 🦅

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/yourusername/APIHawk)


# Note this will be put on hold for a few weeks if you would like to contribute just fork this and send an resolvement

APIHawk is a powerful and flexible API security testing tool designed to help security professionals and developers identify vulnerabilities in their APIs. With support for REST, GraphQL, and gRPC APIs, APIHawk provides comprehensive scanning, fuzzing, and crawling capabilities.

## 🚀 Features

- **Multi-Protocol Support**
  - REST API testing
  - GraphQL API analysis
  - gRPC service scanning

- **Advanced Testing Capabilities**
  - Endpoint fuzzing
  - Vulnerability scanning
  - API crawling
  - Authentication testing
  - Rate limit detection

- **Smart Detection**
  - Automatic API type detection
  - Intelligent endpoint discovery
  - Status code analysis
  - Response pattern matching

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Install
```bash
# Clone the repository
git clone https://github.com/yourusername/APIHawk.git
cd APIHawk

# Install in development mode
pip install -e .
```

### Using pip (coming soon)
```bash
pip install apihawk
```

## 🏃‍♂️ Getting Started

### Basic Usage
```bash
# Show help message
python -m apihawk.cli -h

# Scan an API endpoint
python -m apihawk.cli scan --url https://api.example.com --method GET --wordlist wordlists/common.txt

# Fuzz endpoints
python -m apihawk.cli fuzz --url https://api.example.com/FUZZ --method GET --wordlist wordlists/common.txt

# Crawl an API
python -m apihawk.cli crawl --url https://api.example.com --depth 3
```

### Command Options

#### Scan Command
```bash
python -m apihawk.cli scan \
  --url https://api.example.com \
  --method GET \
  --wordlist wordlists/common.txt \
  --timeout 5 \
  --verbose
```

#### Fuzz Command
```bash
python -m apihawk.cli fuzz \
  --url https://api.example.com/FUZZ \
  --method GET \
  --wordlist wordlists/common.txt \
  --cookie "session=xyz" \
  --header "Authorization: Bearer token"
```

## 📚 Documentation

For detailed documentation, please visit:
- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)
- [Contributing Guide](docs/contributing.md)

## 🔧 Configuration

APIHawk can be configured using either command-line arguments or a configuration file. See the [example configuration](examples/sample_config.yaml) for more details.

```yaml
# sample_config.yaml
timeout: 5
headers:
  User-Agent: "APIHawk/1.0.0"
  Authorization: "Bearer YOUR_TOKEN"
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](docs/contributing.md) for details on our code of conduct and the process for submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape APIHawk
- Inspired by various API security testing tools in the community

## 📈 Project Status

APIHawk is under active development. Check the [changelog](docs/changelog.md) for recent updates and new features.

## 📞 Support

- Create an issue for bug reports
- Join our community discussions
- Follow project updates

---

<p align="center">Made by Linkan</p>
