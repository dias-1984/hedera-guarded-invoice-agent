from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from .models import Invoice, PolicyDecision


@dataclass(frozen=True)
class InvoicePolicy:
    allowed_vendors: frozenset[str] = field(default_factory=lambda: frozenset({"vendor-ace-cloud"}))
    allowed_currencies: frozenset[str] = field(default_factory=lambda: frozenset({"USD", "USDC", "HBAR"}))
    max_prepare_amount: Decimal = Decimal("250.00")
    approval_threshold: Decimal = Decimal("50.00")

    def evaluate(self, invoice: Invoice) -> PolicyDecision:
        reasons: list[str] = []
        risk_score = 0

        if invoice.vendor_id not in self.allowed_vendors:
            reasons.append("vendor_not_allowlisted")
            risk_score += 60
        if invoice.currency not in self.allowed_currencies:
            reasons.append("currency_not_allowed")
            risk_score += 40
        if invoice.amount > self.max_prepare_amount:
            reasons.append("amount_above_prepare_limit")
            risk_score += 50
        if len(invoice.memo) > 100:
            reasons.append("memo_too_long")
            risk_score += 5

        allowed = not any(reason in reasons for reason in ("vendor_not_allowlisted", "currency_not_allowed", "amount_above_prepare_limit"))
        requires_approval = invoice.amount >= self.approval_threshold or risk_score > 0
        if requires_approval:
            reasons.append("human_approval_required")

        return PolicyDecision(
            allowed=allowed,
            requires_human_approval=requires_approval,
            reasons=tuple(dict.fromkeys(reasons)),
            risk_score=min(risk_score, 100),
        )
