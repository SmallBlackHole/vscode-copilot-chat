"""
Configuration settings for the Recipe Recommendation Agent
"""

import os
from typing import List, Optional
from pydantic import BaseSettings

class AgentConfig(BaseSettings):
    """Configuration for the Recipe Recommendation Agent"""
    
    # GitHub Models Configuration
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    base_url: str = "https://models.github.ai/inference/"
    
    # Model Settings
    default_model: str = "openai/gpt-4o-mini"
    reasoning_model: str = "openai/o1-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # Agent Behavior
    max_recipes: int = 3
    include_instructions: bool = True
    difficulty_levels: List[str] = ["Easy", "Medium", "Hard"]
    
    # Dietary Preferences (can be overridden by user input)
    default_dietary_restrictions: List[str] = []
    default_cuisine_preferences: List[str] = []
    
    # System Prompts
    system_prompt: str = """You are a helpful recipe recommendation agent. Your role is to suggest delicious and practical recipes based on the ingredients users provide.

Guidelines:
1. Always suggest recipes that primarily use the provided ingredients
2. Include cooking time and difficulty level
3. Consider dietary restrictions if mentioned
4. Provide brief, appetizing descriptions
5. Ask if the user wants detailed instructions
6. Be creative but practical
7. Suggest recipes with varying difficulty levels when possible

Format your responses clearly with recipe names, descriptions, cook times, and difficulty levels."""

    @property
    def model_config(self) -> dict:
        """Get model configuration for GitHub models"""
        return {
            "model": self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "base_url": self.base_url,
            "api_key": self.github_token
        }

# Global configuration instance
config = AgentConfig()