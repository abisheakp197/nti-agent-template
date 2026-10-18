# Security Policy

## Overview

`nti-agent-template` is designed to demonstrate zero-trust capability enforcement for AI agents built with LangChain, powered by **NTI (Neutral Trust Infrastructure)**.

NTI provides post-quantum cryptographic security and capability-based authorization for tool execution in AI agent workflows.

## Reporting Vulnerabilities

If you discover a security vulnerability in this project or the underlying NTI SDKs (`langchain-nti`, `ube-foundation`), please do not create a public issue.

Instead, report security concerns directly via email or private security disclosure:
- Email: security@ube.foundation (or maintainer contact)
- GitHub Security Advisory: Create a draft advisory in the repository.

Please include:
- A description of the issue and potential impact
- Step-by-step instructions or PoC to reproduce the issue
- Affected version(s) and environment details

We will acknowledge receipt within 24–48 hours and provide updates on resolution.

## NTI Security Model

NTI protects agent tool invocation using five foundational security pillars:

1. **Zero-Trust Capability Enforcement**: Tool execution requires explicit runtime grants (`grant_capability`). Unregistered or ungranted tool invocations are blocked immediately with `PermissionError`.
2. **NIST Post-Quantum Cryptography**: Signatures and keys use Dilithium5 signature schemes and Kyber1024 key encapsulation.
3. **BFT Multi-Agent Consensus**: Distributed validation across participating agent nodes preventing single-node authorization compromise.
4. **Merkle-Chained Audit Trails**: Immutable tamper-evident transaction logs capturing all tool calls and capability evaluations.
5. **P2P Agent Mesh & State Persistence**: Secure peer-to-peer communication and cryptographically anchored state management.

## Best Practices for Deployment

- **API Keys**: Never hardcode API keys or secret tokens in source code. Store credentials in `.env` files or environment variables.
- **Least Privilege**: Only grant the minimum required capabilities (`grant_capability(...)`) necessary for agent operation.
- **Dependency Scanning**: Regularly update dependencies (`ube-foundation`, `langchain`, `langchain-nti`) and scan for security advisories.
