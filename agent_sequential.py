from agent_framework_orchestrations import SequentialBuilder
from agent_framework import AgentResponse
from base import client

import asyncio

writer = client.as_agent(
    instructions=(
        "You are a concise copywriter. Provide a single, punchy marketing sentence based on the prompt."
    ),
    name="writer"
)

reviewer = client.as_agent(
    instructions=(
        "You are a thoughtful reviewer. Give brief feedback on the previous assistant message."
    ),
    name="reviewer",
)

workflow_sequential = SequentialBuilder(
    participants=[writer, reviewer]
).build()

async def main():
    events = await workflow_sequential.run("Write a tagline for a budget-friendly eBike.")
    outputs = events.get_outputs()

    if outputs:
        print("===== Final Response =====")
        final: AgentResponse = outputs[0]
        for msg in final.messages:
            name = msg.author_name or "assistant"
            print(f"[{name}]\n{msg.text}")

if __name__ == "__main__":
    asyncio.run(main())
