# AI Joke Teller Console App

A simple console application that uses AI to generate jokes about user-specified topics. This app demonstrates how to integrate GitHub Models (AI) into a console application.

## Features

- 🎭 Generate AI-powered jokes on any topic
- 🔄 Interactive console interface
- 🛡️ Family-friendly, clean humor
- 💰 Cost-effective using GitHub Models (free tier available)
- ⚡ Fast response using GPT-4.1-mini model

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get GitHub Personal Access Token

1. Go to [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "AI Joke Teller"
4. Select the `read:packages` scope (required for GitHub Models)
5. Click "Generate token"
6. Copy the token (you won't see it again!)

### 3. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace `your_github_personal_access_token_here` with your actual GitHub token:
   ```
   GITHUB_TOKEN=ghp_your_actual_token_here
   ```

### 4. Run the Application

```bash
python joke_teller.py
```

## Usage

1. Run the application
2. Enter any topic when prompted (e.g., "cats", "programming", "pizza")
3. Enjoy your AI-generated joke!
4. Type `quit` or `exit` to stop

### Example Session

```
🎭 Welcome to the AI Joke Teller! 🎭
I can tell jokes about any topic you'd like!
Type 'quit' or 'exit' to stop.

What topic would you like a joke about? cats

🤔 Thinking of a joke about 'cats'...

😄 Here's your joke:
Why don't cats play poker in the jungle? Because there are too many cheetahs!

--------------------------------------------------
What topic would you like a joke about? programming

🤔 Thinking of a joke about 'programming'...

😄 Here's your joke:
Why do programmers prefer dark mode? Because light attracts bugs!

--------------------------------------------------
What topic would you like a joke about? quit
Thanks for using the AI Joke Teller! Have a great day! 👋
```

## Technical Details

### Model Selection
- **Model**: OpenAI GPT-4.1-mini via GitHub Models
- **Why this model**: Cost-effective, fast, and perfect for creative text generation like jokes
- **Endpoint**: GitHub Models (https://models.github.ai)

### Architecture
- Simple Python console application
- Uses OpenAI SDK for API communication
- Environment-based configuration for security
- Error handling for robust operation

### Cost
- GitHub Models offers a **free tier** for getting started
- GPT-4.1-mini is one of the most cost-effective options
- No charges until you hit rate limits

## Customization

You can customize the application by:

1. **Changing the model**: Edit the `self.model` in `JokeTeller.__init__()`
2. **Adjusting creativity**: Modify the `temperature` parameter (0.0-1.0)
3. **Changing joke style**: Modify the system prompt in `generate_joke()`
4. **Adding joke categories**: Extend the prompt to include specific joke types

## Troubleshooting

### Common Issues

1. **"GITHUB_TOKEN not found"**
   - Make sure you created the `.env` file
   - Verify your token is correctly set in the `.env` file

2. **Authentication errors**
   - Check that your GitHub token has the correct permissions
   - Ensure the token hasn't expired

3. **API errors**
   - Check your internet connection
   - Verify GitHub Models service status

### Support
For issues with GitHub Models, check the [GitHub Models documentation](https://docs.github.com/en/github-models).

## License

This project is open source and available under the MIT License.