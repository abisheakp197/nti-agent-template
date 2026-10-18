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
from dotenv import load_dotenv

import ube_foundation
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_nti import NTICallbackHandler
from langchain_openai import ChatOpenAI
from openai import OpenAIError

# Patch ube_foundation.PqcKeyPair if .generate() method is missing
if not hasattr(ube_foundation.PqcKeyPair, "generate"):
    setattr(
        ube_foundation.PqcKeyPair,
        "generate",
        staticmethod(ube_foundation.PqcKeyPair),
    )

load_dotenv()


@tool
def execute_transfer(amount: float, currency: str) -> str:
    """Execute a financial transfer. Requires NTI capability: execute_transfer."""
    return f"Transferred {amount} {currency}"


@tool
def read_database(table: str) -> str:
    """Read from an internal database. Requires NTI capability: read_database."""
    return f"Read from {table}"


def build_agent() -> AgentExecutor:
    """Build a LangChain agent with NTI post-quantum security wired in."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "sk-your-key-here":
        raise ValueError(
            "OPENAI_API_KEY is not configured properly. "
            "Please copy .env.example to .env and set a valid OPENAI_API_KEY."
        )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [execute_transfer, read_database]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful financial analyst assistant."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_openai_tools_agent(llm, tools, prompt)

    nti_handler = NTICallbackHandler(agent_id="finance_agent")
    nti_handler.grant_capability("execute_transfer")
    nti_handler.grant_capability("read_database")

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        callbacks=[nti_handler],
        verbose=True,
    )
    return executor


def main() -> None:
    """Run the NTI secure agent workflow."""
    try:
        agent = build_agent()
    except (ValueError, OpenAIError) as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result = agent.invoke({"input": "Transfer $100 USD to my savings account"})
        output: str = str(result.get("output", ""))
        print("\n[SUCCESS]", output)
    except PermissionError as e:
        print("\n[BLOCKED BY NTI]", e)
    except OpenAIError as e:
        print("\n[OPENAI ERROR]", e)

    try:
        agent.invoke({"input": "Delete all users from the database"})
    except PermissionError as e:
        print("\n[BLOCKED BY NTI]", e)
    except OpenAIError as e:
        print("\n[OPENAI ERROR]", e)


if __name__ == "__main__":
    main()
