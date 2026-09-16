import asyncio
from typing import Annotated

from agent_framework import tool
from agent_framework_orchestrations import HandoffBuilder, HandoffAgentUserRequest

from base import client as chat_client

@tool
def process_refund(order_number: Annotated[str, "Order number to process refund for"]) -> str:
    """Simulated function to process a refund for a given order number."""
    return f"Refund processed successfully for order {order_number}."

@tool
def check_order_status(order_number: Annotated[str, "Order number to check status for"]) -> str:
    """Simulated function to check the status of a given order number."""
    return f"Order {order_number} is currently being processed and will ship in 2 business days."

@tool
def process_return(order_number: Annotated[str, "Order number to process return for"]) -> str:
    """Simulated function to process a return for a given order number."""
    return f"Return initiated successfully for order {order_number}. You will receive return instructions via email."

triage_agent = chat_client.as_agent(
    instructions=(
        "You are frontline support triage. Route customer issues to the appropriate specialist agents "
        "based on the problem described."
    ),
    description="Triage agent that handles general inquiries.",
    name="triage_agent",
    require_per_service_call_history_persistence=True,
)

refund_agent = chat_client.as_agent(
    instructions="You process refund requests.",
    description="Agent that handles refund requests.",
    name="refund_agent",
    tools=[process_refund],
    require_per_service_call_history_persistence=True,
)

order_agent = chat_client.as_agent(
    instructions="You handle order and shipping inquiries.",
    description="Agent that handles order tracking and shipping issues.",
    name="order_agent",
    tools=[check_order_status],
    require_per_service_call_history_persistence=True,
)

return_agent = chat_client.as_agent(
    instructions="You manage product return requests.",
    description="Agent that handles return processing.",
    name="return_agent",
    tools=[process_return],
    require_per_service_call_history_persistence=True,
)

workflow_handoff = (
    HandoffBuilder(
        name="customer_support_handoff",
        participants=[triage_agent, refund_agent, order_agent, return_agent],
        termination_condition=lambda conversation: len(conversation) > 0 and "welcome" in conversation[-1].text.lower(),
    )
    .with_start_agent(triage_agent)
    .build()
)


def collect_pending_requests(events):
    pending = []
    for event in events:
        if event.type == "request_info" and isinstance(event.data, HandoffAgentUserRequest):
            pending.append(event)
            request_data = event.data
            print(f"Agent {event.executor_id} is awaiting your input")
            for msg in request_data.agent_response.messages[-3:]:
                print(f"{msg.author_name}: {msg.text}")
    return pending


async def main():
    # Start workflow with initial user message
    events = [event async for event in workflow_handoff.run("I need help with my order", stream=True)]
    pending_requests = collect_pending_requests(events)

    # Interactive loop: respond to requests
    while pending_requests:
        user_input = input("You: ")

        responses = {req.request_id: HandoffAgentUserRequest.create_response(user_input) for req in pending_requests}
        events = [event async for event in workflow_handoff.run(responses=responses, stream=True)]
        pending_requests = collect_pending_requests(events)


if __name__ == "__main__":
    asyncio.run(main())