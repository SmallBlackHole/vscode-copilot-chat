# AI-Powered Cooking Plan Agent - Project Structure

## 📁 Project Layout

```
myCooking/
├── 📄 main.py                    # Main console application entry point
├── 📄 demo.py                    # Quick demo script with pre-configured settings
├── 📄 setup.py                   # Automated setup script
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # Project documentation
├── 📄 .env.example               # Environment variables template
├── 📄 .gitignore                 # Git ignore rules
│
├── 📁 agents/                    # AI agent definitions
│   ├── 📄 __init__.py
│   └── 📄 cooking_agents.py      # Specialized cooking agents
│
├── 📁 models/                    # Data models and schemas
│   └── 📄 __init__.py            # Pydantic models for recipes, ingredients, etc.
│
├── 📁 services/                  # External service integrations
│   ├── 📄 __init__.py
│   └── 📄 contoso_api.py         # Mock Contoso API service
│
├── 📁 utils/                     # Helper utilities
│   ├── 📄 __init__.py
│   └── 📄 console_formatter.py   # Rich console formatting
│
└── 📁 .vscode/                   # VS Code configuration
    └── 📄 tasks.json             # Build and run tasks
```

## 🤖 Agent Architecture

### Main Coordinator Agent
- **Role**: Orchestrates the entire cooking planning process
- **Capabilities**: User interaction, workflow coordination, final summaries

### Specialized Agents
1. **Cooking Planner Agent**
   - Generates detailed recipes based on preferences
   - Considers dietary restrictions, skill level, time constraints
   - Provides cooking tips and techniques

2. **Pantry Analyzer Agent**
   - Compares required vs. available ingredients
   - Identifies missing items for shopping
   - Suggests ingredient substitutions

3. **Shopping Assistant Agent**
   - Searches Contoso product catalog
   - Finds best products for ingredients
   - Automatically adds items to shopping cart

## 🛠️ Technologies Used

- **OpenAI Agents SDK**: Agent orchestration and tool calling
- **GPT-4.1**: Advanced reasoning model (via GitHub Models or OpenAI)
- **Rich**: Beautiful console output and formatting
- **Pydantic**: Data validation and type safety
- **asyncio**: Asynchronous programming for API calls

## 🔧 Key Features

### Smart Recipe Generation
- AI-powered recipe creation based on user preferences
- Considers dietary restrictions, cooking time, and skill level
- Provides detailed ingredients list and step-by-step instructions

### Intelligent Pantry Management
- Analyzes available vs. required ingredients
- Smart matching (e.g., "garlic powder" matches "garlic")
- Suggests substitutions when items are missing

### Automated Shopping
- Searches Contoso catalog for missing ingredients
- Finds best products based on price, rating, and availability
- Automatically adds items to shopping cart
- Provides total cost calculation

### Rich Console Experience
- Colorful, formatted output using Rich library
- Progress indicators and status updates
- Interactive prompts and confirmations
- Professional tables and panels

## 🚀 Quick Start

1. **Setup**: Run `python setup.py`
2. **Configure**: Edit `.env` with your API keys
3. **Run**: Execute `python main.py` or try `python demo.py`

## 🎯 Usage Patterns

### Interactive Mode
```bash
python main.py
```
Full interactive experience with user input prompts.

### Demo Mode
```bash
python demo.py
```
Pre-configured demonstration with sample data.

### VS Code Integration
- Use Ctrl+Shift+P → "Tasks: Run Task"
- Select "Run Cooking Agent" or "Run Demo"

## 🔍 Observability

- **Logging**: Rich console output with different log levels
- **Error Handling**: Graceful error reporting and recovery

## 🛡️ Best Practices Implemented

- **Agent Design**: Following OpenAI Agents SDK patterns
- **Model Selection**: Using GPT-4.1 for advanced reasoning
- **Type Safety**: Pydantic models for data validation
- **Async Programming**: Non-blocking API calls
- **Error Handling**: Comprehensive error management
- **User Experience**: Rich, interactive console interface
