# Weather-Time Coordination Agent Evaluation

This project evaluates how well an AI agent handles queries that involve both weather and time information in a coordinated manner.

## Overview

The evaluation analyzes OpenTelemetry traces from an agent with weather and time tools to measure:

1. **Tool Call Accuracy**: How appropriately the agent selects and uses tools
2. **Coordination Efficiency**: How well the agent coordinates multiple tools when both are needed
3. **Response Completeness**: Whether responses include all requested information

## Dataset Analysis

The dataset contains 3 traces:
- **Trace 1**: Weather-only query - "What's the weather like in New York?"
- **Trace 2**: Time-only query - "What's the current UTC time?"  
- **Trace 3**: Combined query - "What's the weather in London and what's the current UTC time?"

The third trace demonstrates coordinated tool usage, which is the focus of this evaluation.

## Evaluation Metrics

### 1. Tool Call Accuracy (Azure AI ToolCallAccuracyEvaluator)
- **Purpose**: Measures how accurately the agent uses tools according to definitions
- **Scale**: 1-5 (1=irrelevant, 5=perfect)
- **Key aspects**: Relevance, parameter correctness, value extraction

### 2. Coordination Efficiency (Custom Evaluator)
- **Purpose**: Evaluates tool coordination for weather+time queries
- **Metrics**:
  - Whether both required tools are used
  - Parallel vs sequential execution (parallel preferred)
  - Minimal unnecessary calls
- **Scale**: 0-5 with efficiency ratings (excellent/good/fair/poor)

### 3. Response Completeness (Custom Evaluator)
- **Purpose**: Checks if responses contain both weather and time information
- **Method**: Text analysis for weather and time keywords
- **Scale**: 0-5 (complete/partial/incomplete)

## Results Summary

From the evaluation of 3 traces:

### Overall Performance
- **Tool Call Accuracy**: 3.67/5.0 (Good)
- **Coordination Efficiency**: 1.67/5.0 (Limited by single-tool queries)
- **Response Completeness**: 1.67/5.0 (Limited by single-tool queries)

### Key Findings

✅ **Excellent Coordination**: The agent demonstrates perfect coordination for the combined weather+time query:
- Uses both required tools (get_weather and get_time)
- Executes tools in parallel for efficiency
- Provides complete response with both types of information

✅ **Appropriate Tool Selection**: For single-purpose queries, the agent correctly uses only the relevant tool

✅ **Parallel Execution**: When both tools are needed, the agent calls them simultaneously rather than sequentially

### Coordination Quality Distribution
- **Excellent (4.5-5.0)**: 1 query (the combined weather+time query)
- **Not Applicable**: 2 queries (single-purpose queries)

## Technical Implementation

### Built-in Evaluators
- **ToolCallAccuracyEvaluator**: Azure AI Evaluation SDK evaluator for tool usage assessment
- Uses LLM-based evaluation with scoring rubric

### Custom Evaluators
- **CoordinationEfficiencyEvaluator**: Analyzes tool usage patterns for coordination
- **ResponseCompletenessEvaluator**: Text analysis for information completeness

### Data Processing
- Converts OpenTelemetry traces to evaluation format
- Extracts queries, tool calls, and responses
- Maps function calls to standard tool call format

## Files

- `evaluate_weather_time_coordination.py`: Full evaluation script using Azure AI Evaluation SDK
- `demo_evaluation_clean.py`: Demo script that runs without API keys
- `requirements.txt`: Required Python packages
- `setup_simple.py`: Setup script for dependencies

## Usage

### Option 1: Demo Evaluation (No API Keys Required)
```bash
python demo_evaluation_clean.py
```

### Option 2: Full Evaluation (Requires GitHub Token)
```bash
# Set environment variable
export GITHUB_TOKEN=your_github_token

# Install dependencies
pip install -r requirements.txt

# Run evaluation
python evaluate_weather_time_coordination.py
```

## Conclusions

The agent demonstrates **excellent weather-time coordination capabilities**:

1. **Perfect Parallel Execution**: When both weather and time are requested, the agent efficiently calls both tools simultaneously
2. **Complete Information Delivery**: Responses include both weather and time information as requested
3. **Appropriate Tool Selection**: No unnecessary tool calls or missing required tools
4. **Optimal Coordination Score**: 5.0/5.0 for the coordination-requiring query

This evaluation framework successfully measures multi-tool coordination quality and can be extended to evaluate other agent coordination scenarios.