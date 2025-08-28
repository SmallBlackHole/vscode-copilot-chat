import json
import asyncio
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

from agents import Agent, function_tool, RunContextWrapper
from models import (
    Recipe, Ingredient, CookingPlan, UserPreferences, 
    MeasurementUnit, DietaryRestriction, ContosoProduct, ShoppingCart
)
from services import get_contoso_service
from utils import console_formatter


class RecipeRequest(TypedDict):
    """Type definition for recipe generation requests."""
    dish_name: str
    cuisine: str
    servings: int
    dietary_restrictions: List[str]
    available_time_minutes: int


class IngredientAnalysis(TypedDict):
    """Type definition for ingredient analysis results."""
    required_ingredients: List[str]
    missing_ingredients: List[str]
    pantry_items: List[str]


@function_tool
async def generate_recipe(ctx: RunContextWrapper[Any], recipe_request: RecipeRequest) -> str:
    """Generate a detailed recipe based on user preferences and constraints.
    
    Args:
        recipe_request: Details about the desired recipe including dish name, 
                       cuisine, servings, dietary restrictions, and time constraints.
    """
    console_formatter.print_info(f"🤖 Generating recipe for: {recipe_request['dish_name']}")
    
    # This is a mock implementation - in a real app, this would use the LLM
    # to generate recipes based on the request parameters
    
    # Sample recipe generation (mock)
    if "pasta" in recipe_request['dish_name'].lower():
        recipe = Recipe(
            name="Creamy Garlic Parmesan Pasta",
            description="A rich and creamy pasta dish with garlic and parmesan cheese",
            servings=recipe_request['servings'],
            prep_time_minutes=15,
            cook_time_minutes=20,
            difficulty="easy",
            cuisine=recipe_request['cuisine'],
            dietary_restrictions=[DietaryRestriction(r) for r in recipe_request['dietary_restrictions'] if r in [e.value for e in DietaryRestriction]],
            ingredients=[
                Ingredient(name="Pasta", quantity=1.0, unit=MeasurementUnit.POUND, category="pantry"),
                Ingredient(name="Heavy Cream", quantity=1.0, unit=MeasurementUnit.CUP, category="dairy"),
                Ingredient(name="Garlic", quantity=3.0, unit=MeasurementUnit.CLOVE, category="produce"),
                Ingredient(name="Parmesan Cheese", quantity=0.5, unit=MeasurementUnit.CUP, category="dairy"),
                Ingredient(name="Butter", quantity=2.0, unit=MeasurementUnit.TABLESPOON, category="dairy"),
                Ingredient(name="Salt", quantity=1.0, unit=MeasurementUnit.TEASPOON, category="pantry"),
                Ingredient(name="Black Pepper", quantity=0.5, unit=MeasurementUnit.TEASPOON, category="pantry"),
            ],
            instructions=[
                "Bring a large pot of salted water to boil and cook pasta according to package directions",
                "In a large skillet, melt butter over medium heat and add minced garlic",
                "Cook garlic for 1-2 minutes until fragrant, then add heavy cream",
                "Simmer cream for 3-4 minutes until slightly thickened",
                "Add cooked pasta to the skillet and toss with the cream sauce",
                "Remove from heat and add parmesan cheese, salt, and pepper",
                "Toss until cheese melts and pasta is well coated",
                "Serve immediately with additional parmesan if desired"
            ],
            tips=[
                "Don't let the cream boil or it may curdle",
                "Save some pasta water to thin the sauce if needed",
                "Use freshly grated parmesan for best flavor"
            ]
        )
    else:
        # Default chicken recipe
        recipe = Recipe(
            name=f"Simple {recipe_request['dish_name'].title()}",
            description=f"A delicious {recipe_request['dish_name']} recipe",
            servings=recipe_request['servings'],
            prep_time_minutes=10,
            cook_time_minutes=25,
            difficulty="medium",
            cuisine=recipe_request['cuisine'],
            dietary_restrictions=[DietaryRestriction(r) for r in recipe_request['dietary_restrictions'] if r in [e.value for e in DietaryRestriction]],
            ingredients=[
                Ingredient(name="Chicken Breast", quantity=2.0, unit=MeasurementUnit.POUND, category="meat"),
                Ingredient(name="Olive Oil", quantity=2.0, unit=MeasurementUnit.TABLESPOON, category="pantry"),
                Ingredient(name="Salt", quantity=1.0, unit=MeasurementUnit.TEASPOON, category="pantry"),
                Ingredient(name="Black Pepper", quantity=0.5, unit=MeasurementUnit.TEASPOON, category="pantry"),
                Ingredient(name="Garlic", quantity=2.0, unit=MeasurementUnit.CLOVE, category="produce"),
            ],
            instructions=[
                "Season chicken with salt and pepper",
                "Heat olive oil in a large skillet over medium-high heat",
                "Add chicken and cook for 6-7 minutes per side until golden brown",
                "Add minced garlic and cook for 1 minute more",
                "Let rest for 5 minutes before serving"
            ],
            tips=[
                "Use a meat thermometer to ensure chicken reaches 165°F internal temperature"
            ]
        )
    
    # Store the recipe in context for later use
    if not hasattr(ctx, 'recipes'):
        ctx.recipes = []
    ctx.recipes.append(recipe)
    
    return json.dumps({
        "recipe_generated": True,
        "recipe_name": recipe.name,
        "total_ingredients": len(recipe.ingredients),
        "prep_time": recipe.prep_time_minutes,
        "cook_time": recipe.cook_time_minutes
    })


