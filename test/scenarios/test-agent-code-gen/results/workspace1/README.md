# Weather Agent

A simple weather agent built with the Microsoft Agent Framework that can retrieve weather information for any city using GitHub models.

## Features

- 🌤️ **Real Weather Data**: Uses OpenWeatherMap API for accurate weather information
- 🎲 **Simulated Weather**: Fallback to simulated data for testing or when API is unavailable
- 🔄 **Multi-turn Conversations**: Maintains context across multiple queries
- 📅 **Weather Forecasts**: Provides multi-day weather forecasts
- 🤖 **AI-Powered**: Uses GitHub models (GPT-4.1-mini) for natural language processing

## Setup

### 1. Install Dependencies

First, create a virtual environment and install the required packages:

```bash
# Create virtual environment
python -m venv weather-agent-env

# Activate virtual environment
# On Windows:
weather-agent-env\Scripts\activate
# On macOS/Linux:
source weather-agent-env/bin/activate

# Install dependencies
pip install -r requirements.txt --constraint constraints.txt
```

### 2. Environment Configuration

Copy the `.env` file and update it with your credentials:

```bash
# Copy the example environment file
cp .env .env.local
```

Update the `.env` file with your credentials:

```env
# Required: GitHub Personal Access Token for accessing GitHub models
GITHUB_TOKEN=your_github_token_here

# Optional: OpenWeatherMap API Key for real weather data
WEATHER_API_KEY=your_openweathermap_api_key_here

# Model configuration
MODEL_ID=openai/gpt-4.1-mini
```

#### Getting a GitHub Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "Weather Agent"
4. Select the appropriate scopes (for GitHub models, basic access is sufficient)
5. Copy the generated token to your `.env` file

#### Getting an OpenWeatherMap API Key (Optional)

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add it to your `.env` file

If you don't provide a weather API key, the agent will use simulated weather data.

## Usage

### Basic Usage

Run the weather agent:

```bash
python weather_agent.py
```

The agent will start in interactive mode where you can ask weather questions like:
- "What's the weather like in London?"
- "How's the weather in Tokyo today?"
- "Can you give me a 5-day forecast for New York?"

### Using in Your Code

```python
import asyncio
from weather_agent import WeatherAgent

async def example():
    # Create weather agent
    agent = WeatherAgent(use_real_weather=True)  # Set to False for simulated data
    
    # Get weather for a specific city
    weather = await agent.get_weather("Paris")
    print(weather)
    
    # Have a conversation
    thread = agent.get_new_thread()
    response = await agent.chat("What's the weather like in Seattle?", thread=thread)
    print(response)
    
    # Follow-up question (maintains context)
    response2 = await agent.chat("What about tomorrow?", thread=thread)
    print(response2)

# Run the example
asyncio.run(example())
```

## Project Structure

```
weather-agent/
├── weather_agent.py      # Main agent implementation
├── weather_tools.py      # Weather data retrieval tools
├── requirements.txt      # Python dependencies
├── constraints.txt       # Version constraints
├── .env                  # Environment variables (copy and configure)
└── README.md            # This file
```

## How It Works

1. **Agent Framework**: Uses Microsoft Agent Framework to create an AI agent
2. **GitHub Models**: Leverages GitHub's hosted AI models for natural language understanding
3. **Function Calling**: The agent can call weather functions to retrieve real data
4. **Context Management**: Maintains conversation context across multiple interactions

## Available Models

The agent uses GitHub models by default. You can change the model by updating the `MODEL_ID` in your `.env` file. Some available options:

- `openai/gpt-4.1-mini` (default) - Fast and cost-effective
- `openai/gpt-4.1` - More capable for complex queries
- `openai/gpt-4o-mini` - Multimodal capabilities
- `microsoft/phi-4-mini-instruct` - Smaller, efficient model

## Troubleshooting

### Common Issues

1. **Missing GitHub Token**: Make sure you've set `GITHUB_TOKEN` in your `.env` file
2. **Installation Issues**: Ensure you're using Python 3.10 or later
3. **Network Issues**: The agent requires internet access to reach GitHub models and weather APIs

### Error Messages

- `GITHUB_TOKEN environment variable is required`: Add your GitHub token to `.env`
- `Error fetching weather data`: Check your `WEATHER_API_KEY` or use simulated mode
- `Model not found`: Verify your `MODEL_ID` is correct and available

## Extending the Agent

You can easily extend the agent with additional tools:

```python
# Add to weather_tools.py
def get_air_quality(location: str) -> str:
    """Get air quality information for a location."""
    # Implementation here
    pass

# Add to agent tools in weather_agent.py
self.agent = ChatAgent(
    # ... other parameters
    tools=[weather_function, get_weather_forecast, get_air_quality],
)
```

## License

This project is open source and available under the MIT License.