"""
Simple Agent Evaluation Script
Direct evaluation using individual evaluators to avoid dependency issues.
"""

import os
import json
from typing import Dict, List


def load_evaluation_data(file_path: str) -> List[Dict]:
    """Load evaluation data from JSONL file."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def evaluate_relevance_simple(query: str, response: str) -> Dict:
    """
    Simple relevance evaluation based on keyword matching and response completeness.
    This is a simplified version for demonstration purposes.
    """
    score = 0
    reasons = []
    
    # Check if response addresses the query
    query_lower = query.lower()
    response_lower = response.lower()
    
    if "weather" in query_lower:
        if "weather" in response_lower or "sunny" in response_lower or "temperature" in response_lower:
            score += 2
            reasons.append("Response mentions weather information")
        if any(temp in response_lower for temp in ["°c", "celsius", "degrees"]):
            score += 1
            reasons.append("Response includes temperature details")
    
    if "time" in query_lower:
        if "time" in response_lower or "am" in response_lower or "pm" in response_lower:
            score += 2
            reasons.append("Response mentions time information")
        if any(time_format in response_lower for time_format in [":", "utc", "2025"]):
            score += 1
            reasons.append("Response includes specific time details")
    
    # Check for location specificity
    locations = ["new york", "london", "paris", "tokyo"]
    for location in locations:
        if location in query_lower and location in response_lower:
            score += 1
            reasons.append(f"Response correctly addresses {location}")
    
    # Ensure response is not empty and provides some value
    if len(response.strip()) > 10:
        score += 1
        reasons.append("Response provides substantial information")
    
    # Normalize score to 1-5 scale
    final_score = min(5, max(1, score))
    
    return {
        "relevance": final_score,
        "relevance_reason": "; ".join(reasons) if reasons else "Basic response provided",
        "relevance_result": "pass" if final_score >= 3 else "fail",
        "relevance_threshold": 3
    }


def evaluate_tool_calls_simple(query: str, tool_calls: List[Dict], tool_definitions: List[Dict]) -> Dict:
    """
    Simple tool call accuracy evaluation.
    Checks if the right tools were called with appropriate parameters.
    """
    score = 1  # Start with minimum score
    reasons = []
    
    if not tool_calls:
        return {
            "tool_call_accuracy": 1,
            "tool_call_accuracy_reason": "No tool calls made",
            "tool_call_accuracy_result": "fail",
            "tool_call_accuracy_threshold": 3
        }
    
    query_lower = query.lower()
    
    # Check if appropriate tools were called
    tool_names = [tc.get("name", "") for tc in tool_calls]
    
    # Weather query expectations
    if "weather" in query_lower:
        if "get_weather" in tool_names:
            score += 2
            reasons.append("Correctly called get_weather for weather query")
            
            # Check weather tool parameters
            for tc in tool_calls:
                if tc.get("name") == "get_weather":
                    args = tc.get("arguments", {})
                    if "location" in args and args["location"]:
                        score += 1
                        reasons.append(f"Provided location parameter: {args['location']}")
                        
                        # Check if location matches query
                        expected_locations = ["new york", "london", "paris", "tokyo"]
                        for loc in expected_locations:
                            if loc in query_lower and loc.lower() in args["location"].lower():
                                score += 1
                                reasons.append(f"Location parameter matches query: {loc}")
                                break
        else:
            reasons.append("Weather query but get_weather not called")
    
    # Time query expectations
    if "time" in query_lower:
        if "get_time" in tool_names:
            score += 2
            reasons.append("Correctly called get_time for time query")
        else:
            reasons.append("Time query but get_time not called")
    
    # Check for unnecessary tool calls
    expected_tools = set()
    if "weather" in query_lower:
        expected_tools.add("get_weather")
    if "time" in query_lower:
        expected_tools.add("get_time")
    
    actual_tools = set(tool_names)
    unnecessary_tools = actual_tools - expected_tools
    if not unnecessary_tools:
        score += 1
        reasons.append("No unnecessary tool calls made")
    else:
        reasons.append(f"Unnecessary tool calls: {', '.join(unnecessary_tools)}")
    
    # Normalize score to 1-5 scale
    final_score = min(5, max(1, score))
    
    return {
        "tool_call_accuracy": final_score,
        "tool_call_accuracy_reason": "; ".join(reasons) if reasons else "Basic tool usage",
        "tool_call_accuracy_result": "pass" if final_score >= 3 else "fail",
        "tool_call_accuracy_threshold": 3
    }


def run_simple_evaluation():
    """Run simplified evaluation."""
    print("Starting Simple Agent Evaluation")
    print("=" * 50)
    
    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "evaluation_data.jsonl")
    
    if not os.path.exists(data_file):
        print("Error: evaluation_data.jsonl not found")
        print("Please run data_processor.py first.")
        return
    
    data = load_evaluation_data(data_file)
    print(f"Loaded {len(data)} traces for evaluation")
    
    results = []
    
    for i, trace in enumerate(data):
        print(f"\nEvaluating Trace {i+1}:")
        print(f"  Query: {trace['query']}")
        print(f"  Response: {trace['response']}")
        
        # Evaluate relevance
        relevance_result = evaluate_relevance_simple(trace['query'], trace['response'])
        
        # Evaluate tool calls
        tool_result = evaluate_tool_calls_simple(
            trace['query'], 
            trace['tool_calls'], 
            trace['tool_definitions']
        )
        
        # Combine results
        trace_result = {
            **trace,
            **relevance_result,
            **tool_result
        }
        results.append(trace_result)
        
        print(f"  Relevance: {relevance_result['relevance']}/5 ({relevance_result['relevance_result']})")
        print(f"  Tool Accuracy: {tool_result['tool_call_accuracy']}/5 ({tool_result['tool_call_accuracy_result']})")
    
    # Calculate aggregate metrics
    print("\n" + "=" * 50)
    print("EVALUATION RESULTS SUMMARY")
    print("=" * 50)
    
    relevance_scores = [r['relevance'] for r in results]
    tool_scores = [r['tool_call_accuracy'] for r in results]
    
    avg_relevance = sum(relevance_scores) / len(relevance_scores)
    avg_tool_accuracy = sum(tool_scores) / len(tool_scores)
    
    relevance_pass_rate = sum(1 for r in results if r['relevance_result'] == 'pass') / len(results)
    tool_pass_rate = sum(1 for r in results if r['tool_call_accuracy_result'] == 'pass') / len(results)
    
    print(f"\nRELEVANCE METRICS:")
    print(f"  Average Score: {avg_relevance:.2f}/5.0")
    print(f"  Pass Rate: {relevance_pass_rate:.1%}")
    print(f"  Best Score: {max(relevance_scores)}/5")
    print(f"  Worst Score: {min(relevance_scores)}/5")
    
    print(f"\nTOOL CALL ACCURACY METRICS:")
    print(f"  Average Score: {avg_tool_accuracy:.2f}/5.0")
    print(f"  Pass Rate: {tool_pass_rate:.1%}")
    print(f"  Best Score: {max(tool_scores)}/5")
    print(f"  Worst Score: {min(tool_scores)}/5")
    
    print(f"\nOVERALL PERFORMANCE:")
    overall_score = (avg_relevance + avg_tool_accuracy) / 2
    print(f"  Overall Score: {overall_score:.2f}/5.0")
    print(f"  Overall Pass Rate: {(relevance_pass_rate + tool_pass_rate) / 2:.1%}")
    
    # Detailed per-trace results
    print("\n" + "=" * 50)
    print("DETAILED PER-TRACE RESULTS")
    print("=" * 50)
    
    for i, result in enumerate(results):
        print(f"\nTrace {i+1} ({result['trace_id'][:8]}...):")
        print(f"  Query: {result['query']}")
        print(f"  Response: {result['response']}")
        print(f"  Relevance: {result['relevance']}/5 - {result['relevance_reason']}")
        print(f"  Tool Accuracy: {result['tool_call_accuracy']}/5 - {result['tool_call_accuracy_reason']}")
        print(f"  Tool Calls: {len(result['tool_calls'])} calls")
        for j, tc in enumerate(result['tool_calls']):
            print(f"    {j+1}. {tc['name']}({tc['arguments']})")
    
    # Save results
    output_file = os.path.join(script_dir, "evaluation_results_simple.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "summary": {
                "total_traces": len(results),
                "average_relevance": avg_relevance,
                "average_tool_accuracy": avg_tool_accuracy,
                "overall_score": overall_score,
                "relevance_pass_rate": relevance_pass_rate,
                "tool_pass_rate": tool_pass_rate
            },
            "detailed_results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nEvaluation completed! Results saved to: {output_file}")
    
    # Analysis and recommendations
    print("\n" + "=" * 50)
    print("ANALYSIS & RECOMMENDATIONS")
    print("=" * 50)
    
    if overall_score >= 4.0:
        print("Excellent Performance!")
        print("  The agent demonstrates strong relevance and tool usage accuracy.")
    elif overall_score >= 3.0:
        print("Good Performance with Room for Improvement")
        if avg_relevance < avg_tool_accuracy:
            print("  Focus on improving response relevance to user queries.")
        else:
            print("  Focus on improving tool selection and parameter accuracy.")
    else:
        print("Performance Needs Improvement")
        print("  Consider reviewing both response generation and tool usage logic.")
    
    print(f"\nKey Findings:")
    if avg_relevance >= 4.0:
        print("  [+] Responses are highly relevant to user queries")
    elif avg_relevance >= 3.0:
        print("  [+] Responses are generally relevant but could be more precise")
    else:
        print("  [-] Responses often miss key aspects of user queries")
    
    if avg_tool_accuracy >= 4.0:
        print("  [+] Tool usage is highly accurate and appropriate")
    elif avg_tool_accuracy >= 3.0:
        print("  [+] Tool usage is generally correct but could be optimized")
    else:
        print("  [-] Tool usage needs significant improvement")


if __name__ == "__main__":
    try:
        run_simple_evaluation()
    except Exception as e:
        print(f"❌ Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()