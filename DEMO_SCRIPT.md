# Demo Script

## Title

Hedera Guarded Invoice Agent: enterprise invoice payment with human approval

## Setup

```bash
cd /srv/tars/bots/money_sprint_2026-05-25/hedera_guarded_invoice_agent
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Valid Invoice Path

```bash
PYTHONPATH=src python3 -m hedera_guarded_invoice_agent.cli examples/invoice_valid.json
```

Narration:

`This invoice is from an allowlisted vendor and below the policy threshold. The agent validates it, computes a deterministic idempotency key, and prepares return-bytes output. It still does not sign or execute anything.`

Expected result:

- `decision.allowed` is `true`.
- `prepared_transfer` is present.
- `transaction_bytes` is returned.
- Approval message says signing remains manual.

## Rejected Invoice Path

```bash
PYTHONPATH=src python3 -m hedera_guarded_invoice_agent.cli examples/invoice_rejected.json
```

Narration:

`This invoice fails policy because the vendor is not allowlisted and the amount is above the preparation limit. The agent rejects it and no transfer object is created.`

Expected result:

- `decision.allowed` is `false`.
- Reasons include `vendor_not_allowlisted` and `amount_above_prepare_limit`.
- `prepared_transfer` is `null`.

## Closing

`The same boundary can be wired to Hedera Agent Kit RETURN_BYTES mode: the agent prepares transaction bytes after deterministic checks, but the human or host application remains responsible for signing and execution.`
