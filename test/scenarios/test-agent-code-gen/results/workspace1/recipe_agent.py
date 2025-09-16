#!/usr/bin/env python3
"""
Recipe Recommendation Agent

An LLM-based AI agent that recommends recipes based on user-provided ingredients.
Built with Microsoft Agent Framework and GitHub models.
"""

import os
import sys
import asyncio
import argparse
from typing import List, Optional
import logging

import click
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.models import OpenAIChatCompletionClient

from config import config

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

class RecipeAgent:
    """Main Recipe Recommendation Agent class"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.setup_logging()
        self.setup_agents()
    
    def setup_logging(self):
        """Setup logging configuration"""
        level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_agents(self):
        """Initialize the agent with GitHub models"""
        try:
            # Validate GitHub token
            if not config.github_token:
                raise ValueError("GitHub token not found. Please set GITHUB_TOKEN environment variable.")
            
            # Create OpenAI client for GitHub models
            self.model_client = OpenAIChatCompletionClient(
                model=config.default_model,
                base_url=config.base_url,
                api_key=config.github_token,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            
            # Create the recipe recommendation agent
            self.recipe_agent = AssistantAgent(
                name="RecipeChef",
                model_client=self.model_client,
                system_message=config.system_prompt,
                description="A culinary expert that provides recipe recommendations based on available ingredients."
            )
            
            self.logger.info(f"Recipe agent initialized with model: {config.default_model}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {e}")
            raise
    
    def validate_ingredients(self, ingredients: str) -> List[str]:
        """Validate and clean ingredient list"""
        if not ingredients.strip():
            raise ValueError("Please provide at least one ingredient.")
        
        # Split by comma and clean up
        ingredient_list = [
            ingredient.strip() 
            for ingredient in ingredients.split(',') 
            if ingredient.strip()
        ]
        
        if not ingredient_list:
            raise ValueError("Please provide valid ingredients.")
        
        return ingredient_list
    
    def format_user_prompt(self, ingredients: List[str], 
                          dietary_restrictions: Optional[List[str]] = None,
                          cuisine_preference: Optional[str] = None) -> str:
        """Format the user prompt with ingredients and preferences"""
        
        prompt = f"I have these ingredients: {', '.join(ingredients)}."
        
        if dietary_restrictions:
            prompt += f" I have these dietary restrictions: {', '.join(dietary_restrictions)}."
        
        if cuisine_preference:
            prompt += f" I prefer {cuisine_preference} cuisine."
        
        prompt += f" Please suggest {config.max_recipes} recipe recommendations."
        
        return prompt
    
    async def get_recipe_recommendations(self, 
                                       ingredients: List[str],
                                       dietary_restrictions: Optional[List[str]] = None,
                                       cuisine_preference: Optional[str] = None) -> str:
        """Get recipe recommendations from the agent"""
        
        try:
            user_prompt = self.format_user_prompt(ingredients, dietary_restrictions, cuisine_preference)
            
            self.logger.debug(f"Sending prompt: {user_prompt}")
            
            # Create a simple team with just our recipe agent
            team = RoundRobinGroupChat([self.recipe_agent])
            
            # Get response from the agent
            result = await Console(team.run_stream(task=user_prompt))
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting recipe recommendations: {e}")
            return f"Sorry, I encountered an error while generating recipe recommendations: {e}"
    
    def print_welcome(self):
        """Print welcome message"""
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🍳 Recipe Recommendation Agent{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Powered by Microsoft Agent Framework & GitHub Models{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Model: {config.default_model}{Style.RESET_ALL}\n")
    
    async def interactive_mode(self):
        """Run the agent in interactive mode"""
        self.print_welcome()
        
        while True:
            try:
                # Get ingredients from user
                print(f"{Fore.CYAN}What ingredients do you have?{Style.RESET_ALL}")
                print(f"{Fore.WHITE}(Enter comma-separated ingredients, or 'quit' to exit){Style.RESET_ALL}")
                
                ingredients_input = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
                
                if ingredients_input.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.YELLOW}👋 Happy cooking!{Style.RESET_ALL}")
                    break
                
                # Validate ingredients
                ingredients = self.validate_ingredients(ingredients_input)
                
                # Optional: Ask for dietary restrictions
                print(f"\n{Fore.CYAN}Any dietary restrictions? (optional){Style.RESET_ALL}")
                dietary_input = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
                dietary_restrictions = None
                if dietary_input:
                    dietary_restrictions = [d.strip() for d in dietary_input.split(',')]
                
                # Optional: Ask for cuisine preference
                print(f"\n{Fore.CYAN}Preferred cuisine type? (optional){Style.RESET_ALL}")
                cuisine_input = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
                cuisine_preference = cuisine_input if cuisine_input else None
                
                # Show loading message
                print(f"\n{Fore.YELLOW}🤖 Generating recipe recommendations...{Style.RESET_ALL}")
                
                # Get recommendations
                recommendations = await self.get_recipe_recommendations(
                    ingredients, dietary_restrictions, cuisine_preference
                )
                
                # Display results
                print(f"\n{Fore.GREEN}{Style.BRIGHT}📋 Recipe Recommendations:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{recommendations}{Style.RESET_ALL}")
                
                print(f"\n{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}\n")
                
            except ValueError as e:
                print(f"{Fore.RED}❌ {e}{Style.RESET_ALL}\n")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Happy cooking!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}\n")
                if self.debug:
                    self.logger.exception("Full error details:")

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Recipe Recommendation Agent")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--ingredients", type=str, help="Comma-separated list of ingredients")
    parser.add_argument("--dietary", type=str, help="Comma-separated dietary restrictions")
    parser.add_argument("--cuisine", type=str, help="Preferred cuisine type")
    
    args = parser.parse_args()
    
    # Create agent instance
    agent = RecipeAgent(debug=args.debug)
    
    if args.ingredients:
        # Single-shot mode
        try:
            ingredients = agent.validate_ingredients(args.ingredients)
            dietary_restrictions = None
            if args.dietary:
                dietary_restrictions = [d.strip() for d in args.dietary.split(',')]
            
            agent.print_welcome()
            print(f"{Fore.YELLOW}🤖 Generating recipe recommendations...{Style.RESET_ALL}")
            
            recommendations = await agent.get_recipe_recommendations(
                ingredients, dietary_restrictions, args.cuisine
            )
            
            print(f"\n{Fore.GREEN}{Style.BRIGHT}📋 Recipe Recommendations:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{recommendations}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            sys.exit(1)
    else:
        # Interactive mode
        await agent.interactive_mode()

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("GITHUB_TOKEN"):
        print(f"{Fore.RED}❌ Error: GITHUB_TOKEN environment variable is required{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please set your GitHub Personal Access Token:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}export GITHUB_TOKEN=your_token_here{Style.RESET_ALL}")
        sys.exit(1)
    
    # Run the async main function
    asyncio.run(main())