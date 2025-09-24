#!/usr/bin/env python3
"""
Agent Response Length Evaluation using Azure AI Evaluation SDK.

This script evaluates agent responses by measuring their length characteristics
using a custom ResponseLengthEvaluator and the Azure AI Evaluation SDK.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Import Azure AI Evaluation SDK components
from azure.ai.evaluation import evaluate

# Import our custom evaluator
from response_length_evaluator import ResponseLengthEvaluator


def setup_model_configuration():
    """
    Set up model configuration for GitHub-hosted models.
    
    Returns:
        dict: Model configuration for Azure AI Evaluation SDK
    """
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN not found in environment variables. Please set it in .env file.")
    
    # Configure GitHub-hosted model
    model_config = {
        "type": "openai",  # Type is required for OpenAI-compatible endpoints
        "model": "gpt-4.1-mini",  # Cost-effective model for evaluation
        "base_url": "https://models.github.ai/inference",  # GitHub models endpoint
        "api_key": github_token
    }
    
    return model_config


def run_response_length_evaluation():
    """
    Run the response length evaluation using Azure AI Evaluation SDK.
    
    This function:
    1. Sets up the model configuration
    2. Creates the custom response length evaluator
    3. Runs the evaluation using the evaluate() API
    4. Saves results and prints summary
    """
    
    print("Starting Agent Response Length Evaluation")
    print("=" * 50)
    
    # Setup model configuration
    try:
        model_config = setup_model_configuration()
        print("Model configuration set up successfully")
        print(f"   Model: {model_config['model']}")
        print(f"   Endpoint: {model_config['base_url']}")
    except Exception as e:
        print(f"Error setting up model configuration: {e}")
        return
    
    # Create custom evaluator
    response_length_evaluator = ResponseLengthEvaluator()
    print("Response Length Evaluator created")
    
    # Check if evaluation data exists
    data_file = "evaluation_data.jsonl"
    if not Path(data_file).exists():
        print(f"Evaluation data file '{data_file}' not found.")
        print("   Please run convert_data.py first to create the JSONL file.")
        return
    
    print(f"Found evaluation data: {data_file}")
    
    # Run evaluation using Azure AI Evaluation SDK
    print("\nRunning evaluation...")
    
    try:
        result = evaluate(
            data=data_file,
            evaluators={
                "response_length": response_length_evaluator
            },
            evaluator_config={
                "response_length": {
                    "column_mapping": {
                        "response": "${data.response}"
                    }
                }
            },
            # Save results to output file
            output_path="./evaluation_results.json",
            # Add tags for tracking
            tags={
                "experiment": "response_length_evaluation",
                "model": "custom_length_evaluator",
                "dataset": "agent_workflow_responses",
                "environment": "development"
            }
        )
        
        print("Evaluation completed successfully!")
        
        # Print summary results
        print("\nEvaluation Summary:")
        print("=" * 30)
        
        # Extract metrics from result
        if hasattr(result, 'metrics') and result.metrics:
            metrics = result.metrics
            print("\nAggregate Metrics:")
            for metric_name, metric_value in metrics.items():
                print(f"   {metric_name}: {metric_value}")
        
        # Count total rows evaluated
        if hasattr(result, 'rows') and result.rows:
            print(f"\nEvaluated {len(result.rows)} responses")
            
            # Show sample of individual results
            print("\nSample Individual Results:")
            for i, row in enumerate(result.rows[:2]):  # Show first 2 results
                print(f"\n   Response {i+1}:")
                if hasattr(row, 'outputs') and row.outputs:
                    outputs = row.outputs
                    if 'response_length.response_char_count' in outputs:
                        char_count = outputs['response_length.response_char_count']
                        word_count = outputs.get('response_length.response_word_count', 'N/A')
                        category = outputs.get('response_length.response_length_category', 'N/A')
                        print(f"     Characters: {char_count}")
                        print(f"     Words: {word_count}")
                        print(f"     Category: {category}")
        
        print(f"\nDetailed results saved to: evaluation_results.json")
        
        return result
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        print(f"   Error type: {type(e).__name__}")
        return None


def main():
    """Main execution function."""
    
    print("Agent Response Length Evaluation Tool")
    print("Using Azure AI Evaluation SDK with Custom Evaluator")
    print("=" * 60)
    
    # Run the evaluation
    result = run_response_length_evaluation()
    
    if result:
        print("\nEvaluation completed successfully!")
        print("   Check evaluation_results.json for detailed results.")
    else:
        print("\nEvaluation failed. Please check the error messages above.")


if __name__ == "__main__":
    main()