#!/usr/bin/env python3
"""
AI-Powered Cooking Plan Agent
Main console application entry point.
"""

import os
import sys
import asyncio
from typing import Dict, Any, List
from dotenv import load_dotenv

from openai import AsyncOpenAI
from agents import set_tracing_disabled, set_default_openai_client, set_default_openai_api, Runner
from cooking_agents import get_main_agent
from utils import console_formatter
from models import UserPreferences, DietaryRestriction


def setup_openai_client():
    """Set up the OpenAI client with GitHub Models or OpenAI API."""
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if github_token:
        # Use GitHub Models (free tier)
        console_formatter.print_info("🚀 Using GitHub Models API (GPT-4.1)")
        client = AsyncOpenAI(
            base_url="https://models.github.ai/inference/",
            api_key=github_token,
        )
        set_default_openai_client(client=client, use_for_tracing=False)
        set_default_openai_api("chat_completions")
        set_tracing_disabled(True)
        return "gpt-4.1"  # GitHub Models model
    elif openai_api_key:
        # Use OpenAI directly
        console_formatter.print_info("🤖 Using OpenAI API")
        client = AsyncOpenAI(api_key=openai_api_key)
        set_default_openai_client(client=client, use_for_tracing=False)
        set_tracing_disabled(True)
        return "gpt-4.1"  # OpenAI model
    else:
        console_formatter.print_error("No API key found! Please set GITHUB_TOKEN or OPENAI_API_KEY in .env file")
        sys.exit(1)


def get_user_preferences() -> UserPreferences:
    """Get user preferences for cooking."""
    console_formatter.print_section_header("Tell me about your cooking preferences", "👨‍🍳")
    
    # Get dietary restrictions
    console_formatter.console.print("[bold]Dietary Restrictions (optional):[/bold]")
    console_formatter.console.print("Available options: vegetarian, vegan, gluten_free, dairy_free, nut_free, keto, paleo")
    dietary_input = console_formatter.prompt_user_input(
        "Enter dietary restrictions (comma-separated)", 
        default=""
    )
    
    dietary_restrictions = []
    if dietary_input.strip():
        for restriction in dietary_input.split(","):
            restriction = restriction.strip().lower()
            try:
                dietary_restrictions.append(DietaryRestriction(restriction))
            except ValueError:
                console_formatter.print_warning(f"Unknown dietary restriction: {restriction}")
    
    # Get other preferences
    favorite_cuisines = []
    cuisine_input = console_formatter.prompt_user_input(
        "Favorite cuisines (comma-separated)", 
        default="american, italian"
    )
    if cuisine_input.strip():
        favorite_cuisines = [c.strip() for c in cuisine_input.split(",")]
    
    skill_level = console_formatter.prompt_user_input(
        "Cooking skill level (beginner/intermediate/advanced)", 
        default="intermediate"
    )
    
    available_time = console_formatter.prompt_user_input(
        "Available cooking time (minutes)", 
        default="60"
    )
    
    serving_size = console_formatter.prompt_user_input(
        "Number of servings needed", 
        default="4"
    )
    
    # Get pantry items
    console_formatter.console.print("\n[bold]What do you have in your pantry/fridge?[/bold]")
    console_formatter.console.print("(This helps us identify what you need to buy)")
    pantry_input = console_formatter.prompt_user_input(
        "List available ingredients (comma-separated)", 
        default="salt, pepper, olive oil, onions"
    )
    
    pantry_items = []
    if pantry_input.strip():
        pantry_items = [item.strip() for item in pantry_input.split(",")]
    
    try:
        available_time_int = int(available_time)
        serving_size_int = int(serving_size)
    except ValueError:
        available_time_int = 60
        serving_size_int = 4
        console_formatter.print_warning("Using default values for time and serving size")
    
    preferences = UserPreferences(
        dietary_restrictions=dietary_restrictions,
        favorite_cuisines=favorite_cuisines,
        cooking_skill_level=skill_level,
        available_time_minutes=available_time_int,
        serving_size=serving_size_int,
        pantry_items=[]  # We'll use the string list for the agent
    )
    
    # Store pantry items as strings for agent use
    preferences.pantry_items = pantry_items
    
    return preferences


