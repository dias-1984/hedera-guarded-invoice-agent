"""Reference integration shape for Hedera Agent Kit RETURN_BYTES mode.

This file is intentionally not used by the default tests because it requires
real Hedera testnet credentials and an LLM provider key. It shows how the
project's human-in-the-loop policy boundary maps to Hedera Agent Kit's
return-bytes execution mode.

Run only against testnet credentials:

    pip install hedera-agent-kit langchain langchain-openai python-dotenv
    ACCOUNT_ID=0.0.x PRIVATE_KEY=... OPENAI_API_KEY=... python examples/hedera_agentkit_return_bytes_langchain.py
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from hedera_agent_kit.langchain.toolkit import HederaLangchainToolkit
from hedera_agent_kit.plugins import core_account_plugin, core_account_query_plugin
from hedera_agent_kit.shared.configuration import AgentMode, Configuration, Context
from hiero_sdk_python import AccountId, Client, Network, PrivateKey
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver


async def main() -> None:
    load_dotenv()

    account_id_raw = os.environ["ACCOUNT_ID"]
    private_key_raw = os.environ["PRIVATE_KEY"]

    account_id = AccountId.from_string(account_id_raw)
    private_key = PrivateKey.from_string(private_key_raw)
    client = Client(Network(network="testnet"))
    client.set_operator(account_id, private_key)

    toolkit = HederaLangchainToolkit(
        client=client,
        configuration=Configuration(
            tools=[],
            plugins=[core_account_plugin, core_account_query_plugin],
            context=Context(mode=AgentMode.RETURN_BYTES, account_id=str(account_id)),
        ),
    )

    agent = create_agent(
        model=ChatOpenAI(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"]),
        tools=toolkit.get_tools(),
        checkpointer=MemorySaver(),
        system_prompt=(
            "You prepare Hedera testnet transaction bytes for human review. "
            "Never claim that a transfer has been signed or executed."
        ),
    )

    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Prepare return bytes for a 1 tinybar transfer to 0.0.12345 with memo invoice-demo.",
                }
            ]
        },
        config={"configurable": {"thread_id": "return-bytes-demo"}},
    )

    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
