import asyncio
from agent_framework import Agent
from agent_framework_foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

client = FoundryChatClient(
    project_endpoint="https://kenidinghk-5470-resource.services.ai.azure.com",
    model="gpt-5.4-nano",
    credential=DefaultAzureCredential()
)

agent = Agent(
    client=client,
    name="AsistentePreguntas",
    instructions="You are a friendly assistant. Keep your answers brief.",
)

async def main():
    result = await agent.run("What is the capital of France?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())