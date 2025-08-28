#!/usr/bin/env python3
"""
Quick demo of the AI-Powered Cooking Plan Agent
This script demonstrates the agent with pre-configured settings.
"""

import os
import asyncio
from dotenv import load_dotenv

from openai import AsyncOpenAI
from agents import set_default_openai_client, set_default_openai_api, Runner
from cooking_agents import get_main_agent
from utils import console_formatter
from services import get_contoso_service


async def demo_cooking_agent():
    """Run a demonstration of the cooking agent."""
    console_formatter.print_welcome()
    console_formatter.print_section_header("Demo Mode", "🎭")
    console_formatter.print_info("Running with pre-configured settings...")
    
    # Setup demo configuration
    load_dotenv()
    
    # Check for API keys
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY") 
    
    if not github_token and not openai_api_key:
        console_formatter.print_error("No API key found!")
        console_formatter.print_info("Please set GITHUB_TOKEN or OPENAI_API_KEY in your .env file")
        console_formatter.print_info("Copy .env.example to .env and add your keys")
        return
    
    # Setup OpenAI client
    if github_token:
        console_formatter.print_info("🚀 Using GitHub Models API")
        client = AsyncOpenAI(
            base_url="https://models.github.ai/inference/",
            api_key=github_token,
        )
        set_default_openai_client(client=client, use_for_tracing=False)
        set_default_openai_api("chat_completions")
    else:
        console_formatter.print_info("🤖 Using OpenAI API")
        client = AsyncOpenAI(api_key=openai_api_key)
        set_default_openai_client(client=client, use_for_tracing=False)
    
    # Demo cooking request
    cooking_request = """
I want to cook: spaghetti carbonara
Cuisine preference: Italian
Serving size: 4 people
Available cooking time: 45 minutes
Skill level: intermediate
Dietary restrictions: none
Available pantry items: salt, black pepper, olive oil, onions, garlic

Please create a complete cooking plan including:
1. Generate a detailed recipe for spaghetti carbonara
2. Analyze what ingredients I'm missing from my pantry
3. Find those missing ingredients in the Contoso product catalog
4. Add the best options to my shopping cart
5. Provide a summary of the plan and shopping list

Make this automated - find the best products and add them to my cart!
"""
    
    console_formatter.print_section_header("Demo Request", "📝")
    console_formatter.console.print("[dim]Request: Spaghetti Carbonara for 4 people[/dim]")
    console_formatter.console.print("[dim]Available: salt, pepper, olive oil, onions, garlic[/dim]")
    console_formatter.console.print()
    
    try:
        console_formatter.print_info("🤖 AI agent is creating your cooking plan...")
        
        # Get the main agent and run the cooking plan creation
        main_agent = get_main_agent()
        result = await Runner.run(main_agent, cooking_request)
        
        console_formatter.print_section_header("Agent Response", "🤖")
        console_formatter.console.print(result.final_output)
        
        # Show final shopping cart
        console_formatter.print_section_header("Shopping Cart Summary", "🛒")
        contoso_service = get_contoso_service()
        cart = await contoso_service.get_cart()
        console_formatter.print_shopping_cart(cart)
        
        console_formatter.print_section_header("Demo Complete!", "✅")
        console_formatter.print_success("🎉 Demo completed successfully!")
        console_formatter.print_info("Run 'python main.py' for the interactive version")
        
    except Exception as e:
        console_formatter.print_error(f"Demo failed: {str(e)}")
        console_formatter.print_info("Please check your API configuration")


if __name__ == "__main__":
    asyncio.run(demo_cooking_agent())
