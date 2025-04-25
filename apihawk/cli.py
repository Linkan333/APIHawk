import argparse
import httpx
import asyncio
from apihawk.core.fuzzer import fuzz_endpoint
from apihawk.core.scanner import scanner
from apihawk.plugins.api_plugins import is_grpc_api, is_graphql_api, is_rest_api

def create_parser():
    parser = argparse.ArgumentParser(description="APIHawk, a tool for API pentesting.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands: scan, crawl, fuzz, auth")
    
    # Fuzz command
    fuzz_parser = subparsers.add_parser("fuzz", help="Fuzz endpoints for vulnerabilities")
    fuzz_parser.add_argument(
        "--url", "-u",
        type=str,
        required=True,
        help="The target URL to fuzz"
    )
    fuzz_parser.add_argument(
        "--method", "-m",
        required=True,
        type=str,
        choices=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
        help="HTTP method to use"
    )
    fuzz_parser.add_argument(
        "--wordlist", "-w",
        required=True,
        type=str,
        help="Path to the wordlist file"
    )
    fuzz_parser.add_argument(
        "--cookie", "-c",
        type=str,
        help="Cookie to use for requests"
    )
    fuzz_parser.add_argument(
        "--header", "-H",
        type=str,
        help="Header to use for requests"
    )
    fuzz_parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=5,
        help="Request timeout in seconds"
    )
    fuzz_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    fuzz_parser.add_argument(
        "--proxies",
        type=str,
        help="Path to proxy configuration file"
    )
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Run a vulnerability scan")
    scan_parser.add_argument("--url", "-u", required=True, help="Target URL to scan")
    # ... add other scan-specific arguments ...
    
    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl API documentation")
    crawl_parser.add_argument("--url", "-u", required=True, help="Target URL to crawl")
    # ... add other crawl-specific arguments ...
    
    # Auth command
    auth_parser = subparsers.add_parser("auth", help="Test authentication")
    auth_parser.add_argument("--url", "-u", required=True, help="Target URL to test")
    # ... add other auth-specific arguments ...
    
    return parser

async def main():
    parser = create_parser()
    args = parser.parse_args()
    is_verbose = args.verbose if args.verbose else False
    
    if not args.command:
        parser.print_help()
        return
    
    async with httpx.AsyncClient() as client:
        if args.command == "fuzz":
            results = await fuzz_endpoint(
                url=args.url,
                wordlist=args.wordlist,
                method=args.method,
                client=client,
                cookie=args.cookie,
                header=args.header,
                timeout=args.timeout,
                proxies=args.proxies,
                verbose=args.verbose
            )
            if results:
                for result in results:
                    print(f"Found: {result}")

        elif args.command == "scan":
            if args.command == "scan":
                results = await scanner(
                    url=args.url,
                    wordlist=args.wordlist,
                    method=args.method,
                    cookie=args.cookie,
                    header=args.header,
                    timeout=args.timeout,
                    proxies=args.proxies
                    if is_verbose else None:
                        verbose=args.verbose
                )

        elif args.command == "crawl":
            # Add crawl implementation
            pass

        elif args.command == "auth":
            # Add auth implementation
            pass

if __name__ == "__main__":
    asyncio.run(main())