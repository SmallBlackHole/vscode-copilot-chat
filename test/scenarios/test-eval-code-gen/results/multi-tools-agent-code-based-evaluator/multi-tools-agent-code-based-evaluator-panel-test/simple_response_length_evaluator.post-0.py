#!/usr/bin/env python3
"""
Simple evaluation script to measure response length from agent traces.
This script processes the dataset.json file and evaluates the length of assistant responses.
"""

import json
import os
from typing import List, Dict, Any

def extract_responses_from_traces(dataset_path: str) -> List[Dict[str, Any]]:
    """
    Extract user queries and assistant responses from the trace dataset.
    
    Args:
        dataset_path: Path to the dataset.json file
        
    Returns:
        List of dictionaries containing query-response pairs
    """
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    extracted_data = []
    
    for trace in data.get('traces', []):
        events = trace.get('events', [])
        
        # Find user message and assistant response in the events
        user_message = None
        assistant_response = None
        
        for event in events:
            if event.get('name') == 'gen_ai.user.message':
                # Parse the body to get the user message
                body = json.loads(event.get('body', '{}'))
                contents = body.get('contents', [])
                if contents and len(contents) > 0:
                    user_message = contents[0].get('text', '')
            
            elif event.get('name') == 'gen_ai.choice':
                # Parse the body to get the assistant response
                body = json.loads(event.get('body', '{}'))
                message = body.get('message', {})
                contents = message.get('contents', [])
                
                # Look for text content in the response
                for content in contents:
                    if content.get('type') == 'text':
                        assistant_response = content.get('text', '')
                        break
        
        # Add the query-response pair if both are found
        if user_message and assistant_response:
            extracted_data.append({
                "query": user_message,
                "response": assistant_response,
                "trace_id": trace.get('context', {}).get('trace_id', ''),
                "model": trace.get('attributes', {}).get('gen_ai.request.model', 'unknown'),
                "start_time": trace.get('start_time', ''),
                "end_time": trace.get('end_time', '')
            })
    
    return extracted_data

def evaluate_response_length(response: str) -> Dict[str, Any]:
    """
    Evaluate the length of a response.
    
    Args:
        response: The assistant response text to measure
        
    Returns:
        Dictionary containing response length metrics
    """
    if not response:
        return {
            "response_length_chars": 0,
            "response_length_words": 0,
            "response_empty": True
        }
    
    char_count = len(response)
    word_count = len(response.split())
    
    return {
        "response_length_chars": char_count,
        "response_length_words": word_count,
        "response_empty": False
    }

def calculate_duration(start_time: str, end_time: str) -> float:
    """Calculate duration between start and end times in seconds."""
    try:
        from datetime import datetime
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        return (end - start).total_seconds()
    except:
        return 0.0

def main():
    """Main evaluation function."""
    print("Starting response length evaluation...")
    
    # Paths
    dataset_path = "dataset.json"
    
    # Step 1: Extract and prepare data
    print("Extracting responses from traces...")
    extracted_data = extract_responses_from_traces(dataset_path)
    
    if not extracted_data:
        print("No query-response pairs found in the dataset!")
        return
    
    print(f"Found {len(extracted_data)} query-response pairs")
    print("\n=== EVALUATION RESULTS ===")
    
    # Step 2: Evaluate each response
    results = []
    total_chars = 0
    total_words = 0
    total_duration = 0.0
    
    for i, item in enumerate(extracted_data, 1):
        # Evaluate response length
        length_metrics = evaluate_response_length(item['response'])
        
        # Calculate response time
        duration = calculate_duration(item['start_time'], item['end_time'])
        
        # Combine results
        result = {
            **item,
            **length_metrics,
            "response_duration_seconds": duration
        }
        results.append(result)
        
        # Accumulate totals
        total_chars += length_metrics['response_length_chars']
        total_words += length_metrics['response_length_words']
        total_duration += duration
        
        # Display individual result
        print(f"\n{i}. User Query: {item['query']}")
        print(f"   Assistant Response: {item['response']}")
        print(f"   Model: {item['model']}")
        print(f"   Response Length: {length_metrics['response_length_chars']} characters, {length_metrics['response_length_words']} words")
        print(f"   Response Time: {duration:.2f} seconds")
        print(f"   Trace ID: {item['trace_id']}")
    
    # Step 3: Calculate and display summary statistics
    num_responses = len(extracted_data)
    avg_chars = total_chars / num_responses
    avg_words = total_words / num_responses
    avg_duration = total_duration / num_responses
    
    print("\n" + "="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    print(f"Total responses evaluated: {num_responses}")
    print(f"Average response length: {avg_chars:.1f} characters")
    print(f"Average response length: {avg_words:.1f} words")
    print(f"Average response time: {avg_duration:.2f} seconds")
    print(f"Total characters across all responses: {total_chars}")
    print(f"Total words across all responses: {total_words}")
    print(f"Total response time: {total_duration:.2f} seconds")
    
    # Step 4: Save detailed results
    output_file = "evaluation_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "summary": {
                "total_responses": num_responses,
                "average_chars": avg_chars,
                "average_words": avg_words,
                "average_duration_seconds": avg_duration,
                "total_chars": total_chars,
                "total_words": total_words,
                "total_duration_seconds": total_duration
            },
            "individual_results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: {output_file}")

if __name__ == "__main__":
    main()