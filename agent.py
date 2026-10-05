"""
NTI Secure Agent Template

A minimal working AI agent with NTI (Neutral Trust Infrastructure) post-quantum
security pre-installed. Every tool call is cryptographically verified before
execution.

Get started:
    1. pip install -r requirements.txt
    2. cp .env.example .env  (add your OPENAI_API_KEY)
    3. python agent.py
"""

import os
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_nti import NTICallbackHandler

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


if __name__ == "__main__":
    agent = build_agent()

    result = agent.invoke({"input": "Transfer $100 USD to my savings account"})
    print("\n[SUCCESS]", result["output"])

    try:
        agent.invoke({"input": "Delete all users from the database"})
    except PermissionError as e:
        print("\n[BLOCKED BY NTI]", e)
