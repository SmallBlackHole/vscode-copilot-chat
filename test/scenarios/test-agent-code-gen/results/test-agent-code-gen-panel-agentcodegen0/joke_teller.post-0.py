#!/usr/bin/env python3
"""
AI Joke Teller Console App

A simple console application that uses GitHub Models (AI) to generate jokes
about user-specified topics. This app demonstrates how to integrate AI 
capabilities into a console application using OpenAI's API with GitHub Models.

Usage:
    python joke_teller.py

Requirements:
    - Python 3.7+
    - openai package
    - python-dotenv package
    - GitHub Personal Access Token (set in .env file)
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

class JokeTeller:
    """A class to handle AI-powered joke generation."""
    
    def __init__(self):
        """Initialize the JokeTeller with GitHub Models configuration."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Get GitHub token from environment
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("❌ Error: GITHUB_TOKEN not found in environment variables.")
            print("Please create a .env file with your GitHub Personal Access Token.")
            print("See .env.example for the required format.")
            sys.exit(1)
        
        # Initialize OpenAI client with GitHub Models endpoint
        self.client = OpenAI(
            api_key=github_token,
            base_url="https://models.github.ai"
        )
        
        # Using GPT-4.1-mini for cost-effective joke generation
        self.model = "openai/gpt-4.1-mini"
        
    def generate_joke(self, topic):
        """
        Generate a joke about the given topic using AI.
        
        Args:
            topic (str): The topic to generate a joke about
            
        Returns:
            str: The generated joke
        """
        try:
            # Create a prompt for joke generation
            prompt = f"""You are a friendly comedian. Tell me a clean, funny joke about {topic}. 
            Make it appropriate for all audiences and genuinely amusing. 
            Keep it concise but entertaining."""
            
            # Make API call to GitHub Models
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a witty comedian who tells clean, family-friendly jokes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8  # Higher temperature for more creative jokes
            )
            
            # Extract and return the joke
            joke = response.choices[0].message.content.strip()
            return joke
            
        except Exception as e:
            return f"Sorry, I couldn't generate a joke right now. Error: {str(e)}"
    
    def run(self):
        """Main application loop."""
        print("🎭 Welcome to the AI Joke Teller! 🎭")
        print("I can tell jokes about any topic you'd like!")
        print("Type 'quit' or 'exit' to stop.\n")
        
        while True:
            try:
                # Get topic from user
                topic = input("What topic would you like a joke about? ").strip()
                
                # Check for exit commands
                if topic.lower() in ['quit', 'exit', 'q']:
                    print("Thanks for using the AI Joke Teller! Have a great day! 👋")
                    break
                
                # Validate input
                if not topic:
                    print("Please enter a topic for the joke.\n")
                    continue
                
                # Generate and display joke
                print(f"\n🤔 Thinking of a joke about '{topic}'...")
                joke = self.generate_joke(topic)
                print(f"\n😄 Here's your joke:\n{joke}\n")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\nThanks for using the AI Joke Teller! Have a great day! 👋")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                print("Let's try again!\n")

def main():
    """Main entry point for the application."""
    joke_teller = JokeTeller()
    joke_teller.run()

if __name__ == "__main__":
    main()