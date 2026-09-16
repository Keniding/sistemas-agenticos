from typing import Never

from agent_framework import Executor, handler, WorkflowContext, executor, WorkflowBuilder
import asyncio
from base import client

class UpperCase(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert input to uppercase and forward to the next node."""
        await ctx.send_message(text.upper())

@executor(id="reverse_text")
async def reverse_text(text: str, ctx: WorkflowContext[Never, str]) -> None:
    """Reverse the string and yield the final workflow output."""
    await ctx.yield_output(text[::-1])

def create_workflow():
    upper = UpperCase(id="upper_case")
    return WorkflowBuilder(
        start_executor=upper
    ).add_edge(
        upper, reverse_text
    ).build()

workflow = create_workflow()

async def main():
    events = await workflow.run("hello world")
    print(f"Output: {events.get_outputs()}")
    print(f"Final state: {events.get_final_state()}")

if __name__ == "__main__":
    asyncio.run(main())