@function_tool
async def analyze_pantry_ingredients(ctx: RunContextWrapper[Any], 
                                   required_ingredients: List[str],
                                   user_pantry: List[str]) -> str:
    """Analyze which ingredients are missing from the user's pantry.
    
    Args:
        required_ingredients: List of ingredients needed for the recipes.
        user_pantry: List of ingredients currently available in user's pantry.
    """
    console_formatter.print_info("🔍 Analyzing pantry inventory...")
    
    # Convert to lowercase for comparison
    available_lower = [item.lower().strip() for item in user_pantry]
    required_lower = [item.lower().strip() for item in required_ingredients]
    
    # Find missing ingredients
    missing = []
    available = []
    
    for req_ingredient in required_ingredients:
        req_lower = req_ingredient.lower().strip()
        
        # Check for exact match or partial match
        found = False
        for avail_ingredient in available_lower:
            if req_lower in avail_ingredient or avail_ingredient in req_lower:
                found = True
                available.append(req_ingredient)
                break
        
        if not found:
            missing.append(req_ingredient)
    
    analysis = {
        "total_required": len(required_ingredients),
        "available_count": len(available),
        "missing_count": len(missing),
        "missing_ingredients": missing,
        "available_ingredients": available
    }
    
    # Store analysis in context
    ctx.ingredient_analysis = analysis
    
    return json.dumps(analysis)


@function_tool
async def search_contoso_products(ctx: RunContextWrapper[Any], 
                                ingredient_name: str,
                                quantity: float = 1.0,
                                unit: str = "piece") -> str:
    """Search for products in the Contoso catalog that match a cooking ingredient.
    
    Args:
        ingredient_name: Name of the ingredient to search for.
        quantity: Amount needed for the recipe.
        unit: Unit of measurement for the ingredient.
    """
    console_formatter.print_info(f"🔍 Searching Contoso catalog for: {ingredient_name}")
    
    contoso_service = get_contoso_service()
    products = await contoso_service.find_ingredient_products(ingredient_name, quantity, unit)
    
    if products:
        console_formatter.print_products_search_results(products, ingredient_name)
        
        # Store products in context
        if not hasattr(ctx, 'found_products'):
            ctx.found_products = {}
        ctx.found_products[ingredient_name] = products
        
        return json.dumps({
            "ingredient": ingredient_name,
            "products_found": len(products),
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "brand": p.brand,
                    "rating": p.rating
                } for p in products
            ]
        })
    else:
        console_formatter.print_error(f"No products found for {ingredient_name}")
        return json.dumps({
            "ingredient": ingredient_name,
            "products_found": 0,
            "products": []
        })


@function_tool
async def add_to_contoso_cart(ctx: RunContextWrapper[Any], 
                            product_id: str,
                            quantity: int = 1) -> str:
    """Add a product to the Contoso shopping cart.
    
    Args:
        product_id: ID of the product to add to cart.
        quantity: Number of items to add.
    """
    console_formatter.print_info(f"🛒 Adding product {product_id} to cart...")
    
    contoso_service = get_contoso_service()
    success = await contoso_service.add_to_cart(product_id, quantity)
    
    if success:
        product = await contoso_service.get_product_by_id(product_id)
        console_formatter.print_success(f"Added {product.name} to your cart!")
        
        return json.dumps({
            "success": True,
            "product_id": product_id,
            "product_name": product.name,
            "quantity": quantity,
            "message": f"Successfully added {quantity}x {product.name} to cart"
        })
    else:
        console_formatter.print_error(f"Failed to add product {product_id} to cart")
        return json.dumps({
            "success": False,
            "product_id": product_id,
            "quantity": quantity,
            "message": "Failed to add product to cart - product may be unavailable"
        })


