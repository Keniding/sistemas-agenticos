from typing import Never

from agent_framework_orchestrations import SequentialBuilder
from agent_framework import AgentResponse, Executor, handler, AgentExecutorResponse, WorkflowContext, Message
from base import client

import asyncio

class Summarizer(Executor):
    """Terminator custom executor: consumes full conversation and yields a summary as the workflow's final answer."""

    @handler
    async def summarize(
            self,
            agent_response: AgentExecutorResponse,
            ctx: WorkflowContext[Never, AgentResponse]
    ) -> None:
        if not agent_response.full_conversation:
            await ctx.yield_output(
                AgentResponse(
                    messages=[
                        Message(
                            "assistant",
                            ["No conversation to summarize."]
                        )
                    ]
                )
            )
            return

        users = sum(1 for m in agent_response.full_conversation if m.role == "user")
        assistants = sum(1 for m in agent_response.full_conversation if m.role == "assistant")
        summary = Message("assistant", [f"Summary -> users:{users} assistants:{assistants}"])
        await ctx.yield_output(AgentResponse(messages=[summary]))

content = client.as_agent(
    instructions="Produce a concise paragraph answering the user's request.",
    name="content",
)

summarize = Summarizer(id="summarizer")

workflow_sequential = SequentialBuilder(
    participants=[content, summarize],
    chain_only_agent_responses=True
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
