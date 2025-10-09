    # Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from datetime import datetime, timezone
from random import randint
from typing import Annotated

from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from pydantic import Field


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


def get_time() -> str:
    """Get the current UTC time."""
    current_time = datetime.now(timezone.utc)
    return f"The current UTC time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}."


async def tools_on_agent_level() -> None:
    """Example showing tools defined when creating the agent."""
    print("=== Tools Defined on Agent Level ===")

    # Load environment variables from .env file
    load_dotenv()

    # Get Azure OpenAI configuration from environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not endpoint or not deployment_name:
        raise ValueError("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME in your .env file")

    # Tools are provided when creating the agent
    # The agent can use these tools for any query during its lifetime
    # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
    # authentication option.
    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(
            credential=AzureCliCredential(),
            endpoint=endpoint,
            deployment_name=deployment_name,
        ),
        instructions="You are a helpful assistant that can provide weather and time information.",
        tools=[get_weather, get_time],  # Tools defined at agent creation
        name="Weather and Time Agent",
    )

    # First query - agent can use weather tool
    query1 = "What's the weather like in New York?"
    print(f"User: {query1}")
    result1 = await agent.run(query1)
    print(f"Agent: {result1}\n")

    # Second query - agent can use time tool
    query2 = "What's the current UTC time?"
    print(f"User: {query2}")
    result2 = await agent.run(query2)
    print(f"Agent: {result2}\n")

    # Third query - agent can use both tools if needed
    query3 = "What's the weather in London and what's the current UTC time?"
    print(f"User: {query3}")
    result3 = await agent.run(query3)
    print(f"Agent: {result3}\n")


async def main() -> None:
    print("=== Azure Chat Client Agent with Function Tools Examples ===\n")

    await tools_on_agent_level()


if __name__ == "__main__":
    asyncio.run(main())