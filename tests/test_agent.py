"""Tests for NTI Secure Agent Template."""

import pytest
from langgraph.graph.state import CompiledStateGraph

from agent import build_agent, execute_transfer, get_nti_callback_handler, read_database


def test_tools_functionality() -> None:
    """Verify tool functions return expected output strings."""
    assert execute_transfer.invoke({"amount": 100.0, "currency": "USD"}) == "Transferred 100.0 USD"
    assert read_database.invoke({"table": "users"}) == "Read from users"


def test_build_agent_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify agent builds successfully with a valid API key configured."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-1234567890abcdef")
    agent = build_agent()
    assert isinstance(agent, CompiledStateGraph)
    assert "model" in agent.nodes
    assert "tools" in agent.nodes

    # Verify NTI Callback Handler setup
    nti_handler = get_nti_callback_handler()
    assert nti_handler.agent_id == "finance_agent"


def test_build_agent_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify ValueError is raised when OPENAI_API_KEY is missing or blank."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY is not configured properly"):
        build_agent()


def test_build_agent_placeholder_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify ValueError is raised when default placeholder API key is used."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-your-key-here")
    with pytest.raises(ValueError, match="OPENAI_API_KEY is not configured properly"):
        build_agent()
