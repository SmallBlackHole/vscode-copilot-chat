#!/usr/bin/env python3
"""
Convert dataset.json to JSONL format required by Azure AI Evaluation SDK.
This script transforms the agent conversation results into evaluation-ready format.
"""

import json

def convert_dataset_to_jsonl():
    """
    Convert the JSON dataset to JSONL format for Azure AI Evaluation SDK.
    
    The SDK requires:
    - JSONL format (one JSON object per line)
    - No timestamp fields (they cause SDK errors)
    - Clean field names for column mapping
    """
    
    # Read the original dataset
    with open('dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    # Transform each result into evaluation format
    evaluation_data = []
    
    for result in dataset['results']:
        # Extract essential fields, removing timestamps
        eval_record = {
            'input': result['input'],
            'response': result['final_output'],
            'final_state': result['final_state']
            # Note: Deliberately excluding 'timestamp' field as it causes SDK errors
        }
        
        evaluation_data.append(eval_record)
    
    # Write to JSONL format
    with open('evaluation_data.jsonl', 'w', encoding='utf-8') as f:
        for record in evaluation_data:
            f.write(json.dumps(record) + '\n')
    
    print(f"Converted {len(evaluation_data)} records to evaluation_data.jsonl")
    print("Sample record:")
    print(json.dumps(evaluation_data[0], indent=2))

if __name__ == "__main__":
    convert_dataset_to_jsonl()