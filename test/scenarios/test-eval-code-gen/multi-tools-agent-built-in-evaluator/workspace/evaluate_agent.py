"""
Agent Evaluation Script
Evaluates agent performance using Azure AI Evaluation SDK for:
1. Response relevance to user queries
2. Tool call accuracy
"""

import os
import json
from azure.ai.evaluation import evaluate, RelevanceEvaluator, ToolCallAccuracyEvaluator
from azure.ai.evaluation import OpenAIModelConfiguration


def setup_model_configuration():
    """Setup model configuration for evaluators."""
    # Use GitHub-hosted models as recommended for getting started
    model_config = OpenAIModelConfiguration(
        type="openai",
        model="gpt-4o-mini",  # Free tier model
        base_url="https://models.inference.ai.azure.com",
        api_key=os.environ["GITHUB_TOKEN"]
    )
    return model_config


def run_evaluation():
    """Run comprehensive evaluation on the agent traces."""
    
    print("🚀 Starting Agent Evaluation")
    print("=" * 50)
    
    # Setup model configuration
    model_config = setup_model_configuration()
    
    # Initialize evaluators
    print("📋 Initializing evaluators...")
    relevance_evaluator = RelevanceEvaluator(model_config=model_config)
    tool_call_accuracy_evaluator = ToolCallAccuracyEvaluator(model_config=model_config)
    
    # Prepare evaluation
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "evaluation_data.jsonl")
    output_path = os.path.join(script_dir, "evaluation_results")
    
    print(f"📊 Evaluating data from: {data_file}")
    print(f"💾 Results will be saved to: {output_path}")
    
    # Run evaluation using the evaluate() API
    result = evaluate(
        data=data_file,
        evaluators={
            "relevance": relevance_evaluator,
            "tool_call_accuracy": tool_call_accuracy_evaluator
        },
        evaluator_config={
            "relevance": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}"
                }
            },
            "tool_call_accuracy": {
                "column_mapping": {
                    "query": "${data.query}",
                    "tool_calls": "${data.tool_calls}",
                    "tool_definitions": "${data.tool_definitions}"
                }
            }
        },
        output_path=output_path
    )
    
    # Print results summary
    print("\n" + "=" * 50)
    print("📈 EVALUATION RESULTS SUMMARY")
    print("=" * 50)
    
    print("\n🎯 RELEVANCE METRICS:")
    relevance_metrics = {k: v for k, v in result['metrics'].items() if 'relevance' in k}
    for metric, value in relevance_metrics.items():
        print(f"  {metric}: {value}")
    
    print("\n🔧 TOOL CALL ACCURACY METRICS:")
    tool_metrics = {k: v for k, v in result['metrics'].items() if 'tool_call_accuracy' in k}
    for metric, value in tool_metrics.items():
        print(f"  {metric}: {value}")
    
    print("\n📋 OVERALL METRICS:")
    other_metrics = {k: v for k, v in result['metrics'].items() 
                    if 'relevance' not in k and 'tool_call_accuracy' not in k}
    for metric, value in other_metrics.items():
        print(f"  {metric}: {value}")
    
    # Print detailed per-row results
    print("\n" + "=" * 50)
    print("📝 DETAILED PER-TRACE RESULTS")
    print("=" * 50)
    
    for i, row in result['rows'].iterrows():
        print(f"\n🔍 Trace {i+1}:")
        print(f"  Query: {row['query']}")
        print(f"  Response: {row['response']}")
        print(f"  Relevance Score: {row.get('relevance', 'N/A')}")
        print(f"  Relevance Result: {row.get('relevance_result', 'N/A')}")
        print(f"  Tool Call Accuracy Score: {row.get('tool_call_accuracy', 'N/A')}")
        print(f"  Tool Call Accuracy Result: {row.get('tool_call_accuracy_result', 'N/A')}")
        
        if 'tool_calls' in row:
            tool_calls = row['tool_calls']
            if isinstance(tool_calls, list) and len(tool_calls) > 0:
                print(f"  Tool Calls Made: {len(tool_calls)}")
                for j, tool_call in enumerate(tool_calls):
                    if isinstance(tool_call, dict):
                        print(f"    {j+1}. {tool_call.get('name', 'Unknown')}({tool_call.get('arguments', {})})")
    
    print(f"\n✅ Evaluation completed! Detailed results saved to: {output_path}")
    return result


def analyze_results(result):
    """Provide additional analysis of the evaluation results."""
    print("\n" + "=" * 50)
    print("🧪 ANALYSIS & INSIGHTS")
    print("=" * 50)
    
    # Relevance analysis
    relevance_scores = [row.get('relevance') for _, row in result['rows'].iterrows() 
                       if row.get('relevance') is not None]
    if relevance_scores:
        avg_relevance = sum(relevance_scores) / len(relevance_scores)
        print(f"\n📊 Relevance Analysis:")
        print(f"  Average Score: {avg_relevance:.2f}/5.0")
        print(f"  Best Score: {max(relevance_scores):.2f}")
        print(f"  Worst Score: {min(relevance_scores):.2f}")
        
        excellent_count = sum(1 for score in relevance_scores if score >= 4.0)
        print(f"  Excellent responses (≥4.0): {excellent_count}/{len(relevance_scores)}")
    
    # Tool call accuracy analysis
    tool_scores = [row.get('tool_call_accuracy') for _, row in result['rows'].iterrows() 
                  if row.get('tool_call_accuracy') is not None]
    if tool_scores:
        avg_tool_accuracy = sum(tool_scores) / len(tool_scores)
        print(f"\n🔧 Tool Call Accuracy Analysis:")
        print(f"  Average Score: {avg_tool_accuracy:.2f}/5.0")
        print(f"  Best Score: {max(tool_scores):.2f}")
        print(f"  Worst Score: {min(tool_scores):.2f}")
        
        accurate_count = sum(1 for score in tool_scores if score >= 4.0)
        print(f"  Highly accurate tool usage (≥4.0): {accurate_count}/{len(tool_scores)}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if relevance_scores and avg_relevance < 3.0:
        print("  - Consider improving response relevance to user queries")
    if tool_scores and avg_tool_accuracy < 3.0:
        print("  - Review tool selection and parameter passing logic")
    if relevance_scores and tool_scores:
        if avg_relevance > 4.0 and avg_tool_accuracy > 4.0:
            print("  - Excellent performance! Agent is working well.")
        elif avg_relevance > avg_tool_accuracy:
            print("  - Responses are relevant but tool usage could be improved")
        elif avg_tool_accuracy > avg_relevance:
            print("  - Tool usage is good but responses could be more relevant")


if __name__ == "__main__":
    try:
        # Check if GITHUB_TOKEN is available
        if "GITHUB_TOKEN" not in os.environ:
            print("❌ Error: GITHUB_TOKEN environment variable is required")
            print("Please set your GitHub token in the environment.")
            exit(1)
            
        # Check if data file exists
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, "evaluation_data.jsonl")
        if not os.path.exists(data_file):
            print("❌ Error: evaluation_data.jsonl not found")
            print("Please run data_processor.py first to generate the evaluation data.")
            exit(1)
        
        # Run evaluation
        result = run_evaluation()
        
        # Analyze results
        analyze_results(result)
        
    except Exception as e:
        print(f"❌ Error during evaluation: {str(e)}")
        print("Please check your configuration and try again.")