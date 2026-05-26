from __future__ import annotations

import base64
import hashlib
from decimal import Decimal
from typing import Protocol

from .models import Invoice, PreparedTransfer


class ReturnBytesHederaAdapter(Protocol):
    def prepare_transfer(self, invoice: Invoice, idempotency_key: str) -> PreparedTransfer:
        """Prepare transaction bytes without signing or executing them."""


class MockReturnBytesHederaAdapter:
    """Deterministic stand-in for Hedera Agent Kit RETURN_BYTES mode."""

    def __init__(self, network: str = "testnet"):
        self.network = network

    def prepare_transfer(self, invoice: Invoice, idempotency_key: str) -> PreparedTransfer:
        payload = "|".join(
            [
                self.network,
                invoice.invoice_id,
                invoice.hedera_account,
                str(invoice.amount),
                invoice.currency,
                invoice.memo,
                idempotency_key,
            ]
        )
        digest = hashlib.sha256(payload.encode("utf-8")).digest()
        return PreparedTransfer(
            network=self.network,
            to_account=invoice.hedera_account,
            amount=Decimal(invoice.amount),
            currency=invoice.currency,
            memo=invoice.memo,
            transaction_bytes=base64.b64encode(digest).decode("ascii"),
            idempotency_key=idempotency_key,
        )
