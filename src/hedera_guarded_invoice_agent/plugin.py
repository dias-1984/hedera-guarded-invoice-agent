from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Any

from .hedera_adapter import ReturnBytesHederaAdapter
from .models import ApprovalPackage, Invoice
from .policy import InvoicePolicy


class InvoiceApprovalPlugin:
    """Agent-facing invoice approval plugin.

    The public methods are intentionally deterministic so they can be exposed as
    tools in LangChain, ADK, MCP, or Hedera Agent Kit plugin wrappers.
    """

    def __init__(self, policy: InvoicePolicy, hedera: ReturnBytesHederaAdapter):
        self.policy = policy
        self.hedera = hedera

    def tool_schema(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "evaluate_invoice",
                "description": "Validate an invoice and return policy/risk decision.",
                "input": "invoice JSON object",
            },
            {
                "name": "prepare_invoice_transfer",
                "description": "Prepare Hedera transaction bytes only if policy allows; never signs or executes.",
                "input": "invoice JSON object",
            },
        ]

    def evaluate_invoice(self, invoice_payload: dict[str, Any]) -> dict[str, Any]:
        invoice = Invoice.from_dict(invoice_payload)
        decision = self.policy.evaluate(invoice)
        return {"invoice": asdict(invoice), "decision": asdict(decision)}

    def prepare_invoice_transfer(self, invoice_payload: dict[str, Any]) -> dict[str, Any]:
        package = self.build_approval_package(invoice_payload)
        return {
            "invoice": asdict(package.invoice),
            "decision": asdict(package.decision),
            "prepared_transfer": asdict(package.prepared_transfer) if package.prepared_transfer else None,
            "approval_message": package.approval_message,
        }

    def build_approval_package(self, invoice_payload: dict[str, Any]) -> ApprovalPackage:
        invoice = Invoice.from_dict(invoice_payload)
        decision = self.policy.evaluate(invoice)
        prepared = None
        if decision.allowed:
            prepared = self.hedera.prepare_transfer(invoice, self.idempotency_key(invoice))

        approval_message = self._approval_message(invoice, decision, prepared is not None)
        return ApprovalPackage(
            invoice=invoice,
            decision=decision,
            prepared_transfer=prepared,
            approval_message=approval_message,
        )

    def idempotency_key(self, invoice: Invoice) -> str:
        raw = f"{invoice.invoice_id}|{invoice.vendor_id}|{invoice.amount}|{invoice.currency}|{invoice.hedera_account}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

    def _approval_message(self, invoice: Invoice, decision, prepared: bool) -> str:
        if not decision.allowed:
            return f"Rejected {invoice.invoice_id}: {', '.join(decision.reasons)}"
        if decision.requires_human_approval:
            return f"Prepared {invoice.invoice_id}; human approval required before signing or execution."
        if prepared:
            return f"Prepared {invoice.invoice_id}; policy permits preparation, signing still remains manual."
        return f"No transfer prepared for {invoice.invoice_id}."
