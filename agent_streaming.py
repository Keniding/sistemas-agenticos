import asyncio
from base import client
from agent_framework import Agent

agent = Agent(
    client=client,
    name="AsistentePreguntas",
    instructions="You are a friendly assistant. Keep your answers brief.",
)

async def main():
    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())