async def create_cooking_plan(preferences: UserPreferences) -> None:
    """Create a cooking plan using the AI agent."""
    console_formatter.print_section_header("Creating your cooking plan", "🍳")
    
    # Get what the user wants to cook
    dish_request = console_formatter.prompt_user_input(
        "What would you like to cook today?", 
        default="pasta with garlic and herbs"
    )
    
    # Format the cooking request
    cuisine = preferences.favorite_cuisines[0] if preferences.favorite_cuisines else "american"
    dietary_restrictions_str = ", ".join([dr.value for dr in preferences.dietary_restrictions])
    
    cooking_request = f"""
I want to cook: {dish_request}
Cuisine preference: {cuisine}
Serving size: {preferences.serving_size} people
Available cooking time: {preferences.available_time_minutes} minutes
Skill level: {preferences.cooking_skill_level}
Dietary restrictions: {dietary_restrictions_str if dietary_restrictions_str else "none"}
Available pantry items: {", ".join(getattr(preferences, 'pantry_items', []))}

Please create a complete cooking plan including:
1. Generate a detailed recipe for the dish
2. Analyze what ingredients I'm missing from my pantry
3. Find those missing ingredients in the Contoso product catalog
4. Add the best options to my shopping cart
5. Provide a summary of the plan and shopping list

Make this as automated as possible - I want to cook, not spend time shopping around!
"""
    
    console_formatter.print_info("🤖 AI agent is working on your cooking plan...")
    
    try:
        # Get the main agent and run the cooking plan creation
        main_agent = get_main_agent()
        result = await Runner.run(main_agent, cooking_request)
        
        console_formatter.print_section_header("Cooking Plan Complete!", "✅")
        console_formatter.console.print(result.final_output)
        
        # Show final shopping cart
        console_formatter.print_section_header("Your Shopping Cart", "🛒")
        from services import get_contoso_service
        contoso_service = get_contoso_service()
        cart = await contoso_service.get_cart()
        console_formatter.print_shopping_cart(cart)
        
        if cart.items:
            checkout = console_formatter.prompt_confirmation(
                "Would you like to proceed to checkout?"
            )
            if checkout:
                console_formatter.print_success("🎉 Order placed! Your ingredients will be delivered soon.")
                console_formatter.print_info("Happy cooking! 👨‍🍳")
            else:
                console_formatter.print_info("Cart saved for later. You can checkout anytime!")
        
    except Exception as e:
        console_formatter.print_error(f"Failed to create cooking plan: {str(e)}")
        console_formatter.print_info("Please check your API configuration and try again.")


def show_help():
    """Show help information."""
    console_formatter.print_section_header("How to Use", "❓")
    console_formatter.console.print("""
[bold cyan]Setup:[/bold cyan]
1. Copy .env.example to .env
2. Add your GitHub token or OpenAI API key
3. Run: python main.py

[bold cyan]Features:[/bold cyan]
• 🤖 AI-powered recipe generation
• 🔍 Smart pantry analysis  
• 🛒 Automatic shopping cart management
• 📱 Integration with Contoso product catalog
• 🍽️ Customizable dietary restrictions

[bold cyan]Tips:[/bold cyan]
• Be specific about what you want to cook
• List your pantry items accurately for better results
• The AI will automatically find and add missing ingredients to your cart
""")


async def main():
    """Main application entry point."""
    # Load environment variables
    load_dotenv()
    
    console_formatter.print_welcome()
    
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return
    
    # Setup OpenAI client
    model_name = setup_openai_client()
    
    try:
        # Get user preferences
        preferences = get_user_preferences()
        
        console_formatter.console.print()
        console_formatter.print_success("Preferences saved! Let's create your cooking plan.")
        console_formatter.console.print()
        
        # Create cooking plan
        await create_cooking_plan(preferences)
        
    except KeyboardInterrupt:
        console_formatter.console.print("\n[yellow]👋 Thanks for using the AI Cooking Agent! Happy cooking![/yellow]")
    except Exception as e:
        console_formatter.print_error(f"Unexpected error: {str(e)}")
        console_formatter.print_info("Please report this issue if it persists.")


if __name__ == "__main__":
    asyncio.run(main())
