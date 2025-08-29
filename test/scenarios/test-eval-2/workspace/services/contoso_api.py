import asyncio
import random
from typing import List, Optional, Dict, Any
from models import ContosoProduct, ShoppingCart, MeasurementUnit


class ContosoAPIService:
    """Mock service for Contoso product catalog and shopping cart."""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.products_db = self._initialize_mock_products()
        self.cart = ShoppingCart(id="default_cart")
    
    def _initialize_mock_products(self) -> List[ContosoProduct]:
        """Initialize mock product database."""
        products = [
            # Produce
            ContosoProduct(id="P001", name="Organic Tomatoes", price=3.99, category="produce", 
                         brand="Farm Fresh", size="1 lb", unit=MeasurementUnit.POUND, rating=4.5),
            ContosoProduct(id="P002", name="Yellow Onions", price=2.49, category="produce", 
                         brand="Garden Best", size="3 lb bag", unit=MeasurementUnit.POUND, rating=4.2),
            ContosoProduct(id="P003", name="Fresh Garlic", price=1.99, category="produce", 
                         brand="Fresh Valley", size="3 bulbs", unit=MeasurementUnit.PIECE, rating=4.7),
            ContosoProduct(id="P004", name="Bell Peppers", price=4.99, category="produce", 
                         brand="Colorful Farms", size="3 pack", unit=MeasurementUnit.PIECE, rating=4.3),
            ContosoProduct(id="P005", name="Fresh Basil", price=2.99, category="produce", 
                         brand="Herb Garden", size="1 package", unit=MeasurementUnit.PACKAGE, rating=4.6),
            
            # Dairy & Eggs
            ContosoProduct(id="D001", name="Whole Milk", price=3.79, category="dairy", 
                         brand="Dairy Pure", size="1 gallon", unit=MeasurementUnit.CUP, rating=4.4),
            ContosoProduct(id="D002", name="Large Eggs", price=4.99, category="dairy", 
                         brand="Farm Fresh", size="12 count", unit=MeasurementUnit.PIECE, rating=4.8),
            ContosoProduct(id="D003", name="Mozzarella Cheese", price=5.99, category="dairy", 
                         brand="Italian Best", size="8 oz", unit=MeasurementUnit.OUNCE, rating=4.5),
            ContosoProduct(id="D004", name="Butter", price=4.49, category="dairy", 
                         brand="Creamery Gold", size="1 lb", unit=MeasurementUnit.POUND, rating=4.6),
            
            # Meat & Seafood
            ContosoProduct(id="M001", name="Chicken Breast", price=8.99, category="meat", 
                         brand="Farm Raised", size="2 lb", unit=MeasurementUnit.POUND, rating=4.3),
            ContosoProduct(id="M002", name="Ground Beef", price=7.99, category="meat", 
                         brand="Premium Choice", size="1 lb", unit=MeasurementUnit.POUND, rating=4.5),
            ContosoProduct(id="M003", name="Salmon Fillet", price=12.99, category="seafood", 
                         brand="Ocean Fresh", size="1 lb", unit=MeasurementUnit.POUND, rating=4.7),
            
            # Pantry Staples
            ContosoProduct(id="S001", name="Olive Oil", price=8.99, category="pantry", 
                         brand="Mediterranean Gold", size="500ml", unit=MeasurementUnit.CUP, rating=4.8),
            ContosoProduct(id="S002", name="Sea Salt", price=2.99, category="pantry", 
                         brand="Ocean Harvest", size="26 oz", unit=MeasurementUnit.OUNCE, rating=4.5),
            ContosoProduct(id="S003", name="Black Pepper", price=3.99, category="pantry", 
                         brand="Spice Master", size="2 oz", unit=MeasurementUnit.OUNCE, rating=4.6),
            ContosoProduct(id="S004", name="All-Purpose Flour", price=3.49, category="pantry", 
                         brand="Baker's Best", size="5 lb", unit=MeasurementUnit.POUND, rating=4.4),
            ContosoProduct(id="S005", name="White Rice", price=4.99, category="pantry", 
                         brand="Premium Grain", size="2 lb", unit=MeasurementUnit.POUND, rating=4.5),
            
            # Specialty Items
            ContosoProduct(id="SP001", name="Balsamic Vinegar", price=6.99, category="condiments", 
                         brand="Italian Classic", size="250ml", unit=MeasurementUnit.CUP, rating=4.7),
            ContosoProduct(id="SP002", name="Honey", price=5.99, category="pantry", 
                         brand="Pure Gold", size="12 oz", unit=MeasurementUnit.OUNCE, rating=4.8),
            ContosoProduct(id="SP003", name="Soy Sauce", price=3.99, category="condiments", 
                         brand="Asian Kitchen", size="10 fl oz", unit=MeasurementUnit.OUNCE, rating=4.5),
        ]
        return products
    
    async def search_products(self, query: str, category: Optional[str] = None) -> List[ContosoProduct]:
        """Search for products by name or description."""
        # Simulate API delay
        await asyncio.sleep(0.2)
        
        query_lower = query.lower()
        results = []
        
        for product in self.products_db:
            name_match = query_lower in product.name.lower()
            category_match = category is None or product.category.lower() == category.lower()
            
            if name_match and category_match:
                results.append(product)
        
        # If no exact matches, try fuzzy matching
        if not results:
            for product in self.products_db:
                # Simple fuzzy matching - check if any word in query appears in product name
                query_words = query_lower.split()
                product_words = product.name.lower().split()
                
                if any(qword in pword for qword in query_words for pword in product_words):
                    if category is None or product.category.lower() == category.lower():
                        results.append(product)
        
        return results[:10]  # Return top 10 matches
    
    async def get_product_by_id(self, product_id: str) -> Optional[ContosoProduct]:
        """Get a specific product by ID."""
        await asyncio.sleep(0.1)
        
        for product in self.products_db:
            if product.id == product_id:
                return product
        return None
    
    async def add_to_cart(self, product_id: str, quantity: int = 1) -> bool:
        """Add a product to the shopping cart."""
        await asyncio.sleep(0.1)
        
        product = await self.get_product_by_id(product_id)
        if product and product.availability:
            self.cart.add_item(product, quantity)
            return True
        return False
    
    async def get_cart(self) -> ShoppingCart:
        """Get the current shopping cart."""
        await asyncio.sleep(0.1)
        return self.cart
    
    async def clear_cart(self) -> bool:
        """Clear all items from the cart."""
        await asyncio.sleep(0.1)
        self.cart.items = []
        self.cart.total_price = 0.0
        return True
    
    async def find_ingredient_products(self, ingredient_name: str, quantity: float, unit: str) -> List[ContosoProduct]:
        """Find products that match a cooking ingredient."""
        # Enhanced search for cooking ingredients
        search_terms = [
            ingredient_name,
            ingredient_name.replace(" ", ""),
            ingredient_name.split()[0] if " " in ingredient_name else ingredient_name
        ]
        
        all_results = []
        for term in search_terms:
            results = await self.search_products(term)
            all_results.extend(results)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for product in all_results:
            if product.id not in seen:
                seen.add(product.id)
                unique_results.append(product)
        
        return unique_results[:5]  # Return top 5 matches


# Singleton instance for global use
_contoso_service: Optional[ContosoAPIService] = None


def get_contoso_service(api_key: str = "mock_key", base_url: str = "https://api.contoso.com/v1") -> ContosoAPIService:
    """Get or create the Contoso API service instance."""
    global _contoso_service
    if _contoso_service is None:
        _contoso_service = ContosoAPIService(api_key, base_url)
    return _contoso_service
