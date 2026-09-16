import asyncio

from agent_framework_orchestrations import SequentialBuilder
from agent_framework import Agent, tool

from base import client


@tool(approval_mode="always_require")
def execute_database_query(query: str) -> str:
    return f"Query executed successfully: {query}"


database_agent = Agent(
    client=client,
    name="DatabaseAgent",
    instructions="You are a database assistant.",
    tools=[execute_database_query],
)

workflow = SequentialBuilder(participants=[database_agent]).build()


def _describe_approval(data):
    for path in ("function_call.name", "function_call.function.name", "tool_call.name", "call.name"):
        obj = data
        try:
            for part in path.split("."):
                obj = getattr(obj, part)
            if obj:
                return obj
        except AttributeError:
            continue
    return vars(data) if hasattr(data, "__dict__") else repr(data)


async def process_event_stream(stream):
    responses = {}
    async for event in stream:
        etype = getattr(event, "type", type(event).__name__)
        data = getattr(event, "data", None)

        if etype == "request_info" and getattr(data, "type", None) == "function_approval_request":
            info = _describe_approval(data)
            print(f"[APROBACIÓN REQUERIDA] {info} -> auto-aprobando")
            responses[event.request_id] = data.to_function_approval_response(approved=True)
            continue

        text = getattr(data, "text", None) or getattr(data, "delta", None)
        if text:
            print(text, end="", flush=True)
            continue

    return responses if responses else None

async def main():
    stream = workflow.run("Check the schema and update all pending orders", stream=True)

    pending_responses = await process_event_stream(stream)
    while pending_responses is not None:
        stream = workflow.run(stream=True, responses=pending_responses)
        pending_responses = await process_event_stream(stream)

    print("\n--- Workflow terminado ---")


if __name__ == "__main__":
    asyncio.run(main())