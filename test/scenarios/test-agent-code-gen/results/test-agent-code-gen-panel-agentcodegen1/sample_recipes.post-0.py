#!/usr/bin/env python3
"""
Sample usage examples for the Recipe Recommendation Agent
"""

import asyncio
import os
from recipe_agent import RecipeAgent

async def example_basic_usage():
    """Example of basic recipe recommendation"""
    print("=== Basic Usage Example ===")
    
    # Create agent instance
    agent = RecipeAgent(debug=False)
    
    # Example ingredients
    ingredients = ["chicken", "rice", "broccoli"]
    
    print(f"Ingredients: {', '.join(ingredients)}")
    
    # Get recommendations
    recommendations = await agent.get_recipe_recommendations(ingredients)
    
    print("Recommendations:")
    print(recommendations)
    print("\n" + "="*50 + "\n")

async def example_with_dietary_restrictions():
    """Example with dietary restrictions"""
    print("=== Dietary Restrictions Example ===")
    
    agent = RecipeAgent(debug=False)
    
    ingredients = ["tofu", "spinach", "mushrooms", "garlic"]
    dietary_restrictions = ["vegetarian", "gluten-free"]
    
    print(f"Ingredients: {', '.join(ingredients)}")
    print(f"Dietary restrictions: {', '.join(dietary_restrictions)}")
    
    recommendations = await agent.get_recipe_recommendations(
        ingredients, 
        dietary_restrictions=dietary_restrictions
    )
    
    print("Recommendations:")
    print(recommendations)
    print("\n" + "="*50 + "\n")

async def example_with_cuisine_preference():
    """Example with cuisine preference"""
    print("=== Cuisine Preference Example ===")
    
    agent = RecipeAgent(debug=False)
    
    ingredients = ["shrimp", "noodles", "bell peppers", "soy sauce"]
    cuisine_preference = "Asian"
    
    print(f"Ingredients: {', '.join(ingredients)}")
    print(f"Cuisine preference: {cuisine_preference}")
    
    recommendations = await agent.get_recipe_recommendations(
        ingredients,
        cuisine_preference=cuisine_preference
    )
    
    print("Recommendations:")
    print(recommendations)
    print("\n" + "="*50 + "\n")

async def example_comprehensive():
    """Example with all parameters"""
    print("=== Comprehensive Example ===")
    
    agent = RecipeAgent(debug=False)
    
    ingredients = ["salmon", "quinoa", "asparagus", "lemon"]
    dietary_restrictions = ["pescatarian", "low-carb"]
    cuisine_preference = "Mediterranean"
    
    print(f"Ingredients: {', '.join(ingredients)}")
    print(f"Dietary restrictions: {', '.join(dietary_restrictions)}")
    print(f"Cuisine preference: {cuisine_preference}")
    
    recommendations = await agent.get_recipe_recommendations(
        ingredients,
        dietary_restrictions=dietary_restrictions,
        cuisine_preference=cuisine_preference
    )
    
    print("Recommendations:")
    print(recommendations)
    print("\n" + "="*50 + "\n")

def sample_expected_outputs():
    """Show sample expected outputs"""
    print("=== Sample Expected Outputs ===")
    print("""
Example 1: Basic chicken, rice, broccoli
----------------------------------------
🤖 Based on your ingredients (chicken, rice, broccoli), here are some delicious recipe recommendations:

1. **Chicken and Broccoli Rice Bowl**
   - A healthy one-bowl meal with seasoned chicken, steamed broccoli, and fluffy rice
   - Cook time: 25 minutes
   - Difficulty: Easy

2. **Chicken Fried Rice with Broccoli**
   - Classic fried rice with diced chicken and fresh broccoli florets
   - Cook time: 20 minutes
   - Difficulty: Easy

3. **Teriyaki Chicken Rice Casserole**
   - Baked casserole with teriyaki-glazed chicken, rice, and broccoli
   - Cook time: 45 minutes
   - Difficulty: Medium

Would you like detailed cooking instructions for any of these recipes?

Example 2: Vegetarian with restrictions
---------------------------------------
🤖 Here are some vegetarian, gluten-free recipes using tofu, spinach, mushrooms, and garlic:

1. **Garlic Mushroom Tofu Stir-fry**
   - Crispy tofu with sautéed mushrooms, wilted spinach, and aromatic garlic
   - Cook time: 15 minutes
   - Difficulty: Easy

2. **Spinach and Mushroom Tofu Scramble**
   - Protein-rich breakfast scramble with seasoned tofu and fresh vegetables
   - Cook time: 12 minutes
   - Difficulty: Easy

3. **Asian-Style Tofu and Vegetable Curry**
   - Fragrant curry with tofu, mushrooms, and spinach in coconut milk
   - Cook time: 30 minutes
   - Difficulty: Medium
""")

async def main():
    """Run all examples"""
    
    # Check if GitHub token is set
    if not os.getenv("GITHUB_TOKEN"):
        print("❌ GITHUB_TOKEN environment variable is required to run examples")
        print("Please set your GitHub Personal Access Token:")
        print("export GITHUB_TOKEN=your_token_here")
        return
    
    print("🍳 Recipe Agent Examples")
    print("=" * 40)
    print()
    
    try:
        await example_basic_usage()
        await example_with_dietary_restrictions()
        await example_with_cuisine_preference()
        await example_comprehensive()
        
        sample_expected_outputs()
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("Make sure your GITHUB_TOKEN is valid and you have internet connection.")

if __name__ == "__main__":
    asyncio.run(main())