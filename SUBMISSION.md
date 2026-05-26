# Hedera AI Agent Bounty Submission Package

Target bounty: Week 2, Enterprise Agent + Plugin.

Prize: `$750 in HBAR`.

Deadline: Sunday 23:59 UTC for the current week.

Submission form: https://ai-bounties.hedera.com/

## Form Fields

Project name:

`Hedera Guarded Invoice Agent`

Your name:

`Dias / TARS`

First name:

`NEEDS DIAS`

Last name:

`NEEDS DIAS`

Country of residence:

`NEEDS DIAS`

Email address:

`NEEDS DIAS`

Other contact:

`NEEDS DIAS`

Bounty:

`Week 2: Enterprise Agent + Plugin`

Project description:

`A policy-constrained invoice-payment agent that validates enterprise invoices, enforces vendor and amount guardrails, and prepares Hedera transaction bytes only after deterministic risk checks.`

Project summary:

`Hedera Guarded Invoice Agent demonstrates a safe enterprise payment workflow for AI agents. A finance operator passes an invoice into an agent-facing plugin. The plugin validates the invoice, checks vendor allowlists, amount limits, currency policy, idempotency, and approval thresholds, then either rejects the request or prepares a human-approval package.`

`The project is designed around Hedera Agent Kit RETURN_BYTES mode: transaction preparation is separated from signing and execution, so the agent can help with commercial workflows without gaining unilateral control over funds. The included mock return-bytes adapter makes the demo deterministic and safe without credentials; the README documents the path to wire it to Hedera Agent Kit testnet credentials.`

`The demo shows two paths: a valid low-risk invoice that produces deterministic testnet-style transaction bytes and an unsafe invoice that is rejected without creating any transfer object. This matches enterprise requirements for auditability, consent, and financial risk controls.`

GitHub repository URL:

`NEEDS PUBLIC REPO URL`

Demo or social-media URL:

`NEEDS DEMO URL OR X/VIDEO URL`

Wallet address:

`NEEDS DIAS HEDERA 0.0.x OR EVM ADDRESS`

Implementation details:

`The project exposes an InvoiceApprovalPlugin with deterministic tools: evaluate_invoice and prepare_invoice_transfer. The plugin composes typed invoice parsing, an InvoicePolicy risk engine, and a ReturnBytesHederaAdapter boundary. The current demo uses MockReturnBytesHederaAdapter to avoid private keys and real transactions while preserving the same interface expected from Hedera Agent Kit AgentMode.RETURN_BYTES.`

`The architecture intentionally keeps signing and execution outside the agent. An allowed invoice produces an approval package containing the invoice, policy decision, idempotency key, and transaction bytes. Rejected invoices never produce a transfer object. Tests cover allowlisted invoices, unknown vendors, amount-limit rejection, return-bytes preparation, and rejection without transfer preparation.`

`The next integration step is to replace MockReturnBytesHederaAdapter with a Hedera Agent Kit adapter configured in RETURN_BYTES mode against a testnet account, keeping all human approval boundaries intact.`

Feedback link:

`NEEDS PUBLIC GITHUB ISSUE URL AFTER POSTING FEEDBACK_DRAFT.md`

## Submission Blockers

- Public GitHub repo is required.
- Demo or public social/video URL is required.
- Wallet address is required for payout.
- Real name, country, email are required for private payout records.
- Feedback link on a Hedera tool is required.
- Current code uses a mock return-bytes adapter; a stronger submission should add a real Hedera Agent Kit adapter or clearly document the adapter boundary.

## Recommended Action

1. Dias approves public repo creation.
2. Publish this folder as a GitHub repo.
3. Add a short screen recording of:
   - valid invoice preparation,
   - rejected unsafe invoice,
   - tests passing.
4. Post `FEEDBACK_DRAFT.md` as a GitHub issue against `hashgraph/hedera-agent-kit-py` or another accepted Hedera tool repo.
5. Submit the form.
