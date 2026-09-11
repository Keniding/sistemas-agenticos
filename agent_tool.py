import asyncio

from base import client
from agent_framework import Agent

from clima import get_weather

agent = Agent(
    client=client,
    name="AsistentePreguntas",
    instructions="You are a helpful weather agent. Use the tool to answer questions.",
    tools=[get_weather]
)

PREGUNTA = "What is the weather like in New York?"

async def main():
    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run(PREGUNTA, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())