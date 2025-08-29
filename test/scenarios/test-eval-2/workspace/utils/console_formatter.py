from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.align import Align
from typing import List, Dict, Any
from models import Recipe, Ingredient, ContosoProduct, ShoppingCart, CookingPlan
import time


class ConsoleFormatter:
    """Rich console formatting utilities for the cooking app."""
    
    def __init__(self):
        self.console = Console()
    
    def print_welcome(self):
        """Display welcome message and app title."""
        title = Text("🍳 AI-Powered Cooking Plan Agent", style="bold magenta")
        subtitle = Text("Your intelligent cooking companion", style="dim italic")
        
        welcome_panel = Panel(
            Align.center(f"{title}\n{subtitle}"),
            border_style="bright_blue",
            padding=(1, 2)
        )
        
        self.console.print(welcome_panel)
        self.console.print()
    
    def print_section_header(self, title: str, emoji: str = "✨"):
        """Print a section header with styling."""
        header_text = Text(f"{emoji} {title}", style="bold cyan")
        self.console.print(header_text)
        self.console.print("─" * len(f"{emoji} {title}"), style="cyan")
        self.console.print()
    
    def print_recipe(self, recipe: Recipe):
        """Display a recipe in a formatted table."""
        # Recipe header
        recipe_panel = Panel(
            f"[bold green]{recipe.name}[/bold green]\n"
            f"[dim]{recipe.description}[/dim]\n\n"
            f"🍽️  Servings: {recipe.servings} | "
            f"⏱️  Prep: {recipe.prep_time_minutes}m | "
            f"🔥 Cook: {recipe.cook_time_minutes}m | "
            f"📊 Difficulty: {recipe.difficulty.title()}",
            border_style="green"
        )
        self.console.print(recipe_panel)
        
        # Ingredients table
        ingredients_table = Table(title="🥗 Ingredients", show_header=True, header_style="bold blue")
        ingredients_table.add_column("Ingredient", style="cyan", width=30)
        ingredients_table.add_column("Quantity", justify="right", style="magenta", width=10)
        ingredients_table.add_column("Unit", style="yellow", width=12)
        ingredients_table.add_column("Category", style="green", width=15)
        
        for ingredient in recipe.ingredients:
            ingredients_table.add_row(
                ingredient.name,
                str(ingredient.quantity),
                ingredient.unit.value,
                ingredient.category
            )
        
        self.console.print(ingredients_table)
        self.console.print()
        
        # Instructions
        if recipe.instructions:
            self.console.print("[bold blue]📋 Instructions:[/bold blue]")
            for i, instruction in enumerate(recipe.instructions, 1):
                self.console.print(f"[dim]{i}.[/dim] {instruction}")
            self.console.print()
        
        # Tips
        if recipe.tips:
            self.console.print("[bold yellow]💡 Tips:[/bold yellow]")
            for tip in recipe.tips:
                self.console.print(f"• {tip}")
            self.console.print()
    
    def print_ingredients_comparison(self, required: List[Ingredient], missing: List[Ingredient]):
        """Display comparison of required vs missing ingredients."""
        comparison_table = Table(title="🔍 Ingredient Analysis", show_header=True, header_style="bold blue")
        comparison_table.add_column("Ingredient", style="cyan", width=25)
        comparison_table.add_column("Required", justify="right", style="magenta", width=12)
        comparison_table.add_column("Status", style="bold", width=15)
        comparison_table.add_column("Action", style="yellow", width=20)
        
        missing_names = {ing.name.lower() for ing in missing}
        
        for ingredient in required:
            status = "❌ Missing" if ingredient.name.lower() in missing_names else "✅ Available"
            action = "Need to buy" if ingredient.name.lower() in missing_names else "In pantry"
            status_style = "red" if ingredient.name.lower() in missing_names else "green"
            
            comparison_table.add_row(
                ingredient.name,
                f"{ingredient.quantity} {ingredient.unit.value}",
                f"[{status_style}]{status}[/{status_style}]",
                action
            )
        
        self.console.print(comparison_table)
        self.console.print()
    
    def print_products_search_results(self, products: List[ContosoProduct], ingredient_name: str):
        """Display search results for products."""
        if not products:
            self.console.print(f"[red]❌ No products found for '{ingredient_name}'[/red]")
            return
        
        products_table = Table(
            title=f"🛒 Contoso Products for '{ingredient_name}'", 
            show_header=True, 
            header_style="bold blue"
        )
        products_table.add_column("ID", style="dim", width=8)
        products_table.add_column("Product", style="cyan", width=25)
        products_table.add_column("Brand", style="green", width=15)
        products_table.add_column("Size", style="yellow", width=12)
        products_table.add_column("Price", justify="right", style="magenta", width=10)
        products_table.add_column("Rating", justify="center", style="bright_yellow", width=8)
        
        for product in products:
            rating_stars = "⭐" * int(product.rating) + "☆" * (5 - int(product.rating))
            products_table.add_row(
                product.id,
                product.name,
                product.brand,
                product.size,
                f"${product.price:.2f}",
                f"{product.rating:.1f}"
            )
        
        self.console.print(products_table)
        self.console.print()
    
    def print_shopping_cart(self, cart: ShoppingCart):
        """Display the current shopping cart."""
        if not cart.items:
            self.console.print("[yellow]🛒 Your cart is empty[/yellow]")
            return
        
        cart_table = Table(title="🛒 Your Contoso Shopping Cart", show_header=True, header_style="bold blue")
        cart_table.add_column("Product", style="cyan", width=30)
        cart_table.add_column("Quantity", justify="right", style="magenta", width=10)
        cart_table.add_column("Unit Price", justify="right", style="yellow", width=12)
        cart_table.add_column("Total", justify="right", style="bold green", width=12)
        
        for item in cart.items:
            total_price = item.product.price * item.quantity
            cart_table.add_row(
                f"{item.product.name} ({item.product.brand})",
                str(item.quantity),
                f"${item.product.price:.2f}",
                f"${total_price:.2f}"
            )
        
        cart_table.add_row(
            "[bold]TOTAL[/bold]",
            "",
            "",
            f"[bold green]${cart.total_price:.2f}[/bold green]"
        )
        
        self.console.print(cart_table)
        self.console.print()
    
    def print_cooking_plan_summary(self, plan: CookingPlan):
        """Display a summary of the cooking plan."""
        summary_panel = Panel(
            f"[bold green]{plan.name}[/bold green]\n\n"
            f"📝 Recipes: {len(plan.recipes)}\n"
            f"🍽️  Total Servings: {plan.total_servings}\n"
            f"⏱️  Total Prep Time: {plan.total_prep_time} minutes\n"
            f"🔥 Total Cook Time: {plan.total_cook_time} minutes\n"
            f"🥗 Total Ingredients: {len(plan.all_ingredients)}\n"
            f"🛒 Missing Items: {len(plan.missing_ingredients)}",
            border_style="green",
            title="📋 Cooking Plan Summary"
        )
        self.console.print(summary_panel)
        self.console.print()
    
    def show_progress(self, description: str, total_steps: int = None):
        """Show a progress spinner or bar."""
        if total_steps:
            return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            )
        else:
            # Simple spinner for unknown duration tasks
            self.console.print(f"[yellow]⏳ {description}...[/yellow]")
    
    def prompt_user_input(self, prompt_text: str, default: str = None) -> str:
        """Get user input with rich prompt."""
        return Prompt.ask(f"[bold cyan]{prompt_text}[/bold cyan]", default=default)
    
    def prompt_confirmation(self, question: str) -> bool:
        """Get yes/no confirmation from user."""
        return Confirm.ask(f"[bold yellow]{question}[/bold yellow]")
    
    def print_error(self, message: str):
        """Print error message with styling."""
        self.console.print(f"[bold red]❌ Error: {message}[/bold red]")
    
    def print_success(self, message: str):
        """Print success message with styling."""
        self.console.print(f"[bold green]✅ {message}[/bold green]")
    
    def print_info(self, message: str):
        """Print info message with styling."""
        self.console.print(f"[blue]ℹ️  {message}[/blue]")
    
    def print_warning(self, message: str):
        """Print warning message with styling."""
        self.console.print(f"[yellow]⚠️  {message}[/yellow]")


# Global console formatter instance
console_formatter = ConsoleFormatter()
