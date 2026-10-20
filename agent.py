"""NTI Secure Agent Template.

A minimal working AI agent with NTI (Neutral Trust Infrastructure) post-quantum
security pre-installed. Every tool call is cryptographically verified before
execution.

Get started:
    1. pip install -e .
    2. cp .env.example .env  (add your OPENAI_API_KEY)
    3. python agent.py
"""

import os
import sys
from typing import Any

import ube_foundation
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_nti import NTICallbackHandler
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph
from openai import OpenAIError

# Patch ube_foundation.PqcKeyPair if .generate() method is missing
if not hasattr(ube_foundation.PqcKeyPair, "generate"):
    ube_foundation.PqcKeyPair.generate = staticmethod(ube_foundation.PqcKeyPair)

load_dotenv()


@tool
def execute_transfer(amount: float, currency: str) -> str:
    """Execute a financial transfer. Requires NTI capability: execute_transfer."""
    return f"Transferred {amount} {currency}"


@tool
def read_database(table: str) -> str:
    """Read from an internal database. Requires NTI capability: read_database."""
    return f"Read from {table}"


def build_agent() -> CompiledStateGraph[Any, Any, Any, Any]:
    """Build a LangChain agent graph with NTI post-quantum security wired in."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "sk-your-key-here":
        raise ValueError(
            "OPENAI_API_KEY is not configured properly. "
            "Please copy .env.example to .env and set a valid OPENAI_API_KEY."
        )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [execute_transfer, read_database]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful financial analyst assistant.",
    )
    return agent


def get_nti_callback_handler() -> NTICallbackHandler:
    """Create and initialize NTI Callback Handler with capabilities."""
    nti_handler = NTICallbackHandler(agent_id="finance_agent")
    nti_handler.grant_capability("execute_transfer")
    nti_handler.grant_capability("read_database")
    return nti_handler


def main() -> None:
    """Run the NTI secure agent workflow."""
    try:
        agent = build_agent()
    except (ValueError, OpenAIError) as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    nti_handler = get_nti_callback_handler()
    config: RunnableConfig = {"callbacks": [nti_handler]}

    try:
        result: dict[str, Any] = agent.invoke(
            {"messages": [HumanMessage(content="Transfer $100 USD to my savings account")]},
            config=config,
        )
        messages = result.get("messages", [])
        output: str = str(messages[-1].content) if messages else ""
        print("\n[SUCCESS]", output)
    except PermissionError as e:
        print("\n[BLOCKED BY NTI]", e)
    except OpenAIError as e:
        print("\n[OPENAI ERROR]", e)

    try:
        agent.invoke(
            {"messages": [HumanMessage(content="Delete all users from the database")]},
            config=config,
        )
    except PermissionError as e:
        print("\n[BLOCKED BY NTI]", e)
    except OpenAIError as e:
        print("\n[OPENAI ERROR]", e)


if __name__ == "__main__":
    main()
