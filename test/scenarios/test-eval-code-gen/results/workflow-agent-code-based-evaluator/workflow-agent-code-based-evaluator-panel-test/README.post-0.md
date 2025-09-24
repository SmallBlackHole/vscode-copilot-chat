# Agent Response Length Evaluation

This project evaluates agent responses by measuring their length characteristics using the Azure AI Evaluation SDK with a custom ResponseLengthEvaluator.

## Overview

The evaluation system measures:
- **Character count** (including and excluding spaces)
- **Word count** (raw and clean)
- **Average word length**
- **Response length categories** (short, medium, long, very_long)

## Files Structure

```
workspace/
├── dataset.json                    # Original agent conversation data
├── convert_data.py                 # Convert JSON to JSONL format
├── evaluation_data.jsonl           # Converted data for evaluation
├── response_length_evaluator.py    # Custom length evaluator
├── evaluate_response_length.py     # Main evaluation script
├── evaluation_results.json         # Detailed evaluation results
├── generate_report.py              # Human-readable summary report
├── .env                           # Environment variables (GitHub token)
└── README.md                      # This file
```

## Prerequisites

1. **Python packages**: Install required dependencies
   ```bash
   pip install azure-ai-evaluation python-dotenv
   ```

2. **GitHub Token**: Set your GitHub token in `.env` file:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

## Usage

### 1. Convert Dataset to JSONL Format
```bash
python convert_data.py
```
This transforms `dataset.json` into `evaluation_data.jsonl` format required by Azure AI Evaluation SDK.

### 2. Run Response Length Evaluation
```bash
python evaluate_response_length.py
```
This executes the evaluation using:
- Custom ResponseLengthEvaluator
- GitHub-hosted gpt-4.1-mini model
- Azure AI Evaluation SDK's `evaluate()` API

### 3. Generate Summary Report
```bash
python generate_report.py
```
This creates a human-readable summary of the evaluation results.

## Evaluation Results

### Sample Results Summary

**Aggregate Metrics (Average across all responses):**
- Average Character Count: 875.3
- Average Word Count: 131.0
- Average Word Length: 5.36 characters

**Length Distribution:**
- Long: 2 responses (66.7%)
- Very_long: 1 responses (33.3%)

**Key Insights:**
- The agent produces comprehensive responses with significant length variation (524-1479 chars)
- Response length adapts appropriately to different request types
- Uses balanced vocabulary complexity

## Custom Evaluator Details

The `ResponseLengthEvaluator` follows Azure AI Evaluation SDK patterns:

```python
class ResponseLengthEvaluator:
    def __init__(self):
        pass
    
    def __call__(self, *, response: str, **kwargs) -> Dict[str, Any]:
        # Measures character count, word count, avg word length, etc.
        return {
            "response_char_count": char_count,
            "response_word_count": word_count,
            "response_length_category": category,
            # ... other metrics
        }
```

## Configuration

The evaluation uses GitHub-hosted models:
- **Model**: gpt-4.1-mini (cost-effective)
- **Endpoint**: https://models.github.ai/inference
- **Authentication**: GitHub Personal Access Token

## Output Files

1. **evaluation_results.json**: Raw evaluation data with individual and aggregate metrics
2. **Summary report**: Human-readable analysis printed to console

## Extending the Evaluation

To add more metrics:
1. Modify `ResponseLengthEvaluator.__call__()` to return additional metrics
2. Update the summary report generator as needed
3. Re-run the evaluation

## Architecture

This implementation follows Azure AI Evaluation SDK best practices:
- ✅ Uses the unified `evaluate()` API for execution
- ✅ Implements custom code-based evaluator with proper structure
- ✅ Handles JSONL data format requirements
- ✅ Provides comprehensive column mapping configuration
- ✅ Generates both row-level and aggregate metrics automatically