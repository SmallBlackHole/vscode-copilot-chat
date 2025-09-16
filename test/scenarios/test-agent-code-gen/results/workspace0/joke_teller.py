"""
AI Joke Teller Console App

A simple console application that tells jokes about any given topic using AI.
Uses the Microsoft Agent Framework with GitHub models for cost-effective joke generation.
"""

import asyncio
import os
import sys
from typing import Optional

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI


class JokeTeller:
    """AI-powered joke teller that generates jokes about any topic."""
    
    def __init__(self, github_token: str, model_id: str = "openai/gpt-4.1-mini"):
        """
        Initialize the JokeTeller with GitHub model credentials.
        
        Args:
            github_token: GitHub Personal Access Token for model access
            model_id: The model ID to use (default: openai/gpt-4.1-mini)
        """
        self.github_token = github_token
        self.model_id = model_id
        self.agent: Optional[ChatAgent] = None
    
    async def initialize(self):
        """Initialize the AI agent for joke telling."""
        try:
            # Create OpenAI client pointing to GitHub models endpoint
            openai_client = AsyncOpenAI(
                base_url="https://models.github.ai/inference",
                api_key=self.github_token,
            )
            
            # Create chat client
            chat_client = OpenAIChatClient(
                async_client=openai_client,
                ai_model_id=self.model_id
            )
            
            # Create the joke-telling agent
            self.agent = ChatAgent(
                chat_client=chat_client,
                name="JokeTeller",
                instructions="""You are a witty and family-friendly comedian AI. 
                Your job is to tell creative, clean, and funny jokes about any topic the user provides.
                
                Guidelines:
                - Keep jokes appropriate for all audiences
                - Be creative and original with your humor
                - If asked about a topic, create 1-3 jokes related to that topic
                - Use various joke formats: puns, one-liners, knock-knock jokes, etc.
                - Make the jokes engaging and entertaining
                - If the topic is sensitive, redirect to light-hearted aspects
                """
            )
            
            print("🎭 AI Joke Teller initialized successfully!")
            print("💡 Using model:", self.model_id)
            
        except Exception as e:
            print(f"❌ Error initializing joke teller: {e}")
            raise
    
    async def tell_joke(self, topic: str) -> str:
        """
        Generate and return a joke about the given topic.
        
        Args:
            topic: The topic to create jokes about
            
        Returns:
            The generated joke(s) as a string
        """
        if not self.agent:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        
        try:
            # Create a prompt for joke generation
            prompt = f"Tell me a funny, clean joke about: {topic}"
            
            # Get response from the agent
            result = await self.agent.run(prompt)
            return result.text
            
        except Exception as e:
            return f"😅 Oops! I couldn't come up with a joke right now. Error: {e}"
    
    async def interactive_mode(self):
        """Run the joke teller in interactive mode."""
        print("\n🎪 Welcome to the AI Joke Teller!")
        print("📝 Enter any topic and I'll tell you a joke about it.")
        print("💬 Type 'quit', 'exit', or 'bye' to stop.\n")
        
        while True:
            try:
                # Get topic from user
                topic = input("🎯 What topic would you like a joke about? ").strip()
                
                # Check for exit commands
                if topic.lower() in ['quit', 'exit', 'bye', '']:
                    print("👋 Thanks for using AI Joke Teller! Have a great day!")
                    break
                
                # Generate and display joke
                print("🤔 Thinking of a joke...")
                joke = await self.tell_joke(topic)
                print(f"\n😂 Here's your joke:\n{joke}\n")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using AI Joke Teller!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")


async def main():
    """Main function to run the joke teller application."""
    print("🎭 AI Joke Teller - Powered by Microsoft Agent Framework & GitHub Models")
    print("=" * 70)
    
    # Get GitHub token from environment variable or user input
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("\n🔑 GitHub Personal Access Token required to access models.")
        print("💡 You can either:")
        print("   1. Set GITHUB_TOKEN environment variable")
        print("   2. Enter it below (will not be stored)")
        github_token = input("\n🔐 Enter your GitHub token: ").strip()
        
        if not github_token:
            print("❌ GitHub token is required to use AI models. Exiting.")
            sys.exit(1)
    
    # Allow user to choose model (optional)
    print(f"\n🤖 Available models (or press Enter for default):")
    print("   • openai/gpt-4.1-mini (default - fast & cost-effective)")
    print("   • openai/gpt-4.1 (more capable)")
    print("   • openai/gpt-4o-mini (multimodal)")
    
    model_choice = input("\n🎯 Choose model (or press Enter for default): ").strip()
    model_id = model_choice if model_choice else "openai/gpt-4.1-mini"
    
    try:
        # Create and initialize joke teller
        joke_teller = JokeTeller(github_token, model_id)
        await joke_teller.initialize()
        
        # Check if running in interactive mode or with command line argument
        if len(sys.argv) > 1:
            # Single joke mode - topic provided as command line argument
            topic = ' '.join(sys.argv[1:])
            print(f"\n🎯 Topic: {topic}")
            joke = await joke_teller.tell_joke(topic)
            print(f"\n😂 Your joke:\n{joke}")
        else:
            # Interactive mode
            await joke_teller.interactive_mode()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())