"""Main entry point for the Risk Analytics Agent application."""

import asyncio
import sys

from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()


def main():
    """Run the Risk Analytics Agent."""
    # Import here to allow environment variables to load first
    from risk_analytics_agent.app import run_cli, run_simple
    
    # Check if a query was provided as command line argument
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        print(f"Query: {query}\n")
        response = asyncio.run(run_simple(query))
        print(f"Response:\n{response}")
    else:
        # Interactive CLI mode
        asyncio.run(run_cli())


if __name__ == "__main__":
    main()
