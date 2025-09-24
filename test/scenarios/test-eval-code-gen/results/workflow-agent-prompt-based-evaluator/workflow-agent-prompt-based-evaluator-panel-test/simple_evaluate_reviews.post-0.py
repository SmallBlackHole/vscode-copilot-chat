# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import json
import pandas as pd
from azure.ai.evaluation import evaluate, OpenAIModelConfiguration

def simple_constructiveness_evaluator(*, original_content: str, reviewer_feedback: str, **kwargs):
    """Simple constructiveness evaluator for testing."""
    # For demo purposes, score based on length and presence of specific words
    feedback_lower = reviewer_feedback.lower()
    
    score = 3  # Base score
    
    # Positive indicators
    if any(word in feedback_lower for word in ['consider', 'suggest', 'recommend', 'improve']):
        score += 0.5
    if any(word in feedback_lower for word in ['good', 'effective', 'nice', 'well']):
        score += 0.5
    if len(reviewer_feedback.split()) > 20:  # Detailed feedback
        score += 0.5
    if any(word in feedback_lower for word in ['specific', 'example', 'concrete']):
        score += 0.5
    
    # Negative indicators
    if any(word in feedback_lower for word in ['bad', 'terrible', 'awful', 'wrong']):
        score -= 1
    if len(reviewer_feedback.split()) < 10:  # Too short
        score -= 0.5
    
    # Ensure score is within range
    score = max(1, min(5, score))
    
    return {
        "constructiveness": score,
        "constructiveness_reasoning": f"Scored {score} based on language analysis and feedback characteristics."
    }

def simple_actionability_evaluator(*, original_content: str, reviewer_feedback: str, **kwargs):
    """Simple actionability evaluator for testing."""
    feedback_lower = reviewer_feedback.lower()
    
    score = 3  # Base score
    
    # Positive indicators for actionability
    if any(word in feedback_lower for word in ['tighten', 'clarify', 'vary', 'enhance', 'polish']):
        score += 0.5
    if any(word in feedback_lower for word in ['e.g.', 'for example', 'such as', 'like']):
        score += 0.5
    if '—' in reviewer_feedback or '-' in reviewer_feedback:  # Specific examples given
        score += 0.5
    if any(word in feedback_lower for word in ['check', 'ensure', 'make sure', 'try']):
        score += 0.5
    
    # Negative indicators
    if any(word in feedback_lower for word in ['generally', 'overall', 'in general']):
        score -= 0.5
    if len(reviewer_feedback.split()) < 15:  # Too vague/short
        score -= 0.5
    
    # Ensure score is within range
    score = max(1, min(5, score))
    
    return {
        "actionability": score,
        "actionability_reasoning": f"Scored {score} based on specificity and actionable language use."
    }

def simple_overall_quality_evaluator(*, original_content: str, reviewer_feedback: str, **kwargs):
    """Simple overall quality evaluator for testing."""
    feedback_lower = reviewer_feedback.lower()
    
    score = 3  # Base score
    
    # Quality indicators
    word_count = len(reviewer_feedback.split())
    if word_count > 30:  # Comprehensive
        score += 0.5
    if word_count > 50:  # Very comprehensive
        score += 0.5
    
    # Professional language
    if any(word in feedback_lower for word in ['thoughtful', 'insightful', 'analysis', 'perspective']):
        score += 0.5
    
    # Balance indicators
    if any(word in feedback_lower for word in ['balance', 'strength', 'positive']) and any(word in feedback_lower for word in ['improve', 'enhance', 'consider']):
        score += 0.5
    
    # Negative indicators
    if any(word in feedback_lower for word in ['confusing', 'unclear', 'messy']):
        score -= 0.5
    
    # Ensure score is within range
    score = max(1, min(5, score))
    
    return {
        "overall_quality": score,
        "overall_quality_reasoning": f"Scored {score} based on comprehensiveness, professionalism, and balanced approach."
    }

