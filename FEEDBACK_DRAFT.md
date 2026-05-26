# Feedback: clarify RETURN_BYTES examples for enterprise payment guardrails

While building a guarded invoice-payment agent for the Hedera AI Agent Bounty, I found the `AgentMode.RETURN_BYTES` pattern useful for enterprise workflows where agents should prepare transaction-ready output but never sign or execute without human approval.

One improvement that would help builders:

- Add a minimal Python example showing an enterprise payment tool/plugin in `RETURN_BYTES` mode.
- Show how to return an approval package containing policy decision, transaction bytes, idempotency key, and human-readable approval text.
- Show a rejected policy path where no transaction bytes are generated.
- Document the recommended boundary between deterministic policy checks, agent reasoning, transaction-byte preparation, and final human signing.

This would make the safety model clearer for payment, custody, KYC, and asset-tokenization agents where auditability and consent are core requirements.

Related demo pattern:

- Validate invoice data.
- Enforce vendor allowlist and amount thresholds.
- Prepare transaction bytes only when policy allows.
- Keep signing outside the agent.
