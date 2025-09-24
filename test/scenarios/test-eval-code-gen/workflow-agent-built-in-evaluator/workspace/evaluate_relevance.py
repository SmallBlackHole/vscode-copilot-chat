"""
Evaluation script to measure relevance of agent responses to user queries.

This script uses Azure AI Evaluation SDK to evaluate response relevance using
the built-in RelevanceEvaluator with a GitHub-hosted model.
"""
import os
import json
from pathlib import Path

from azure.ai.evaluation import evaluate, RelevanceEvaluator, OpenAIModelConfiguration


def load_github_token():
    """Load GitHub token from .env file"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    return line.split("=", 1)[1].strip()
    
    # Fallback to environment variable
    return os.environ.get("GITHUB_TOKEN")


def setup_model_configuration():
    """Configure OpenAI model to use GitHub-hosted models"""
    github_token = load_github_token()
    if not github_token:
        raise ValueError("GITHUB_TOKEN not found in .env file or environment variables")
    
    # Use GitHub Models endpoint with gpt-4.1-mini for cost-effective evaluation
    model_config = OpenAIModelConfiguration(
        type="openai",
        model="openai/gpt-4.1-mini",  # GitHub-hosted model
        base_url="https://models.github.ai/inference",
        api_key=github_token
    )
    
    return model_config


def run_evaluation():
    """Run relevance evaluation on the dataset"""
    
    # Set up paths
    workspace_dir = Path(__file__).parent
    dataset_path = workspace_dir / "dataset.jsonl"
    output_path = workspace_dir / "evaluation_results"
    
    # Ensure dataset exists
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    # Set up model configuration
    print("Setting up model configuration...")
    model_config = setup_model_configuration()
    
    # Create RelevanceEvaluator
    print("Creating RelevanceEvaluator...")
    relevance_evaluator = RelevanceEvaluator(model_config=model_config)
    
    # Run evaluation using the evaluate() API
    print("Running evaluation...")
    print(f"Dataset: {dataset_path}")
    print(f"Output: {output_path}")
    
    result = evaluate(
        data=str(dataset_path),
        evaluators={
            "relevance": relevance_evaluator
        },
        evaluator_config={
            "relevance": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}"
                }
            }
        },
        output_path=str(output_path)
    )
    
    print("Evaluation completed!")
    print(f"Results saved to: {output_path}")
    
    # Print summary metrics
    if hasattr(result, 'metrics') and result.metrics:
        print("\n=== EVALUATION SUMMARY ===")
        for metric_name, metric_value in result.metrics.items():
            if isinstance(metric_value, (int, float)):
                print(f"{metric_name}: {metric_value:.4f}")
            else:
                print(f"{metric_name}: {metric_value}")
    
    return result


def display_detailed_results():
    """Display detailed evaluation results"""
    output_path = Path(__file__).parent / "evaluation_results"
    
    # Look for evaluation output files
    if output_path.exists():
        # Check for evaluation_result.json
        result_file = output_path / "evaluation_result.json"
        if result_file.exists():
            print("\n=== DETAILED RESULTS ===")
            with open(result_file) as f:
                results = json.load(f)
                
            # Display metrics
            if "metrics" in results:
                print("\nMetrics:")
                for key, value in results["metrics"].items():
                    if isinstance(value, (int, float)):
                        print(f"  {key}: {value:.4f}")
                    else:
                        print(f"  {key}: {value}")
            
            # Display individual scores
            if "rows" in results:
                print(f"\nIndividual Evaluation Results ({len(results['rows'])} items):")
                for i, row in enumerate(results["rows"], 1):
                    print(f"\nItem {i}:")
                    if "inputs.query" in row:
                        print(f"  Query: {row['inputs.query'][:100]}...")
                    if "inputs.response" in row:
                        print(f"  Response: {row['inputs.response'][:100]}...")
                    if "outputs.relevance.relevance" in row:
                        print(f"  Relevance Score: {row['outputs.relevance.relevance']}")
                    if "outputs.relevance.relevance_reason" in row:
                        print(f"  Reasoning: {row['outputs.relevance.relevance_reason']}")


if __name__ == "__main__":
    try:
        # Run the evaluation
        result = run_evaluation()
        
        # Display detailed results
        display_detailed_results()
        
        print("\n=== EVALUATION COMPLETE ===")
        print("Relevance evaluation has been successfully completed.")
        print("Check the 'evaluation_results' folder for detailed output files.")
        
    except Exception as e:
        print(f"Error running evaluation: {str(e)}")
        raise