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
    fuzz_parser = subparsers.add_parser("fuzz", help="Fuzz urls for hidden endpioints. for help type python apihawk fuzz -h")
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
    scan_parser = subparsers.add_parser("scan", help="Run a vulnerability scan on the target API. for help type python apihawk scan -h")
    scan_parser.add_argument(
        "--url", "-u",
        required=True,
        help="Target URL to scan"
    )
    scan_parser.add_argument(
        "--method", "-m",
        required=True,
        type=str,
        choices=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
        help="HTTP method to use"
    )
    scan_parser.add_argument(
        "--wordlist", "-w",
        required=True,
        type=str,
        help="Path to the wordlist file"
    )
    scan_parser.add_argument(
        "--cookie", "-c",
        type=str,
        help="Cookie to use for requests"
    )
    scan_parser.add_argument(
        "--header", "-H",
        type=str,
        help="Header to use for requests"
    )
    scan_parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=5,
        help="Request timeout in seconds"
    )
    scan_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    scan_parser.add_argument(
        "--proxies",
        type=str,
        help="Path to proxy configuration file"
    )
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
            # Check API type first
            is_grpc = await is_grpc_api(args.url, client)
            is_graphql = await is_graphql_api(args.url, client)
            is_rest = await is_rest_api(args.url, client)
            
            # Run scanner
            results = await scanner(
                url=args.url,
                wordlist=args.wordlist,
                cookie=args.cookie,
                header=args.header,
                method=args.method,
                timeout=args.timeout,
                proxies=args.proxies,
                verbose=args.verbose
            )
            
            # Print results if we found anything
            found_something = False
            
            # Print API type if it was detected
            if is_grpc:
                print(f"Found: gRPC API at {args.url}")
                found_something = True
            elif is_graphql:
                print(f"Found: GraphQL API at {args.url}")
                found_something = True
            elif is_rest:
                print(f"Found: REST API at {args.url}")
                found_something = True
            
            # Print scanner results if any
            if results:
                for result in results:
                    print(f"Found: {result}")
                found_something = True
            
            # Print default finding if nothing else was found
            if not found_something:
                print(f"Found: {args.url}")

        elif args.command == "crawl":
            # Add crawl implementation
            pass

        elif args.command == "auth":
            # Add auth implementation
            pass

if __name__ == "__main__":
    asyncio.run(main())