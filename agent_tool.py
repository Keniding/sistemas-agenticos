import asyncio
from random import randint
from typing import Annotated

from pydantic import Field

from base import client
from agent_framework import Agent
from agent_framework import tool

@tool(approval_mode="never_require")
def get_weather(
        location: Annotated[str, Field(description="The location for which to retrieve the weather.")]
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

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