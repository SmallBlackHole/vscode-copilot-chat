import json
import os

def convert_dataset_to_jsonl():
    """Convert the existing dataset.json to JSONL format for evaluation."""
    
    # Read the original dataset
    with open('dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract evaluation data from the results
    eval_data = []
    
    for result in data['results']:
        # Get the original content from the writer
        original_content = None
        reviewer_feedback = None
        
        # Find the writer's content and reviewer's feedback
        for conversation in result['conversation_history']:
            if conversation['executor_id'] == 'writer':
                original_content = conversation['data']
            elif conversation['executor_id'] == 'reviewer':
                reviewer_feedback = conversation['data']
        
        # Create evaluation record
        if original_content and reviewer_feedback:
            eval_record = {
                "input_query": result['input'],
                "original_content": original_content,
                "reviewer_feedback": reviewer_feedback,
                "final_output": result['final_output'],
                "final_state": result['final_state']
            }
            eval_data.append(eval_record)
    
    # Write to JSONL format
    with open('review_evaluation_data.jsonl', 'w', encoding='utf-8') as f:
        for record in eval_data:
            f.write(json.dumps(record) + '\n')
    
    print(f"Converted {len(eval_data)} records to review_evaluation_data.jsonl")
    
    # Display sample record for verification
    if eval_data:
        print("\nSample record:")
        print(json.dumps(eval_data[0], indent=2))

if __name__ == "__main__":
    convert_dataset_to_jsonl()