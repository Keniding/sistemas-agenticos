import asyncio
from agent_framework import Agent
from agent_framework_foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential

client = FoundryChatClient(
    project_endpoint="https://kenidinghk-5470-resource.services.ai.azure.com",
    model="gpt-5.4-nano",
    credential=AzureCliCredential()
)

agent = Agent(
    client=client,
    name="GestorDocumentos",
    instructions="You are a friendly assistant. Keep your answers brief.",
)


async def main():
    async with AzureCliCredential():
        result = await agent.run("What is the capital of France?")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())