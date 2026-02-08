"""CLI runner for the Risk Analytics Agent."""

from __future__ import annotations

import asyncio
import logging
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from risk_analytics_agent.agent import root_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

APP_NAME = "risk_analytics_agent"
USER_ID = "cli_user"


async def run_cli() -> None:
    """Run the agent in interactive CLI mode."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("Risk Analytics Agent (type 'quit' to exit)")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        )

        print("\nAgent: ", end="", flush=True)
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
        print()


def main() -> None:
    """Entry point for the CLI."""
    asyncio.run(run_cli())


if __name__ == "__main__":
    main()
