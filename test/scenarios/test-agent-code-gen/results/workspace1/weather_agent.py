"""
Weather Agent

A simple weather agent that can retrieve weather information for cities
using the Microsoft Agent Framework and GitHub models.
"""

import os
import asyncio
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI

from weather_tools import get_weather_real, get_weather_simulated, get_weather_forecast


class WeatherAgent:
    """
    A weather agent that can provide weather information for any city.
    """
    
    def __init__(self, use_real_weather=True):
        """
        Initialize the Weather Agent.
        
        Args:
            use_real_weather: If True, use real weather API. If False, use simulated data.
        """
        # Load environment variables
        load_dotenv()
        
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.model_id = os.getenv("MODEL_ID", "openai/gpt-4.1-mini")
        self.use_real_weather = use_real_weather
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        # Initialize OpenAI client for GitHub models
        self.openai_client = AsyncOpenAI(
            base_url="https://models.github.ai/inference",
            api_key=self.github_token,
        )
        
        # Initialize chat client
        self.chat_client = OpenAIChatClient(
            async_client=self.openai_client,
            ai_model_id=self.model_id
        )
        
        # Choose weather function based on configuration
        weather_function = get_weather_real if use_real_weather else get_weather_simulated
        
        # Create the agent with weather tools
        self.agent = ChatAgent(
            chat_client=self.chat_client,
            name="WeatherAgent",
            instructions="""You are a helpful weather agent that provides accurate weather information for any city or location.

When users ask about weather, you should:
1. Use the available weather tools to get current weather information
2. Provide clear, helpful responses about temperature, conditions, and other relevant details
3. If asked about forecasts, use the forecast tool
4. Be friendly and conversational in your responses
5. If weather data is unavailable for a location, suggest similar nearby cities or ask for clarification

Always format weather information in a clear, easy-to-read manner.""",
            tools=[weather_function, get_weather_forecast],
        )
    
    async def get_weather(self, location: str) -> str:
        """
        Get weather information for a specific location.
        
        Args:
            location: The city or location to get weather for.
            
        Returns:
            Weather information as a string.
        """
        query = f"What's the weather like in {location}?"
        result = await self.agent.run(query)
        return result.text
    
    async def chat(self, message: str, thread=None) -> str:
        """
        Have a conversation with the weather agent.
        
        Args:
            message: The user's message.
            thread: Optional thread for maintaining conversation context.
            
        Returns:
            The agent's response.
        """
        result = await self.agent.run(message, thread=thread)
        return result.text
    
    def get_new_thread(self):
        """
        Create a new conversation thread for maintaining context.
        
        Returns:
            A new thread object.
        """
        return self.agent.get_new_thread()


async def main():
    """
    Example usage of the Weather Agent.
    """
    print("🌤️ Weather Agent Starting...\n")
    
    try:
        # Create weather agent (set use_real_weather=False for simulated data)
        agent = WeatherAgent(use_real_weather=False)  # Change to True for real weather
        
        # Create a conversation thread
        thread = agent.get_new_thread()
        
        # Example weather queries
        test_queries = [
            "What's the weather like in London?",
            "How's the weather in Tokyo today?",
            "Can you give me a 5-day forecast for New York?",
            "What about the weather in a small town like Palo Alto?",
        ]
        
        for query in test_queries:
            print(f"User: {query}")
            response = await agent.chat(query, thread=thread)
            print(f"Agent: {response}\n")
            print("-" * 50 + "\n")
        
        # Interactive mode
        print("🌤️ Weather Agent is ready! Type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye! 👋")
                    break
                
                if user_input:
                    response = await agent.chat(user_input, thread=thread)
                    print(f"Weather Agent: {response}\n")
                    
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {e}\n")
    
    except Exception as e:
        print(f"Failed to initialize Weather Agent: {e}")
        print("\nMake sure you have:")
        print("1. Set your GITHUB_TOKEN in the .env file")
        print("2. Installed the required dependencies")
        print("3. (Optional) Set your WEATHER_API_KEY for real weather data")


if __name__ == "__main__":
    asyncio.run(main())