@function_tool
async def get_shopping_cart_summary(ctx: RunContextWrapper[Any]) -> str:
    """Get the current contents and total of the shopping cart.
    """
    console_formatter.print_info("🛒 Retrieving shopping cart...")
    
    contoso_service = get_contoso_service()
    cart = await contoso_service.get_cart()
    
    console_formatter.print_shopping_cart(cart)
    
    return json.dumps({
        "cart_id": cart.id,
        "items_count": len(cart.items),
        "total_price": cart.total_price,
        "items": [
            {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.product.price,
                "total_price": item.product.price * item.quantity
            } for item in cart.items
        ]
    })


# Agent Definitions

def create_cooking_planner_agent() -> Agent:
    """Create the main cooking planner agent."""
    return Agent(
        name="Cooking Planner",
        instructions="""You are an expert cooking planner and meal preparation assistant. Your role is to:

1. Help users create detailed cooking plans based on their preferences, dietary restrictions, and available time
2. Generate comprehensive recipes with ingredients, instructions, and helpful tips
3. Consider user's skill level, cuisine preferences, and serving size requirements
4. Provide realistic time estimates for preparation and cooking
5. Suggest cooking tips and techniques to improve results

When creating recipes:
- Always include accurate ingredient quantities and measurements
- Provide clear, step-by-step instructions
- Consider dietary restrictions and allergies
- Suggest substitutions when possible
- Include helpful cooking tips and techniques

Be enthusiastic about cooking while being practical and helpful.""",
        tools=[generate_recipe],
        handoffs=[]  # Will hand off to other agents as needed
    )


def create_pantry_analyzer_agent() -> Agent:
    """Create the pantry analysis agent."""
    return Agent(
        name="Pantry Analyzer",
        instructions="""You are a pantry management specialist. Your role is to:

1. Analyze what ingredients users have available in their pantry, fridge, and freezer
2. Compare required recipe ingredients against available inventory
3. Identify missing ingredients that need to be purchased
4. Suggest substitutions for missing ingredients when possible
5. Help optimize ingredient usage across multiple recipes

When analyzing ingredients:
- Be thorough in checking for partial matches (e.g., "garlic powder" might substitute for "garlic")
- Consider different forms of ingredients (fresh vs. dried, whole vs. ground)
- Suggest reasonable substitutions based on cooking principles
- Prioritize commonly available pantry staples

Always provide clear lists of what's available vs. what's missing.""",
        tools=[analyze_pantry_ingredients],
        handoffs=[]
    )


def create_shopping_assistant_agent() -> Agent:
    """Create the shopping assistance agent."""
    return Agent(
        name="Shopping Assistant",
        instructions="""You are a smart shopping assistant specialized in finding ingredients and managing shopping carts. Your role is to:

1. Search the Contoso product catalog for cooking ingredients
2. Find the best products that match recipe requirements
3. Add items to the shopping cart automatically
4. Provide product recommendations based on quality, price, and reviews
5. Manage the shopping cart and provide cost summaries

When searching for products:
- Try multiple search terms for each ingredient (e.g., "tomato", "tomatoes", "fresh tomato")
- Consider different brands and package sizes
- Prioritize products with good ratings and reasonable prices
- Automatically add the best matches to the cart unless user specifies otherwise
- Always confirm additions to the cart

Be proactive in finding alternatives if exact matches aren't available.""",
        tools=[search_contoso_products, add_to_contoso_cart, get_shopping_cart_summary],
        handoffs=[]
    )


def create_cooking_coordinator_agent() -> Agent:
    """Create the main coordinator agent that orchestrates the cooking planning process."""
    
    return Agent(
        name="Cooking Coordinator",
        instructions="""You are the main coordinator for the AI-powered cooking plan system. Your role is to:

1. Understand user's cooking requests and preferences
2. Generate detailed recipes using the generate_recipe tool
3. Analyze pantry inventory using the analyze_pantry_ingredients tool
4. Search for missing ingredients using the search_contoso_products tool
5. Add items to cart using the add_to_contoso_cart tool
6. Provide final summaries using get_shopping_cart_summary tool

Your workflow should be:
1. Parse the user's cooking request and use generate_recipe tool to create a recipe
2. Extract the required ingredients and use analyze_pantry_ingredients to check availability
3. For each missing ingredient, use search_contoso_products to find products
4. Use add_to_contoso_cart to add the best products to the cart
5. Use get_shopping_cart_summary to show the final cart

IMPORTANT: You must actually call the tools, not just describe what you would do. Use the tools to complete each step of the workflow.""",
        tools=[
            generate_recipe,
            analyze_pantry_ingredients,
            search_contoso_products,
            add_to_contoso_cart,
            get_shopping_cart_summary
        ],
        handoffs=[]
    )


# Export the main agent
def get_main_agent() -> Agent:
    """Get the main cooking coordinator agent."""
    return create_cooking_coordinator_agent()
