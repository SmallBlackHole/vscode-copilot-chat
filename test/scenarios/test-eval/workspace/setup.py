#!/usr/bin/env python3
"""
Setup script for the AI-Powered Cooking Plan Agent
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def setup_virtual_environment():
    """Set up Python virtual environment."""
    if Path(".venv").exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv .venv", "Creating virtual environment")


def activate_and_install_dependencies():
    """Activate virtual environment and install dependencies."""
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate && pip install -r requirements.txt"
    else:  # Unix/Linux/macOS
        activate_cmd = "source .venv/bin/activate && pip install -r requirements.txt"
    
    return run_command(activate_cmd, "Installing dependencies")


def setup_environment_file():
    """Set up the .env file if it doesn't exist."""
    if Path(".env").exists():
        print("✅ .env file already exists")
        return True
    
    if Path(".env.example").exists():
        print("📄 Creating .env file from template...")
        try:
            with open(".env.example", "r") as example:
                content = example.read()
            with open(".env", "w") as env_file:
                env_file.write(content)
            print("✅ .env file created")
            print("⚠️  Please edit .env file and add your API keys!")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ .env.example not found")
        return False


def main():
    """Main setup function."""
    print("🍳 AI-Powered Cooking Plan Agent Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Setup virtual environment
    if not setup_virtual_environment():
        return False
    
    # Install dependencies
    if not activate_and_install_dependencies():
        return False
    
    # Setup environment file
    if not setup_environment_file():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your API keys")
    print("   - Get a GitHub token from: https://github.com/settings/tokens")
    print("   - Or add your OpenAI API key")
    print("2. Activate the virtual environment:")
    if os.name == 'nt':
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("3. Run the app:")
    print("   python main.py")
    print("   or try the demo: python demo.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
