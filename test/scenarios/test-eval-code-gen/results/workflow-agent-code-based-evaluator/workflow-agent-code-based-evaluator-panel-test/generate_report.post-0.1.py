#!/usr/bin/env python3
"""
Generate a comprehensive summary report of the response length evaluation results.
"""

import json

def generate_summary_report():
    """Generate a human-readable summary of the evaluation results."""
    
    # Read the evaluation results
    with open('evaluation_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print("=" * 70)
    print("AGENT RESPONSE LENGTH EVALUATION SUMMARY REPORT")
    print("=" * 70)
    
    # Overall metrics
    metrics = results['metrics']
    print("\nAGGREGATE METRICS (Average across all responses):")
    print("-" * 50)
    print(f"Average Character Count:           {metrics['response_length.response_char_count']:.1f}")
    print(f"Average Character Count (no spaces): {metrics['response_length.response_char_count_no_spaces']:.1f}")
    print(f"Average Word Count:               {metrics['response_length.response_word_count']:.1f}")
    print(f"Average Clean Word Count:         {metrics['response_length.response_clean_word_count']:.1f}")
    print(f"Average Word Length:              {metrics['response_length.response_avg_word_length']:.2f} characters")
    
    # Individual response analysis
    print(f"\nINDIVIDUAL RESPONSE ANALYSIS ({len(results['rows'])} responses):")
    print("-" * 50)
    
    for i, row in enumerate(results['rows'], 1):
        input_text = row['inputs.input']
        char_count = row['outputs.response_length.response_char_count']
        word_count = row['outputs.response_length.response_word_count']
        category = row['outputs.response_length.response_length_category']
        avg_word_length = row['outputs.response_length.response_avg_word_length']
        
        print(f"\n{i}. Input: \"{input_text[:50]}{'...' if len(input_text) > 50 else ''}\"")
        print(f"   Length: {char_count} chars, {word_count} words ({category})")
        print(f"   Avg word length: {avg_word_length} chars")
    
    # Length distribution
    categories = {}
    for row in results['rows']:
        category = row['outputs.response_length.response_length_category']
        categories[category] = categories.get(category, 0) + 1
    
    print(f"\nLENGTH DISTRIBUTION:")
    print("-" * 50)
    for category, count in categories.items():
        percentage = (count / len(results['rows'])) * 100
        print(f"{category.capitalize():12}: {count} responses ({percentage:.1f}%)")
    
    # Response length ranges
    char_counts = [row['outputs.response_length.response_char_count'] for row in results['rows']]
    word_counts = [row['outputs.response_length.response_word_count'] for row in results['rows']]
    
    print(f"\nLENGTH RANGES:")
    print("-" * 50)
    print(f"Character count range: {min(char_counts)} - {max(char_counts)} chars")
    print(f"Word count range:      {min(word_counts)} - {max(word_counts)} words")
    
    # Insights and recommendations
    print(f"\nINSIGHTS AND RECOMMENDATIONS:")
    print("-" * 50)
    
    avg_chars = metrics['response_length.response_char_count']
    if avg_chars < 200:
        length_assessment = "quite concise"
    elif avg_chars < 600:
        length_assessment = "moderately detailed"
    elif avg_chars < 1000:
        length_assessment = "comprehensive"
    else:
        length_assessment = "very detailed"
    
    print(f"- The agent produces {length_assessment} responses with an average of {avg_chars:.0f} characters")
    print(f"- Response lengths vary significantly (range: {min(char_counts)}-{max(char_counts)} chars)")
    
    if len(set(categories.keys())) > 1:
        print("- The agent adapts response length appropriately to different types of requests")
    else:
        print("- The agent maintains consistent response length across different requests")
    
    avg_word_len = metrics['response_length.response_avg_word_length']
    if avg_word_len > 5.5:
        print(f"- Uses relatively complex vocabulary (avg word length: {avg_word_len:.1f} chars)")
    elif avg_word_len > 4.5:
        print(f"- Uses balanced vocabulary complexity (avg word length: {avg_word_len:.1f} chars)")
    else:
        print(f"- Uses simple, accessible vocabulary (avg word length: {avg_word_len:.1f} chars)")
    
    print(f"\nEvaluation completed successfully!")
    print(f"   Raw data available in: evaluation_results.json")
    print("=" * 70)

if __name__ == "__main__":
    generate_summary_report()