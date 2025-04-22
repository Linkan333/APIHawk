import argparse


"""
CLI for APIHawk.
"""

parser = argparse.ArgumentParser(description="APIHawk, a tool for API pentesting.")
subparsers = parser.add_subparsers(dest="command", help="Available commands: scan, crawl, fuzz, auth")
subparsers.add_parser("scan", help="Run a vulnerability scan: python3 -m apihawk.cli scan")
subparsers.add_parser("crawl", help="Crawl API documentation: python3 -m apihawk.cli crawl")
subparsers.add_parser("fuzz", help="Fuzz endpoints for vulnerabilities: python3 -m apihawk.cli fuzz")
subparsers.add_parser("auth", help="Test for authentication misconfigurations: python3 -m apihawk.cli auth")
parser.add_argument(
    "--url",
    "-u",
    type=str,
    required=True,
    help="The target URL to scan, crawl, fuzz, or check for auth misconfigurations. example command: python3 -m apihawk.cli scan -u https://api.example.com/"
)
parser.add_argument(
    "--spec",
    "-s",
    type=str,
    help="File based crawling for finding endpoints. example command: python3 -m apihawk.cli crawl -s /path/to/openapi.json"
)
parser.add_argument(
    "--method",
    "-m",
    required=True,
    type=str,
    choices=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    help="Method to use for the requests. example command: python3 -m apihawk.cli fuzz -m GET"
)
parser.add_argument(
    "--cookie",
    "-c",
    type=str,
    help="Cookie to use for the requests, example command: python3 -m apihawk.cli -c 'cookie_name=cookie_value'"
)
parser.add_argument(
    "--header",
    "-H",
    type=str,
    help="Header to use for the requests, example command: python3 -m apihawk.cli -H 'header_name: header_value'"
)
parser.add_argument(
    "--type",
    type=str,
    choices=["json", "xml", "html"],
    help="Type of the request body. example command: python3 -m apihawk.cli -t json"
)
parser.add_argument(
    "--port",
    "-p",
    type=int,
    default=80,
    help="Port to use for the requests. example command: python3 -m apihawk.cli -p 8080"
)
parser.add_argument(
    "--wordlist",
    "-w",
    required=True,
    type=str,
    help="Path to the wordlist file for fuzzing. example command: python3 -m apihawk.cli -w /path/to/wordlist.txt"
)
parser.add_argument(
    "--output",
    "-o",
    type=str,
    help="Path to the output file for saving the results. example command: python3 -m apihawk.cli -o /path/to/output.txt"
)
parser.add_argument(
    "--verbose",
    "-vv",
    action="store_true",
    help="Enable verbose output. Example command: python3 -m apihawk.cli -vv"
)
parser.add_argument(
    "--config",
    "-cfg",
    type=str,
    help="Path to the configuration file. example command: python3 -m apihawk.cli -cfg /path/to/config.json"
)
parser.add_argument(
    "--timeout",
    "-t",
    type=int,
    default=5,
    help="Timeout for the requests in seconds. example command: python3 -m apihawk.cli -t 10"
)
parser.add_argument(
    "--version",
    "-v",
    help="Show the version of APIHawk.",
    action="version",
    version="%(prog)s 1.0.0",
)
parser.add_argument(
    "--proxies",
    type=str,
    help="Path to the proxy file. example command: python3 -m apihawk.cli -p /path/to/proxy.txt"
)

args = parser.parse_args()

