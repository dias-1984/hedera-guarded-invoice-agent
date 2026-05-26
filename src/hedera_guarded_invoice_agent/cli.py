from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

from .hedera_adapter import MockReturnBytesHederaAdapter
from .plugin import InvoiceApprovalPlugin
from .policy import InvoicePolicy


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def build_plugin() -> InvoiceApprovalPlugin:
    return InvoiceApprovalPlugin(
        policy=InvoicePolicy(),
        hedera=MockReturnBytesHederaAdapter(network="testnet"),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("invoice", help="Path to invoice JSON")
    args = parser.parse_args(argv)

    invoice = json.loads(Path(args.invoice).read_text(encoding="utf-8"))
    result = build_plugin().prepare_invoice_transfer(invoice)
    print(json.dumps(result, indent=2, cls=DecimalEncoder))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
