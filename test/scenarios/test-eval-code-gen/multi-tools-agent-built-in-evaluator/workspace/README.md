# Agent Evaluation Setup

This directory contains a comprehensive evaluation framework for assessing AI agent performance using Azure AI Evaluation SDK.

## Overview

The evaluation measures two key aspects:
1. **Response Relevance**: How well agent responses address user queries
2. **Tool Call Accuracy**: Correctness of tool selection and parameter usage

## Files

- `dataset.json` - Original trace data from agent interactions
- `data_processor.py` - Converts traces to evaluation-ready JSONL format
- `evaluate_agent.py` - Main evaluation script using Azure AI Evaluation SDK
- `evaluation_data.jsonl` - Processed data for evaluation (generated)
- `evaluation_results/` - Output directory for results (generated)

## Quick Start

1. **Install dependencies**:
```bash
pip install azure-ai-evaluation
```

2. **Set up environment**:
```bash
export GITHUB_TOKEN=your_github_token_here
```

3. **Process the data**:
```bash
python data_processor.py
```

4. **Run evaluation**:
```bash
python evaluate_agent.py
```

## Evaluation Metrics

### Response Relevance (1-5 scale)
- **5**: Highly relevant, directly addresses the query
- **4**: Mostly relevant with minor gaps
- **3**: Somewhat relevant but may miss key points
- **2**: Partially relevant with significant gaps
- **1**: Irrelevant or off-topic

### Tool Call Accuracy (1-5 scale)
- **5**: Perfect tool selection and parameter usage
- **4**: Mostly correct with minor issues
- **3**: Generally correct but with some unnecessary calls
- **2**: Partially correct tool usage
- **1**: Incorrect or irrelevant tool calls

## Dataset Analysis

The dataset contains 3 agent interaction traces:

1. **Weather Query**: "What's the weather like in New York?"
   - Expected: Single `get_weather` call with location="New York"
   
2. **Time Query**: "What's the current UTC time?"
   - Expected: Single `get_time` call with no parameters
   
3. **Combined Query**: "What's the weather in London and what's the current UTC time?"
   - Expected: Two calls - `get_weather` with location="London" and `get_time`

## Results Interpretation

The evaluation generates:
- **Aggregate metrics**: Overall performance across all traces
- **Per-trace results**: Detailed scores for each interaction
- **Pass/fail rates**: Based on configurable thresholds
- **Detailed reasoning**: Why scores were assigned

## Customization

You can customize the evaluation by:
- Adjusting thresholds in the evaluators
- Adding custom evaluators for domain-specific metrics
- Modifying tool definitions to match your agent's capabilities
- Adding more sophisticated analysis in the results processing