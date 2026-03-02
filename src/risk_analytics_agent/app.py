"""Application runner for the Risk Analytics Agent using ADK App and InMemoryRunner.

This module provides both a simple run_debug() interface and an interactive CLI
for running the agent workflow.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from typing import Optional

from google.adk.runners import InMemoryRunner
from google.genai import types

from risk_analytics_agent.agent import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

USER_ID = "cli_user"


async def run_simple(query: str, user_id: str = USER_ID) -> str:
    """Run a single query using run_debug() - simplest approach.
    
    Args:
        query: The user query to process
        user_id: User identifier (optional)
        
    Returns:
        The agent's response as a string
        
    Note:
        Requires ADK Python v1.18.0 or higher for run_debug()
    """
    runner = InMemoryRunner(app=app)
    
    try:
        response = await runner.run_debug(query, user_id=user_id)
        return response
    except AttributeError:
        # Fallback for older ADK versions without run_debug
        logger.warning("run_debug() not available. Please upgrade to ADK >= 1.18.0")
        return await run_single_query(runner, query, user_id)


async def run_single_query(
    runner: InMemoryRunner,
    query: str,
    user_id: str = USER_ID,
    session_id: Optional[str] = None,
) -> str:
    """Run a single query using the runner's run() method.
    
    Args:
        runner: The InMemoryRunner instance
        query: The user query to process
        user_id: User identifier
        session_id: Optional existing session ID
        
    Returns:
        The agent's response as a string
    """
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=query)],
    )
    
    response_parts = []
    async for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_parts.append(part.text)
    
    return "".join(response_parts)


async def run_cli() -> None:
    """Run the agent in interactive CLI mode."""
    runner = InMemoryRunner(app=app)
    
    print("=" * 70)
    print(" " * 15 + "Risk Analytics Agent")
    print("=" * 70)
    print("\nInteractive CLI Mode")
    print("Commands: 'quit', 'exit', 'q' to exit")
    print("-" * 70)

    session_id = None  # Let runner manage session

    while True:
        try:
            user_input = input("\n🔵 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        print("\n🤖 Agent: ", end="", flush=True)
        
        try:
            response = await run_single_query(
                runner=runner,
                query=user_input,
                user_id=USER_ID,
                session_id=session_id,
            )
            print(response)
            
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


def main() -> None:
    """Entry point for the CLI."""
    try:
        asyncio.run(run_cli())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)


async def demo() -> None:
    """Demo function showing simple one-shot queries."""
    print("Running demo queries...\n")
    
    queries = [
        "What can you help me with?",
        "What schemas and tables are available in the liquidity database?",
        "Show me the MLO variance analysis process",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'=' * 70}")
        print(f"Query {i}: {query}")
        print('=' * 70)
        
        try:
            response = await run_simple(query)
            print(f"\nResponse:\n{response}")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    # You can choose how to run:
    # 1. Interactive CLI (default)
    main()
    
    # 2. Or run the demo
    # asyncio.run(demo())
    
    # 3. Or single query
    # asyncio.run(run_simple("Calculate MLO variance for March 1st"))
