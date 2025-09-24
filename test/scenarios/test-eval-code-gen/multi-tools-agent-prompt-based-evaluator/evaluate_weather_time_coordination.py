#!/usr/bin/env python3
"""
Evaluation script for measuring how well an agent handles queries that involve 
both weather and time in a coordinated manner.

This script evaluates:
1. Tool call accuracy for coordinated weather and time queries
2. Parallel execution efficiency 
3. Response completeness and accuracy
4. Coordination quality between multiple tools
"""

import json
import os
import sys
from typing import List, Dict, Any, Union
import pandas as pd
from azure.ai.evaluation import evaluate, ToolCallAccuracyEvaluator, OpenAIModelConfiguration


# Custom evaluators for weather-time coordination assessment
class CoordinationEfficiencyEvaluator:
    """Evaluates how efficiently the agent coordinates weather and time tools."""
    
    def __init__(self):
        pass
    
    def __call__(self, *, query: str, tool_calls: List[Dict], **kwargs) -> Dict[str, Union[str, float]]:
        """
        Evaluate coordination efficiency based on:
        - Whether both weather and time tools are used when both are needed
        - Whether tools are called in parallel vs sequential (parallel is better)
        - Whether excessive/unnecessary tool calls are made
        """
        if not tool_calls:
            return {
                "coordination_efficiency": "not_applicable",
                "coordination_efficiency_score": 0.0,
                "coordination_efficiency_reason": "No tool calls found"
            }
        
        # Parse query to determine if both weather and time are requested
        query_lower = query.lower()
        needs_weather = any(word in query_lower for word in ['weather', 'temperature', 'sunny', 'rain', 'climate'])
        needs_time = any(word in query_lower for word in ['time', 'utc', 'clock', 'hour', 'minute', 'when'])
        
        if not (needs_weather and needs_time):
            return {
                "coordination_efficiency": "not_applicable", 
                "coordination_efficiency_score": 0.0,
                "coordination_efficiency_reason": "Query does not require both weather and time"
            }
        
        # Extract tool names from tool calls
        weather_tools = []
        time_tools = []
        other_tools = []
        
        for call in tool_calls:
            if isinstance(call, dict):
                name = call.get('name', '')
                if 'weather' in name.lower():
                    weather_tools.append(call)
                elif 'time' in name.lower():
                    time_tools.append(call)
                else:
                    other_tools.append(call)
        
        has_weather_call = len(weather_tools) > 0
        has_time_call = len(time_tools) > 0
        total_calls = len(tool_calls)
        
        # Score based on coordination quality
        score = 0.0
        reason_parts = []
        
        if has_weather_call and has_time_call:
            score += 3.0  # Base score for using both required tools
            reason_parts.append("Used both weather and time tools")
            
            # Check for parallel execution (tools called in same LLM turn)
            if len(tool_calls) == 2:  # Optimal case: exactly 2 calls
                score += 2.0
                reason_parts.append("Optimal parallel execution")
            elif len(tool_calls) > 2:
                score += 1.0  # Some points for parallel but with extra calls
                reason_parts.append("Parallel execution with extra calls")
            else:
                reason_parts.append("Sequential execution")
        elif has_weather_call or has_time_call:
            score += 1.0  # Partial score for using one required tool
            missing = "time" if has_weather_call else "weather"
            reason_parts.append(f"Missing {missing} tool call")
        else:
            reason_parts.append("Missing both required tool calls")
        
        # Efficiency rating
        if score >= 4.5:
            efficiency = "excellent"
        elif score >= 3.0:
            efficiency = "good"
        elif score >= 1.5:
            efficiency = "fair"
        else:
            efficiency = "poor"
        
        return {
            "coordination_efficiency": efficiency,
            "coordination_efficiency_score": score,
            "coordination_efficiency_reason": "; ".join(reason_parts)
        }


class ResponseCompletenessEvaluator:
    """Evaluates whether the response includes both weather and time information when both are requested."""
    
    def __init__(self):
        pass
    
    def __call__(self, *, query: str, response: str, **kwargs) -> Dict[str, Union[str, float]]:
        """
        Evaluate response completeness for weather-time coordination queries.
        """
        query_lower = query.lower()
        response_lower = response.lower()
        
        # Check if query requests both weather and time
        needs_weather = any(word in query_lower for word in ['weather', 'temperature', 'sunny', 'rain', 'climate'])
        needs_time = any(word in query_lower for word in ['time', 'utc', 'clock', 'hour', 'minute', 'when'])
        
        if not (needs_weather and needs_time):
            return {
                "response_completeness": "not_applicable",
                "response_completeness_score": 0.0,
                "response_completeness_reason": "Query does not require both weather and time"
            }
        
        # Check if response contains weather information
        has_weather_info = any(word in response_lower for word in [
            'weather', 'temperature', 'sunny', 'rain', 'cloudy', 'degrees', '°c', '°f', 'celsius', 'fahrenheit'
        ])
        
        # Check if response contains time information
        has_time_info = any(word in response_lower for word in [
            'time', 'utc', 'am', 'pm', 'hour', 'minute', 'clock', ':', 'september', 'monday', 'tuesday'
        ]) or any(char.isdigit() and ':' in response for char in response)
        
        score = 0.0
        reason_parts = []
        
        if has_weather_info and has_time_info:
            score = 5.0
            completeness = "complete"
            reason_parts.append("Contains both weather and time information")
        elif has_weather_info or has_time_info:
            score = 2.5
            completeness = "partial"
            missing = "time" if has_weather_info else "weather"
            reason_parts.append(f"Contains only {missing} information")
        else:
            score = 0.0
            completeness = "incomplete"
            reason_parts.append("Missing both weather and time information")
        
        return {
            "response_completeness": completeness,
            "response_completeness_score": score,
            "response_completeness_reason": "; ".join(reason_parts)
        }


