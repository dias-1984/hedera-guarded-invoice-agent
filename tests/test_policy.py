from decimal import Decimal
import unittest

from hedera_guarded_invoice_agent.models import Invoice
from hedera_guarded_invoice_agent.policy import InvoicePolicy


class TestInvoicePolicy(unittest.TestCase):
    def test_allowlisted_small_invoice_is_allowed(self):
        invoice = Invoice.from_dict(
            {
                "invoice_id": "INV-1",
                "vendor_id": "vendor-ace-cloud",
                "vendor_name": "Ace",
                "amount": "42.50",
                "currency": "USD",
                "memo": "services",
                "hedera_account": "0.0.123",
                "due_date": "2026-05-31",
            }
        )

        decision = InvoicePolicy().evaluate(invoice)

        self.assertTrue(decision.allowed)
        self.assertFalse(decision.requires_human_approval)
        self.assertEqual(decision.risk_score, 0)

    def test_unknown_vendor_is_rejected(self):
        invoice = Invoice.from_dict(
            {
                "invoice_id": "INV-2",
                "vendor_id": "unknown",
                "vendor_name": "Unknown",
                "amount": "42.50",
                "currency": "USD",
                "memo": "services",
                "hedera_account": "0.0.123",
                "due_date": "2026-05-31",
            }
        )

        decision = InvoicePolicy().evaluate(invoice)

        self.assertFalse(decision.allowed)
        self.assertTrue(decision.requires_human_approval)
        self.assertIn("vendor_not_allowlisted", decision.reasons)

    def test_large_invoice_is_rejected_above_prepare_limit(self):
        invoice = Invoice.from_dict(
            {
                "invoice_id": "INV-3",
                "vendor_id": "vendor-ace-cloud",
                "vendor_name": "Ace",
                "amount": "251.00",
                "currency": "USD",
                "memo": "services",
                "hedera_account": "0.0.123",
                "due_date": "2026-05-31",
            }
        )

        policy = InvoicePolicy(max_prepare_amount=Decimal("250.00"))
        decision = policy.evaluate(invoice)

        self.assertFalse(decision.allowed)
        self.assertIn("amount_above_prepare_limit", decision.reasons)


if __name__ == "__main__":
    unittest.main()
