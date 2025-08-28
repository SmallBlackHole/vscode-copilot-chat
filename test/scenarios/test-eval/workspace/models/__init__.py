from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class DietaryRestriction(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    NUT_FREE = "nut_free"
    KETO = "keto"
    PALEO = "paleo"


class MeasurementUnit(str, Enum):
    CUP = "cup"
    TABLESPOON = "tablespoon"
    TEASPOON = "teaspoon"
    OUNCE = "ounce"
    POUND = "pound"
    GRAM = "gram"
    KILOGRAM = "kilogram"
    PIECE = "piece"
    CLOVE = "clove"
    BUNCH = "bunch"
    PACKAGE = "package"


class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: MeasurementUnit
    category: str = "general"  # produce, dairy, meat, pantry, etc.
    notes: Optional[str] = None


class Recipe(BaseModel):
    name: str
    description: str
    servings: int
    prep_time_minutes: int
    cook_time_minutes: int
    difficulty: str = "medium"  # easy, medium, hard
    cuisine: str = "american"
    dietary_restrictions: List[DietaryRestriction] = []
    ingredients: List[Ingredient]
    instructions: List[str]
    tips: List[str] = []


class PantryItem(BaseModel):
    name: str
    quantity: float
    unit: MeasurementUnit
    expiry_date: Optional[datetime] = None
    location: str = "pantry"  # pantry, fridge, freezer


class ContosoProduct(BaseModel):
    id: str
    name: str
    price: float
    category: str
    brand: str
    size: str
    unit: MeasurementUnit
    availability: bool = True
    rating: float = 0.0
    image_url: Optional[str] = None


class ShoppingCartItem(BaseModel):
    product: ContosoProduct
    quantity: int
    added_at: datetime = Field(default_factory=datetime.now)


class ShoppingCart(BaseModel):
    id: str
    items: List[ShoppingCartItem] = []
    total_price: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)
    
    def add_item(self, product: ContosoProduct, quantity: int = 1):
        """Add item to cart or update quantity if already exists."""
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += quantity
                break
        else:
            self.items.append(ShoppingCartItem(product=product, quantity=quantity))
        
        self.calculate_total()
    
    def calculate_total(self):
        """Calculate total price of items in cart."""
        self.total_price = sum(item.product.price * item.quantity for item in self.items)


class CookingPlan(BaseModel):
    id: str
    name: str
    recipes: List[Recipe]
    total_servings: int
    total_prep_time: int
    total_cook_time: int
    all_ingredients: List[Ingredient]
    missing_ingredients: List[Ingredient] = []
    shopping_cart: Optional[ShoppingCart] = None
    created_at: datetime = Field(default_factory=datetime.now)


class UserPreferences(BaseModel):
    dietary_restrictions: List[DietaryRestriction] = []
    favorite_cuisines: List[str] = []
    cooking_skill_level: str = "intermediate"  # beginner, intermediate, advanced
    available_time_minutes: int = 60
    serving_size: int = 4
    budget_limit: Optional[float] = None
    pantry_items: List[PantryItem] = []
