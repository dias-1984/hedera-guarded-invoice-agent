from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any


class InvoiceValidationError(ValueError):
    pass


@dataclass(frozen=True)
class Invoice:
    invoice_id: str
    vendor_id: str
    vendor_name: str
    amount: Decimal
    currency: str
    memo: str
    hedera_account: str
    due_date: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Invoice":
        required = [
            "invoice_id",
            "vendor_id",
            "vendor_name",
            "amount",
            "currency",
            "memo",
            "hedera_account",
            "due_date",
        ]
        missing = [key for key in required if not data.get(key)]
        if missing:
            raise InvoiceValidationError(f"Missing invoice fields: {', '.join(missing)}")
        try:
            amount = Decimal(str(data["amount"]))
        except InvalidOperation as exc:
            raise InvoiceValidationError("Invalid invoice amount") from exc
        if amount <= 0:
            raise InvoiceValidationError("Invoice amount must be positive")
        currency = str(data["currency"]).upper()
        if len(currency) not in {3, 4, 5}:
            raise InvoiceValidationError("Currency code looks invalid")
        try:
            dt.date.fromisoformat(str(data["due_date"]))
        except ValueError as exc:
            raise InvoiceValidationError("due_date must be YYYY-MM-DD") from exc
        account = str(data["hedera_account"])
        if not account.startswith("0.0."):
            raise InvoiceValidationError("hedera_account must look like 0.0.x")
        return cls(
            invoice_id=str(data["invoice_id"]),
            vendor_id=str(data["vendor_id"]),
            vendor_name=str(data["vendor_name"]),
            amount=amount,
            currency=currency,
            memo=str(data["memo"]),
            hedera_account=account,
            due_date=str(data["due_date"]),
        )


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_human_approval: bool
    reasons: tuple[str, ...]
    risk_score: int


@dataclass(frozen=True)
class PreparedTransfer:
    network: str
    to_account: str
    amount: Decimal
    currency: str
    memo: str
    transaction_bytes: str
    idempotency_key: str


@dataclass(frozen=True)
class ApprovalPackage:
    invoice: Invoice
    decision: PolicyDecision
    prepared_transfer: PreparedTransfer | None
    approval_message: str
