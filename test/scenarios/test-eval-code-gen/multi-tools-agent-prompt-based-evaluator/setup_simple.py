#!/usr/bin/env python3
"""
Setup script to install dependencies and run the weather-time coordination evaluation.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    return True

def check_github_token():
    """Check if GitHub token is available."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN environment variable not set")
        print("  Please set your GitHub Personal Access Token:")
        print("  export GITHUB_TOKEN=your_github_token_here")
        return False
    else:
        print("GitHub token found")
        return True

def main():
    print("Setting up Weather-Time Coordination Evaluation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("workspace/dataset.json"):
        print("Error: dataset.json not found in workspace/ directory")
        print("  Please run this script from the correct directory")
        sys.exit(1)
    
    print("Dataset found")
    
    # Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Check GitHub token
    has_token = check_github_token()
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    
    if has_token:
        print("\nTo run the evaluation:")
        print("  python evaluate_weather_time_coordination.py")
    else:
        print("\nBefore running the evaluation:")
        print("  1. Set your GitHub token: export GITHUB_TOKEN=your_token")
        print("  2. Run: python evaluate_weather_time_coordination.py")

if __name__ == "__main__":
    main()