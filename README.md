# Hedera Guarded Invoice Agent

Prototype for the Hedera AI Agent Bounty: an enterprise invoice-payment agent
that refuses unsafe autonomous fund movement and emits a human-approval package
instead.

The core idea is simple: a finance operator gives the agent an invoice, vendor
record, and policy limits. The agent validates the request, produces a risk
decision, and prepares Hedera transaction bytes only when the payment is within
policy. Signing and execution remain outside the agent.

## Why This Fits The Bounty

- Enterprise workflow: invoice approval and payment operations.
- Agent + plugin shape: `InvoiceApprovalPlugin` exposes deterministic tools for
  invoice validation, policy checks, and transaction preparation.
- Hedera alignment: adapter is designed for Hedera Agent Kit
  `AgentMode.RETURN_BYTES`, so a demo can show transaction preparation without
  autonomous signing.
- Safety: no agent path can drain funds. All transfers require explicit
  human approval after policy evaluation.

## Safety Model

- No private keys in code.
- No autonomous mainnet execution.
- Per-invoice idempotency key.
- Vendor allowlist.
- Amount and currency limits.
- Required approval for anything above policy threshold.
- Full audit package for every decision.

## Quick Start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python -m hedera_guarded_invoice_agent.cli examples/invoice_valid.json
python -m unittest discover -v
```

The default adapter is a deterministic mock. It does not call Hedera and does
not create or sign transactions.

## Real Hedera Integration Path

To turn this into a live bounty demo:

1. Install `hedera-agent-kit` in a local virtualenv.
2. Configure a Hedera testnet account in `.env`.
3. Replace `MockReturnBytesHederaAdapter` with an adapter that calls Hedera
   Agent Kit in `AgentMode.RETURN_BYTES`.
4. Keep signing in a separate human approval step.
5. Record a demo showing:
   - rejected unsafe invoice,
   - approved policy-compliant invoice,
   - returned transaction bytes,
   - manual approval boundary.

## Bounty Submission Package

- `SUBMISSION.md`: prefilled Hedera bounty form fields and blockers.
- `FEEDBACK_DRAFT.md`: required Hedera tool feedback draft.
- `DEMO_SCRIPT.md`: short recording script.

## Files

- `src/hedera_guarded_invoice_agent/models.py`: typed domain objects.
- `src/hedera_guarded_invoice_agent/policy.py`: deterministic risk checks.
- `src/hedera_guarded_invoice_agent/hedera_adapter.py`: return-bytes adapter boundary.
- `src/hedera_guarded_invoice_agent/plugin.py`: agent-facing plugin tools.
- `src/hedera_guarded_invoice_agent/cli.py`: local demo entrypoint.
