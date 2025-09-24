"""
Data processor to convert trace data from dataset.json into evaluation-ready format.
Extracts user queries, tool calls, and agent responses for evaluation.
"""

import json
import re
from typing import List, Dict, Any, Optional


def extract_user_query(events: List[Dict]) -> Optional[str]:
    """Extract user query from trace events."""
    for event in events:
        if event.get("name") == "gen_ai.user.message":
            body = json.loads(event.get("body", "{}"))
            contents = body.get("contents", [])
            if contents and len(contents) > 0:
                return contents[0].get("text", "")
    return None


def extract_tool_calls(events: List[Dict]) -> List[Dict]:
    """Extract tool calls from trace events."""
    tool_calls = []
    
    for event in events:
        if event.get("name") == "gen_ai.choice":
            body = json.loads(event.get("body", "{}"))
            message = body.get("message", {})
            contents = message.get("contents", [])
            
            for content in contents:
                if content.get("type") == "function_call":
                    # Convert to the format expected by ToolCallAccuracyEvaluator
                    tool_call = {
                        "type": "tool_call",
                        "tool_call_id": content.get("call_id", ""),
                        "name": content.get("name", ""),
                        "arguments": json.loads(content.get("arguments", "{}"))
                    }
                    tool_calls.append(tool_call)
    
    return tool_calls


def extract_final_response(events: List[Dict]) -> Optional[str]:
    """Extract the final agent response from trace events."""
    for event in reversed(events):  # Check from the end
        if event.get("name") == "gen_ai.choice":
            body = json.loads(event.get("body", "{}"))
            message = body.get("message", {})
            contents = message.get("contents", [])
            
            for content in contents:
                if content.get("type") == "text":
                    return content.get("text", "")
    return None


def define_tool_definitions() -> List[Dict]:
    """Define the tool definitions used by the agent."""
    return [
        {
            "name": "get_weather",
            "type": "function", 
            "description": "Get current weather information for a specified location",
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
                "properties": {},
                "required": []
            }
        }
    ]


def process_traces_to_evaluation_data(dataset_path: str, output_path: str) -> None:
    """
    Process trace data and convert to JSONL format for evaluation.
    
    Args:
        dataset_path: Path to the dataset.json file
        output_path: Path to save the processed JSONL file
    """
    
    with open(dataset_path, 'r') as f:
        data = json.load(f)
    
    tool_definitions = define_tool_definitions()
    evaluation_data = []
    
    for i, trace in enumerate(data.get("traces", [])):
        events = trace.get("events", [])
        
        # Extract components
        query = extract_user_query(events)
        tool_calls = extract_tool_calls(events)
        response = extract_final_response(events)
        
        if query and response:
            evaluation_record = {
                "trace_id": trace.get("context", {}).get("trace_id", f"trace_{i}"),
                "query": query,
                "response": response,
                "tool_calls": tool_calls,
                "tool_definitions": tool_definitions
            }
            evaluation_data.append(evaluation_record)
    
    # Write to JSONL format
    with open(output_path, 'w') as f:
        for record in evaluation_data:
            f.write(json.dumps(record) + '\n')
    
    print(f"Processed {len(evaluation_data)} traces and saved to {output_path}")
    
    # Print summary for verification
    print("\nSummary of processed data:")
    for i, record in enumerate(evaluation_data):
        print(f"Record {i+1}:")
        print(f"  Query: {record['query']}")
        print(f"  Response: {record['response']}")
        print(f"  Tool calls: {len(record['tool_calls'])} calls")
        for j, tool_call in enumerate(record['tool_calls']):
            print(f"    {j+1}. {tool_call['name']}({tool_call['arguments']})")
        print()


if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, "dataset.json")
    output_path = os.path.join(script_dir, "evaluation_data.jsonl")
    process_traces_to_evaluation_data(dataset_path, output_path)