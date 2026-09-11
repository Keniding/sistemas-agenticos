from agent_framework_foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

client = FoundryChatClient(
    project_endpoint="https://kenidinghk-5470-resource.services.ai.azure.com",
    model="gpt-5.4-nano",
    credential=DefaultAzureCredential()
)