import asyncio

from agent_framework import AgentResponse
from agent_framework_orchestrations import ConcurrentBuilder

from base import client as chat_client

researcher = chat_client.as_agent(
    instructions=(
        "You're an expert market and product researcher. Given a prompt, provide concise, factual insights,"
        " opportunities, and risks."
    ),
    name="researcher",
)

marketer = chat_client.as_agent(
    instructions=(
        "You're a creative marketing strategist. Craft compelling value propositions and target messaging"
        " aligned to the prompt."
    ),
    name="marketer",
)

legal = chat_client.as_agent(
    instructions=(
        "You're a cautious legal/compliance reviewer. Highlight constraints, disclaimers, and policy concerns"
        " based on the prompt."
    ),
    name="legal",
)

workflow_concurrent = ConcurrentBuilder(
    participants=[researcher, marketer, legal]
).build()

async def main():
    events = await workflow_concurrent.run("We are launching a new budget-friendly electric bike for urban commuters.")
    outputs = events.get_outputs()

    if outputs:
        print("===== Final Aggregated Results =====")
        final: AgentResponse = outputs[0]
        for msg in final.messages:
            name = msg.author_name or "assistant"
            print(f"{'-' * 60}\n\n[{name}]:\n{msg.text}")

if __name__ == "__main__":
    asyncio.run(main())