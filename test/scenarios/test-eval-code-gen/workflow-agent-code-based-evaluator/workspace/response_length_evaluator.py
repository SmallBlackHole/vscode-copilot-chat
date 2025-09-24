"""
Custom Response Length Evaluator for Azure AI Evaluation SDK.

This evaluator measures the response length using both character count and word count.
It follows the Azure AI Evaluation SDK pattern with __init__ and __call__ methods.
"""

import re
from typing import Dict, Any


class ResponseLengthEvaluator:
    """
    Custom code-based evaluator that measures response length metrics.
    
    This evaluator calculates:
    - Character count (including spaces)
    - Word count (excluding punctuation)
    - Character count without spaces
    - Average word length
    """
    
    def __init__(self):
        """
        Initialize the ResponseLengthEvaluator.
        
        For custom code-based evaluators, __init__ typically handles configuration
        but for response length measurement, no special configuration is needed.
        """
        pass
    
    def __call__(self, *, response: str, **kwargs) -> Dict[str, Any]:
        """
        Evaluate the response length metrics.
        
        Args:
            response (str): The response text to measure
            **kwargs: Additional parameters (ignored for this evaluator)
            
        Returns:
            Dict[str, Any]: Dictionary containing length metrics
        """
        if not isinstance(response, str):
            response = str(response) if response is not None else ""
        
        # Basic character count
        char_count = len(response)
        
        # Character count without spaces
        char_count_no_spaces = len(response.replace(' ', ''))
        
        # Word count (split by whitespace and filter out empty strings)
        words = [word for word in response.split() if word.strip()]
        word_count = len(words)
        
        # Clean word count (removing punctuation for more accurate count)
        clean_words = []
        for word in words:
            # Remove punctuation and keep only alphanumeric characters
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word:
                clean_words.append(clean_word)
        
        clean_word_count = len(clean_words)
        
        # Average word length (excluding punctuation)
        avg_word_length = (
            sum(len(word) for word in clean_words) / clean_word_count
            if clean_word_count > 0 else 0
        )
        
        # Response length category
        if char_count < 100:
            length_category = "short"
        elif char_count < 500:
            length_category = "medium"
        elif char_count < 1000:
            length_category = "long"
        else:
            length_category = "very_long"
        
        return {
            "response_char_count": char_count,
            "response_char_count_no_spaces": char_count_no_spaces,
            "response_word_count": word_count,
            "response_clean_word_count": clean_word_count,
            "response_avg_word_length": round(avg_word_length, 2),
            "response_length_category": length_category
        }


# Example usage for testing
if __name__ == "__main__":
    evaluator = ResponseLengthEvaluator()
    
    # Test with sample response
    sample_response = "The poem is thoughtful and evocative, effectively capturing the emotional and intellectual challenges of learning a language as an adult."
    
    result = evaluator(response=sample_response)
    print("Sample evaluation result:")
    for key, value in result.items():
        print(f"  {key}: {value}")