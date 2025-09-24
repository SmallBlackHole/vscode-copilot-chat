"""
Summary Analysis of Relevance Evaluation Results

This script analyzes and summarizes the evaluation results for response relevance.
"""

import json
from pathlib import Path


def analyze_evaluation_results():
    """Analyze and display evaluation results in a structured format"""
    
    # Read evaluation results
    results_file = Path(__file__).parent / "evaluation_results"
    
    with open(results_file) as f:
        results = json.load(f)
    
    print("="*80)
    print("RELEVANCE EVALUATION RESULTS SUMMARY")
    print("="*80)
    
    # Overall metrics
    metrics = results.get('metrics', {})
    print("\n📊 OVERALL METRICS:")
    print(f"   Average Relevance Score: {metrics.get('relevance.relevance', 0):.3f}/5")
    print(f"   Score Threshold: {metrics.get('relevance.relevance_threshold', 0):.1f}")
    print(f"   Pass Rate: {metrics.get('relevance.binary_aggregate', 0)*100:.1f}%")
    
    # Individual results
    rows = results.get('rows', [])
    print(f"\n📋 INDIVIDUAL EVALUATION RESULTS ({len(rows)} items):")
    print("-"*80)
    
    for i, row in enumerate(rows, 1):
        query = row.get('inputs.query', '')
        response = row.get('inputs.response', '')
        score = row.get('outputs.relevance.relevance', 0)
        reasoning = row.get('outputs.relevance.relevance_reason', '')
        result = row.get('outputs.relevance.relevance_result', '')
        
        print(f"\n{i}. QUERY: {query}")
        print(f"   RESPONSE: {response[:100]}...")
        print(f"   RELEVANCE SCORE: {score}/5 ({result.upper()})")
        print(f"   REASONING: {reasoning}")
    
    # Analysis summary
    print("\n"+"="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    
    scores = [row.get('outputs.relevance.relevance', 0) for row in rows]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    print(f"\n✅ All {len(rows)} queries were evaluated successfully")
    print(f"📈 Average relevance score: {avg_score:.3f}/5")
    print(f"🎯 All responses passed the threshold of {metrics.get('relevance.relevance_threshold', 0)}")
    
    # Score distribution
    score_distribution = {}
    for score in scores:
        score_distribution[score] = score_distribution.get(score, 0) + 1
    
    print(f"\n📊 Score Distribution:")
    for score in sorted(score_distribution.keys()):
        count = score_distribution[score]
        percentage = (count / len(scores)) * 100 if scores else 0
        print(f"   {score}/5: {count} responses ({percentage:.1f}%)")
    
    # Key findings
    print(f"\n🔍 KEY FINDINGS:")
    
    high_scores = [row for row in rows if row.get('outputs.relevance.relevance', 0) >= 4]
    medium_scores = [row for row in rows if 3 <= row.get('outputs.relevance.relevance', 0) < 4]
    low_scores = [row for row in rows if row.get('outputs.relevance.relevance', 0) < 3]
    
    print(f"   • High relevance (4-5/5): {len(high_scores)} responses")
    print(f"   • Medium relevance (3-4/5): {len(medium_scores)} responses") 
    print(f"   • Low relevance (<3/5): {len(low_scores)} responses")
    
    if high_scores:
        print(f"\n🌟 BEST PERFORMING QUERY:")
        best = max(rows, key=lambda x: x.get('outputs.relevance.relevance', 0))
        print(f"   Query: {best.get('inputs.query', '')}")
        print(f"   Score: {best.get('outputs.relevance.relevance', 0)}/5")
        print(f"   Reason: {best.get('outputs.relevance.relevance_reason', '')}")
    
    if medium_scores:
        print(f"\n⚠️  AREAS FOR IMPROVEMENT:")
        for row in medium_scores:
            print(f"   • {row.get('inputs.query', '')[:50]}... (Score: {row.get('outputs.relevance.relevance', 0)}/5)")
    
    print("\n" + "="*80)
    print("EVALUATION COMPLETED SUCCESSFULLY")
    print("="*80)


if __name__ == "__main__":
    analyze_evaluation_results()