def convert_traces_to_jsonl(traces_file: str, output_file: str) -> str:
    """
    Convert OpenTelemetry traces to JSONL format for evaluation.
    
    Args:
        traces_file: Path to the JSON file containing traces
        output_file: Path to save the JSONL file
    
    Returns:
        Path to the created JSONL file
    """
    with open(traces_file, 'r') as f:
        data = json.load(f)
    
    evaluation_data = []
    
    for trace in data.get('traces', []):
        # Extract query from user message event
        query = None
        response = None
        tool_calls = []
        
        for event in trace.get('events', []):
            if event['name'] == 'gen_ai.user.message':
                body = json.loads(event['body'])
                contents = body.get('contents', [])
                if contents and contents[0].get('type') == 'text':
                    query = contents[0]['text']
            
            elif event['name'] == 'gen_ai.choice':
                body = json.loads(event['body'])
                message = body.get('message', {})
                contents = message.get('contents', [])
                
                for content in contents:
                    if content.get('type') == 'function_call':
                        # Convert to tool call format expected by evaluator
                        tool_call = {
                            "type": "tool_call",
                            "tool_call_id": content.get('call_id', ''),
                            "name": content.get('name', ''),
                            "arguments": json.loads(content.get('arguments', '{}'))
                        }
                        tool_calls.append(tool_call)
                    
                    elif content.get('type') == 'text':
                        response = content.get('text', '')
        
        if query:
            # Define tool definitions for weather and time tools
            tool_definitions = [
                {
                    "name": "get_weather",
                    "type": "function", 
                    "description": "Get weather information for a specified location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get weather for"
                            }
                        },
                        "required": ["location"]
                    }
                },
                {
                    "name": "get_time", 
                    "type": "function",
                    "description": "Get current UTC time",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
            
            evaluation_data.append({
                "query": query,
                "response": response or "",
                "tool_calls": tool_calls,
                "tool_definitions": tool_definitions,
                "trace_id": trace.get('context', {}).get('trace_id', ''),
                "span_id": trace.get('context', {}).get('span_id', '')
            })
    
    # Write to JSONL format
    with open(output_file, 'w') as f:
        for item in evaluation_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"Converted {len(evaluation_data)} traces to JSONL format: {output_file}")
    return output_file


def main():
    """Main evaluation function."""
    
    # Set up model configuration for evaluators (using GitHub models for free tier)
    model_config = OpenAIModelConfiguration(
        type="openai",
        model="gpt-4.1-mini",  # Good balance of performance and cost
        base_url="https://models.github.ai/inference",
        api_key=os.environ.get("GITHUB_TOKEN", "your-github-token-here")
    )
    
    # Convert traces to JSONL format
    traces_file = "workspace/dataset.json"
    jsonl_file = "evaluation_data.jsonl"
    
    if not os.path.exists(traces_file):
        print(f"Error: Dataset file not found: {traces_file}")
        sys.exit(1)
    
    convert_traces_to_jsonl(traces_file, jsonl_file)
    
    # Initialize evaluators
    tool_call_accuracy = ToolCallAccuracyEvaluator(model_config=model_config)
    coordination_efficiency = CoordinationEfficiencyEvaluator()
    response_completeness = ResponseCompletenessEvaluator()
    
    # Run evaluation
    print("Starting evaluation of weather-time coordination...")
    
    try:
        result = evaluate(
            data=jsonl_file,
            evaluators={
                "tool_call_accuracy": tool_call_accuracy,
                "coordination_efficiency": coordination_efficiency,
                "response_completeness": response_completeness
            },
            evaluator_config={
                "tool_call_accuracy": {
                    "column_mapping": {
                        "query": "${data.query}",
                        "tool_calls": "${data.tool_calls}",
                        "tool_definitions": "${data.tool_definitions}",
                        "response": "${data.response}"
                    }
                },
                "coordination_efficiency": {
                    "column_mapping": {
                        "query": "${data.query}",
                        "tool_calls": "${data.tool_calls}"
                    }
                },
                "response_completeness": {
                    "column_mapping": {
                        "query": "${data.query}",
                        "response": "${data.response}"
                    }
                }
            },
            output_path="./evaluation_results"
        )
        
        print("\n" + "="*60)
        print("EVALUATION RESULTS - Weather & Time Coordination")
        print("="*60)
        
        # Print summary metrics
        if hasattr(result, 'metrics'):
            metrics = result.metrics
            print(f"\nOverall Metrics:")
            print(f"  • Tool Call Accuracy: {metrics.get('tool_call_accuracy', 'N/A')}")
            print(f"  • Coordination Efficiency: {metrics.get('coordination_efficiency_score', 'N/A')}")
            print(f"  • Response Completeness: {metrics.get('response_completeness_score', 'N/A')}")
        
        # Print detailed results if available
        if hasattr(result, 'rows'):
            print(f"\nDetailed Results:")
            for i, row in enumerate(result.rows):
                print(f"\n  Query {i+1}: {row.get('query', 'N/A')[:60]}...")
                print(f"    Tool Call Accuracy: {row.get('outputs.tool_call_accuracy.tool_call_accuracy', 'N/A')}")
                print(f"    Coordination: {row.get('outputs.coordination_efficiency.coordination_efficiency', 'N/A')}")
                print(f"    Completeness: {row.get('outputs.response_completeness.response_completeness', 'N/A')}")
        
        print(f"\nFull results saved to: ./evaluation_results")
        print("="*60)
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        print("Please check your GitHub token and model access.")
        sys.exit(1)
    
    # Clean up temporary files
    if os.path.exists(jsonl_file):
        os.remove(jsonl_file)


if __name__ == "__main__":
    main()