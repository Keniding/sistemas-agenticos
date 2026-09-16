import asyncio

from base import client
from agent_framework import Agent

agent = Agent(
    client=client,
    name="AsistentePreguntas",
    instructions="You are a friendly assistant. Keep your answers brief.",
)

PREGUNTA1 = "My name is Henry and I love hiking."
PREGUNTA2 = "What do you remember about me?"

async def main():
    session = agent.create_session()
    print("Agent (streaming): ", end="", flush=True)

    async for chunk in agent.run(PREGUNTA1, stream=True, session=session):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print("\n")

    async for chunk in agent.run(PREGUNTA2, stream=True, session=session):
        if chunk.text:
            print(chunk.text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())