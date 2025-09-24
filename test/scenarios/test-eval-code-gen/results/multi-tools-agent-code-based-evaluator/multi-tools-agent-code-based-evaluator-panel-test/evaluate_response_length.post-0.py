#!/usr/bin/env python3
"""
Evaluation script to measure response length from agent traces.
This script processes the dataset.json file and evaluates the length of assistant responses.
"""

import json
import os
from typing import List, Dict, Any
from azure.ai.evaluation import evaluate

class ResponseLengthEvaluator:
    """Custom code-based evaluator to measure response length."""
    
    def __init__(self):
        pass
    
    def __call__(self, *, response: str, **kwargs) -> Dict[str, Any]:
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
                "model": trace.get('attributes', {}).get('gen_ai.request.model', 'unknown')
            })
    
    return extracted_data

def save_as_jsonl(data: List[Dict[str, Any]], output_path: str):
    """
    Save data as JSONL format required by Azure AI Evaluation SDK.
    
    Args:
        data: List of dictionaries to save
        output_path: Path to save the JSONL file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def main():
    """Main evaluation function."""
    print("Starting response length evaluation...")
    
    # Paths
    dataset_path = "dataset.json"
    evaluation_data_path = "evaluation_data.jsonl"
    output_path = "evaluation_results"
    
    # Step 1: Extract and prepare data
    print("Extracting responses from traces...")
    extracted_data = extract_responses_from_traces(dataset_path)
    
    if not extracted_data:
        print("No query-response pairs found in the dataset!")
        return
    
    print(f"Found {len(extracted_data)} query-response pairs:")
    for i, item in enumerate(extracted_data, 1):
        print(f"  {i}. Query: {item['query'][:50]}...")
        print(f"     Response: {item['response'][:50]}...")
        print(f"     Model: {item['model']}")
        print()
    
    # Step 2: Save as JSONL for evaluation
    save_as_jsonl(extracted_data, evaluation_data_path)
    print(f"Saved evaluation data to {evaluation_data_path}")
    
    # Step 3: Create evaluator
    response_length_evaluator = ResponseLengthEvaluator()
    
    # Step 4: Run evaluation
    print("Running response length evaluation...")
    
    try:
        result = evaluate(
            data=evaluation_data_path,
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
            output_path=output_path
        )
        
        print("Evaluation completed successfully!")
        print("\n=== EVALUATION RESULTS ===")
        
        # Display aggregate metrics
        if hasattr(result, 'metrics') and result.metrics:
            print("\nAggregate Metrics:")
            for metric_name, value in result.metrics.items():
                print(f"  {metric_name}: {value}")
        
        # Display individual results
        if hasattr(result, 'rows') and result.rows:
            print(f"\nIndividual Results ({len(result.rows)} responses):")
            for i, row in enumerate(result.rows, 1):
                query = row.get('query', 'N/A')[:50] + "..."
                char_count = row.get('outputs.response_length.response_length_chars', 'N/A')
                word_count = row.get('outputs.response_length.response_length_words', 'N/A')
                print(f"  {i}. Query: {query}")
                print(f"     Response length: {char_count} chars, {word_count} words")
        
        print(f"\nDetailed results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        print("Falling back to direct evaluation...")
        
        # Fallback: Direct evaluation without Azure AI Evaluation SDK
        print("\n=== DIRECT EVALUATION RESULTS ===")
        evaluator = ResponseLengthEvaluator()
        
        total_chars = 0
        total_words = 0
        results = []
        
        for i, item in enumerate(extracted_data, 1):
            result = evaluator(response=item['response'])
            results.append(result)
            
            char_count = result['response_length_chars']
            word_count = result['response_length_words']
            
            total_chars += char_count
            total_words += word_count
            
            print(f"  {i}. Query: {item['query'][:50]}...")
            print(f"     Response length: {char_count} chars, {word_count} words")
            print(f"     Model: {item['model']}")
            print()
        
        # Summary statistics
        avg_chars = total_chars / len(extracted_data)
        avg_words = total_words / len(extracted_data)
        
        print("Summary Statistics:")
        print(f"  Total responses evaluated: {len(extracted_data)}")
        print(f"  Average response length: {avg_chars:.1f} characters")
        print(f"  Average response length: {avg_words:.1f} words")
        print(f"  Total characters across all responses: {total_chars}")
        print(f"  Total words across all responses: {total_words}")

if __name__ == "__main__":
    main()