def run_simple_evaluation():
    """Run a simple evaluation using rule-based evaluators."""
    print("🚀 Starting Simple Review Quality Evaluation")
    print("=" * 50)
    
    # Check if data file exists
    data_file = "review_evaluation_data.jsonl"
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file '{data_file}' not found. Please run convert_dataset.py first.")
    
    print(f"✅ Using data file: {data_file}")
    
    # Create evaluators
    evaluators = {
        "constructiveness": simple_constructiveness_evaluator,
        "actionability": simple_actionability_evaluator,
        "overall_quality": simple_overall_quality_evaluator
    }
    
    # Configure column mapping
    evaluator_config = {
        "default": {
            "column_mapping": {
                "original_content": "${data.original_content}",
                "reviewer_feedback": "${data.reviewer_feedback}"
            }
        }
    }
    
    print(f"✅ Created {len(evaluators)} evaluators")
    for name in evaluators.keys():
        print(f"   - {name}")
    
    # Run evaluation
    print("\n🔄 Running evaluation...")
    result = evaluate(
        data=data_file,
        evaluators=evaluators,
        evaluator_config=evaluator_config,
        output_path="simple_review_evaluation_results.json"
    )
    
    print("✅ Evaluation completed successfully!")
    
    return result

def analyze_simple_results(result):
    """Analyze and display the simple evaluation results."""
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
        
        all_scores = {
            'constructiveness': [],
            'actionability': [],
            'overall_quality': []
        }
        
        for i, row in enumerate(rows, 1):
            print(f"\n--- Review {i} ---")
            
            # Extract input data
            query = row.get("inputs.input_query", "N/A")
            feedback = row.get("inputs.reviewer_feedback", "N/A")
            
            print(f"Query: {query[:100]}...")
            print(f"Feedback: {feedback[:150]}...")
            
            # Extract scores
            constructiveness = row.get("outputs.constructiveness.constructiveness", "N/A")
            actionability = row.get("outputs.actionability.actionability", "N/A")
            overall_quality = row.get("outputs.overall_quality.overall_quality", "N/A")
            
            print(f"Constructiveness: {constructiveness}")
            print(f"Actionability: {actionability}")
            print(f"Overall Quality: {overall_quality}")
            
            # Store scores for analysis
            if isinstance(constructiveness, (int, float)):
                all_scores['constructiveness'].append(constructiveness)
            if isinstance(actionability, (int, float)):
                all_scores['actionability'].append(actionability)
            if isinstance(overall_quality, (int, float)):
                all_scores['overall_quality'].append(overall_quality)
    
    # Generate summary insights
    print(f"\n💡 INSIGHTS:")
    if all_scores['constructiveness']:
        avg_constructiveness = sum(all_scores['constructiveness']) / len(all_scores['constructiveness'])
        print(f"   Average Constructiveness: {avg_constructiveness:.2f}/5")
    
    if all_scores['actionability']:
        avg_actionability = sum(all_scores['actionability']) / len(all_scores['actionability'])
        print(f"   Average Actionability: {avg_actionability:.2f}/5")
    
    if all_scores['overall_quality']:
        avg_overall = sum(all_scores['overall_quality']) / len(all_scores['overall_quality'])
        print(f"   Average Overall Quality: {avg_overall:.2f}/5")
        
        # Quality assessment
        if avg_overall >= 4:
            print("   🌟 The reviews show high quality overall!")
        elif avg_overall >= 3:
            print("   👍 The reviews show good quality with room for improvement.")
        else:
            print("   ⚠️  The reviews could benefit from significant improvement.")
    
    print(f"\n💾 Detailed results saved to: simple_review_evaluation_results.json")

def main():
    """Main function to run the simple review quality evaluation."""
    try:
        # Run the evaluation
        result = run_simple_evaluation()
        
        # Analyze and display results
        analyze_simple_results(result)
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        raise

if __name__ == "__main__":
    main()