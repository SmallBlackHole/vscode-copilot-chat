# AI Joke Teller Console App

A simple console application that tells jokes about any given topic using AI. Built with the Microsoft Agent Framework and GitHub models for cost-effective, high-quality joke generation.

## Features

- 🎭 AI-powered joke generation on any topic
- 💰 Cost-effective using GitHub models (free tier available)
- 🎯 Interactive mode for continuous joke telling
- 📝 Command-line mode for single jokes
- 🛡️ Family-friendly content filtering
- 🚀 Fast response times with optimized models

## Setup

### 1. Install Dependencies

First, create a virtual environment and install the required packages:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt --constraint constraints.txt
```

### 2. Get GitHub Personal Access Token

You need a GitHub Personal Access Token to access GitHub models:

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "AI Joke Teller"
4. Select appropriate scopes (no special scopes needed for model access)
5. Click "Generate token"
6. Copy the token (you won't see it again!)

### 3. Set Environment Variable (Optional)

You can set your GitHub token as an environment variable:

```bash
# Linux/Mac:
export GITHUB_TOKEN="your_github_token_here"

# Windows (Command Prompt):
set GITHUB_TOKEN=your_github_token_here

# Windows (PowerShell):
$env:GITHUB_TOKEN="your_github_token_here"
```

## Usage

### Interactive Mode

Run the app without arguments for interactive mode:

```bash
python joke_teller.py
```

This will start an interactive session where you can:
- Enter any topic to get jokes about
- Type 'quit', 'exit', or 'bye' to stop
- Get multiple jokes by continuing the conversation

### Single Joke Mode

Pass a topic as command-line arguments for a single joke:

```bash
python joke_teller.py programming
python joke_teller.py "artificial intelligence"
python joke_teller.py cats and dogs
```

## Example Output

```
🎭 AI Joke Teller - Powered by Microsoft Agent Framework & GitHub Models
======================================================================

🎭 AI Joke Teller initialized successfully!
💡 Using model: openai/gpt-4.1-mini

🎪 Welcome to the AI Joke Teller!
📝 Enter any topic and I'll tell you a joke about it.
💬 Type 'quit', 'exit', or 'bye' to stop.

🎯 What topic would you like a joke about? programming
🤔 Thinking of a joke...

😂 Here's your joke:
Why do programmers prefer dark mode?

Because light attracts bugs! 🐛

And here's a bonus one:
How many programmers does it take to change a light bulb?
None. That's a hardware problem!

--------------------------------------------------
🎯 What topic would you like a joke about? quit
👋 Thanks for using AI Joke Teller! Have a great day!
```

## Model Options

The app supports various GitHub models:

- **openai/gpt-4.1-mini** (default) - Fast, cost-effective, great for jokes
- **openai/gpt-4.1** - More capable, higher quality responses
- **openai/gpt-4o-mini** - Multimodal capabilities
- And many more available on GitHub models

## Project Structure

```
ai-joke-teller/
├── joke_teller.py          # Main application
├── requirements.txt        # Python dependencies
├── constraints.txt         # Version constraints
└── README.md              # This file
```

## How It Works

1. **Agent Framework**: Uses Microsoft Agent Framework for structured AI interactions
2. **GitHub Models**: Leverages GitHub's model endpoint for cost-effective AI access
3. **Specialized Instructions**: The AI agent is specifically instructed to create family-friendly, creative jokes
4. **Error Handling**: Robust error handling for network issues and API problems

## Customization

You can customize the joke teller by modifying the agent instructions in `joke_teller.py`:

```python
instructions="""You are a witty and family-friendly comedian AI. 
Your job is to tell creative, clean, and funny jokes about any topic the user provides.
# Add your custom instructions here...
"""
```

## Troubleshooting

### Common Issues

1. **"GitHub token is required"**
   - Make sure you've set the `GITHUB_TOKEN` environment variable or enter it when prompted

2. **"Error initializing joke teller"**
   - Check your internet connection
   - Verify your GitHub token is valid
   - Ensure the model ID is correct

3. **"Rate limit exceeded"**
   - GitHub models have rate limits on the free tier
   - Wait a moment before trying again
   - Consider upgrading to a paid plan for higher limits

### Getting Help

- Check the [Microsoft Agent Framework documentation](https://github.com/microsoft/agent-framework)
- Review [GitHub Models documentation](https://docs.github.com/en/github-models)
- Ensure all dependencies are properly installed

## License

This project is open source. Feel free to modify and distribute as needed.

---

Enjoy your AI-powered jokes! 🎭✨