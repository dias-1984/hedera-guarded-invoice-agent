import unittest

from hedera_guarded_invoice_agent.hedera_adapter import MockReturnBytesHederaAdapter
from hedera_guarded_invoice_agent.plugin import InvoiceApprovalPlugin
from hedera_guarded_invoice_agent.policy import InvoicePolicy


class TestInvoiceApprovalPlugin(unittest.TestCase):
    def test_prepares_return_bytes_for_allowed_invoice(self):
        plugin = InvoiceApprovalPlugin(InvoicePolicy(), MockReturnBytesHederaAdapter())

        result = plugin.prepare_invoice_transfer(
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

        self.assertTrue(result["decision"]["allowed"])
        self.assertIsNotNone(result["prepared_transfer"])
        self.assertEqual(result["prepared_transfer"]["network"], "testnet")
        self.assertIn("signing still remains manual", result["approval_message"])

    def test_rejected_invoice_never_prepares_transfer(self):
        plugin = InvoiceApprovalPlugin(InvoicePolicy(), MockReturnBytesHederaAdapter())

        result = plugin.prepare_invoice_transfer(
            {
                "invoice_id": "INV-2",
                "vendor_id": "unknown",
                "vendor_name": "Unknown",
                "amount": "5000",
                "currency": "USD",
                "memo": "urgent",
                "hedera_account": "0.0.999",
                "due_date": "2026-05-31",
            }
        )

        self.assertFalse(result["decision"]["allowed"])
        self.assertIsNone(result["prepared_transfer"])
        self.assertIn("Rejected", result["approval_message"])


if __name__ == "__main__":
    unittest.main()
