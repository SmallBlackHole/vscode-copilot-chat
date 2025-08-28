# AI-Powered Cooking Plan Agent

An intelligent console application that helps you plan meals and automatically handles shopping for missing ingredients.

## Features

- **Smart Meal Planning**: AI agent analyzes your recipes and cooking preferences
- **Ingredient Management**: Automatically identifies missing ingredients from your pantry
- **Smart Shopping**: Integrates with Contoso product catalog to find and add items to cart
- **Interactive Console**: Rich, colorful command-line interface

## Setup

1. Create and activate a Python virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your API configuration:
```
# GitHub Models API (free tier)
GITHUB_TOKEN=your_github_token_here
API_BASE_URL=https://models.github.ai/inference/

# Or use OpenAI directly
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
python main.py
```

## Usage

1. **Start the App**: Run `python main.py`
2. **Create Cooking Plan**: Describe what you want to cook
3. **Review Ingredients**: Agent will analyze required vs available ingredients
4. **Auto-Shopping**: Missing items are automatically found and added to your Contoso cart
5. **Cook Away**: Follow the optimized cooking plan!

## Project Structure

- `main.py` - Main console application entry point
- `agents/` - AI agent definitions
- `services/` - External service integrations (Contoso API)
- `models/` - Data models and schemas
- `utils/` - Helper utilities and formatting

## Technologies

- **OpenAI Agents SDK** - For intelligent agent orchestration
- **GPT-4.1** - Advanced reasoning and planning capabilities
- **Rich** - Beautiful console output and formatting
- **Pydantic** - Data validation and models
