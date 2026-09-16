from agent_framework import Agent, Executor, handler, WorkflowContext, executor, WorkflowBuilder
import asyncio
from base import client

agent = Agent(
    client=client,
    name="AsistentePreguntas",
    instructions="Recibes un texto ya transformado. Responde en una frase sin alterar la posición de las palabras."
)

class UpperCase(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert input to uppercase and forward to the next node."""
        out =text.upper()
        print(out)
        await ctx.send_message(out)

@executor(id="reverse_text")
async def reverse_text(text: str, ctx: WorkflowContext[str]) -> None:
    """Reverse the string and forward it to the agent node."""
    out = text[::-1]
    print(out)
    await ctx.send_message(out)

def create_workflow():
    upper = UpperCase(id="upper_case")
    return WorkflowBuilder(
        start_executor=upper
    ).add_edge(
        upper, reverse_text
    ).add_edge(
        reverse_text, agent
    ).build()

workflow = create_workflow()

async def main():
    events = await workflow.run("hello world")
    for out in events.get_outputs():
        text = getattr(out, "text", None) or str(out)
        print(f"Output: {text}")
    print(f"Final state: {events.get_final_state()}")

if __name__ == "__main__":
    asyncio.run(main())