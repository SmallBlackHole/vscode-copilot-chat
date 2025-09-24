# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import json
import pandas as pd
from typing import Dict, Any
from azure.ai.evaluation import evaluate, OpenAIModelConfiguration
from review_evaluators import (
    ReviewConstructivenessEvaluator,
    ReviewActionabilityEvaluator, 
    ReviewQualityEvaluator
)

def setup_model_configuration() -> OpenAIModelConfiguration:
    """
    Set up the model configuration for GitHub models.
    
    :return: Configured model for evaluation
    :rtype: OpenAIModelConfiguration
    """
    # Check if GitHub token is available
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Warning: GITHUB_TOKEN environment variable not set.")
        print("Please set your GitHub Personal Access Token to use GitHub models.")
        print("You can generate one at: https://github.com/settings/tokens")
        
        # Fallback to prompt for token
        github_token = input("Enter your GitHub token (or press Enter to skip): ").strip()
        if not github_token:
            raise ValueError("GitHub token is required to use GitHub models")
    
    # Configure GitHub models access
    model_config = OpenAIModelConfiguration(
        type="openai",
        model="gpt-4.1-mini",  # Cost-effective model for evaluation
        base_url="https://models.github.ai/inference",
        api_key=github_token
    )
    
    print(f"✅ Model configuration set up successfully")
    print(f"   Model: {model_config.model}")
    print(f"   Endpoint: {model_config.base_url}")
    
    return model_config


def create_evaluators(model_config: OpenAIModelConfiguration) -> Dict[str, Any]:
    """
    Create the evaluation evaluators.
    
    :param model_config: Model configuration to use
    :type model_config: OpenAIModelConfiguration
    :return: Dictionary of evaluators
    :rtype: Dict[str, Any]
    """
    evaluators = {
        "constructiveness": ReviewConstructivenessEvaluator(model_config=model_config),
        "actionability": ReviewActionabilityEvaluator(model_config=model_config),
        "overall_quality": ReviewQualityEvaluator(model_config=model_config)
    }
    
    print(f"✅ Created {len(evaluators)} evaluators")
    for name in evaluators.keys():
        print(f"   - {name}")
    
    return evaluators


def configure_column_mapping() -> Dict[str, Dict[str, str]]:
    """
    Configure the column mapping for evaluators.
    
    :return: Column mapping configuration
    :rtype: Dict[str, Dict[str, str]]
    """
    # Map JSONL columns to evaluator parameters
    column_mapping = {
        "default": {
            "original_content": "${data.original_content}",
            "reviewer_feedback": "${data.reviewer_feedback}"
        }
    }
    
    print("✅ Column mapping configured")
    print("   Mapping JSONL fields to evaluator parameters:")
    for key, value in column_mapping["default"].items():
        print(f"   - {key}: {value}")
    
    return column_mapping


def run_evaluation() -> Dict[str, Any]:
    """
    Run the review quality evaluation.
    
    :return: Evaluation results
    :rtype: Dict[str, Any]
    """
    print("🚀 Starting Review Quality Evaluation")
    print("=" * 50)
    
    # Set up model configuration
    model_config = setup_model_configuration()
    
    # Create evaluators
    evaluators = create_evaluators(model_config)
    
    # Configure column mapping
    evaluator_config = configure_column_mapping()
    
    # Check if data file exists
    data_file = "review_evaluation_data.jsonl"
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file '{data_file}' not found. Please run convert_dataset.py first.")
    
    print(f"✅ Using data file: {data_file}")
    
    # Run evaluation
    print("\n🔄 Running evaluation...")
    result = evaluate(
        data=data_file,
        evaluators=evaluators,
        evaluator_config=evaluator_config,
        output_path="review_evaluation_results.json"
    )
    
    print("✅ Evaluation completed successfully!")
    
    return result


def analyze_results(result: Dict[str, Any]) -> None:
    """
    Analyze and display the evaluation results.
    
    :param result: Evaluation results from the evaluate() function
    :type result: Dict[str, Any]
    """
    print("\n📊 EVALUATION RESULTS ANALYSIS")
    print("=" * 50)
    
    # Display metrics
    metrics = result.get("metrics", {})
    if metrics:
        print("\n🎯 OVERALL METRICS:")
        for metric_name, value in metrics.items():
            if isinstance(value, (int, float)):
                print(f"   {metric_name}: {value:.2f}")
            else:
                print(f"   {metric_name}: {value}")
    
    # Analyze individual results
    rows = result.get("rows", [])
    if rows:
        print(f"\n📝 INDIVIDUAL RESULTS ({len(rows)} reviews analyzed):")
        
        for i, row in enumerate(rows, 1):
            print(f"\n--- Review {i} ---")
            
            # Extract scores
            constructiveness = row.get("outputs.constructiveness.constructiveness", "N/A")
            actionability = row.get("outputs.actionability.actionability", "N/A")
            overall_quality = row.get("outputs.overall_quality.overall_quality", "N/A")
            
            print(f"Constructiveness: {constructiveness}")
            print(f"Actionability: {actionability}")
            print(f"Overall Quality: {overall_quality}")
            
            # Show reasoning if available
            constructiveness_reasoning = row.get("outputs.constructiveness.constructiveness_reasoning", "")
            if constructiveness_reasoning:
                print(f"Constructiveness Reasoning: {constructiveness_reasoning}")
            
            actionability_reasoning = row.get("outputs.actionability.actionability_reasoning", "")
            if actionability_reasoning:
                print(f"Actionability Reasoning: {actionability_reasoning}")
            
            overall_quality_reasoning = row.get("outputs.overall_quality.overall_quality_reasoning", "")
            if overall_quality_reasoning:
                print(f"Overall Quality Reasoning: {overall_quality_reasoning}")
    
    # Generate summary insights
    print(f"\n💡 INSIGHTS:")
    if rows:
        # Calculate averages
        constructiveness_scores = [
            row.get("outputs.constructiveness.constructiveness", 0) 
            for row in rows if row.get("outputs.constructiveness.constructiveness") is not None
        ]
        actionability_scores = [
            row.get("outputs.actionability.actionability", 0) 
            for row in rows if row.get("outputs.actionability.actionability") is not None
        ]
        overall_quality_scores = [
            row.get("outputs.overall_quality.overall_quality", 0) 
            for row in rows if row.get("outputs.overall_quality.overall_quality") is not None
        ]
        
        if constructiveness_scores:
            avg_constructiveness = sum(constructiveness_scores) / len(constructiveness_scores)
            print(f"   Average Constructiveness: {avg_constructiveness:.2f}/5")
        
        if actionability_scores:
            avg_actionability = sum(actionability_scores) / len(actionability_scores)
            print(f"   Average Actionability: {avg_actionability:.2f}/5")
        
        if overall_quality_scores:
            avg_overall = sum(overall_quality_scores) / len(overall_quality_scores)
            print(f"   Average Overall Quality: {avg_overall:.2f}/5")
        
        # Quality assessment
        if avg_overall >= 4:
            print("   🌟 The reviews show high quality overall!")
        elif avg_overall >= 3:
            print("   👍 The reviews show good quality with room for improvement.")
        else:
            print("   ⚠️  The reviews could benefit from significant improvement.")
    
    print(f"\n💾 Detailed results saved to: review_evaluation_results.json")


def main():
    """Main function to run the review quality evaluation."""
    try:
        # Run the evaluation
        result = run_evaluation()
        
        # Analyze and display results
        analyze_results(result)
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        raise


if __name__ == "__main__":
    main()