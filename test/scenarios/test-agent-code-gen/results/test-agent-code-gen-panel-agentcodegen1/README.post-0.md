# Recipe Recommendation Agent

An LLM-based AI agent that recommends recipes based on ingredients provided by users, built with Microsoft Agent Framework and GitHub models.

## Features

- 🥗 Ingredient-based recipe recommendations
- 🤖 Powered by Microsoft Agent Framework
- 🔄 Uses GitHub models with free tier
- 📱 Simple command-line interface
- 🎯 Customizable dietary preferences and restrictions

## Prerequisites

- Python 3.8+
- GitHub Personal Access Token (for GitHub models)

## Installation

1. Clone this repository or download the files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your GitHub Personal Access Token:
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Generate a new token with appropriate permissions
   - Set it as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_github_token_here
   ```

## Usage

### Basic Usage

```bash
python recipe_agent.py
```

### Example Interaction

```
Recipe Recommendation Agent
===========================

What ingredients do you have? chicken, rice, broccoli

🤖 Based on your ingredients (chicken, rice, broccoli), here are some delicious recipe recommendations:

1. **Chicken and Broccoli Rice Bowl**
   - A healthy one-bowl meal with seasoned chicken, steamed broccoli, and fluffy rice
   - Cook time: 25 minutes
   - Difficulty: Easy

2. **Chicken Fried Rice with Broccoli**
   - Classic fried rice with diced chicken and fresh broccoli florets
   - Cook time: 20 minutes
   - Difficulty: Easy

Would you like detailed instructions for any of these recipes? (y/n)
```

### Configuration

You can customize the agent by modifying `config.py`:

- Model selection (default: gpt-4o-mini for cost efficiency)
- Dietary restrictions
- Cuisine preferences
- Recipe complexity level

## Project Structure

```
recipe-agent/
├── recipe_agent.py          # Main agent application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .env.example           # Environment variables template
└── examples/
    └── sample_recipes.py   # Example usage and sample outputs
```

## Model Information

This agent uses GitHub models for cost-effective development:

- **Default Model**: `openai/gpt-4o-mini` - Affordable and efficient for recipe generation
- **Alternative**: `openai/gpt-4o` - Higher quality for more complex recipe requests
- **Reasoning Model**: `openai/o1-mini` - For complex dietary requirement analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section below
- Open an issue on GitHub
- Review the Microsoft Agent Framework documentation

## Troubleshooting

### Common Issues

1. **Authentication Error**: Ensure your GitHub token is correctly set
2. **Model Not Available**: Check if the model is available in your region
3. **Rate Limiting**: GitHub models have free tier limits; consider upgrading if needed

### Debug Mode

Run with debug logging:
```bash
python recipe_agent.py --debug
```