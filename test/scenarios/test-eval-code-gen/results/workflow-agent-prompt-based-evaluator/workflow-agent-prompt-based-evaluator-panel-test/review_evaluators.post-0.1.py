# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import json
import logging
from typing import Dict, Union, Optional
from azure.ai.evaluation import OpenAIModelConfiguration

logger = logging.getLogger(__name__)


class ReviewConstructivenessEvaluator:
    """
    Evaluator to measure how constructive and helpful reviewer feedback is.
    
    This evaluator uses an LLM to assess whether feedback is constructive,
    offers specific suggestions for improvement, and maintains a helpful tone.
    """
    
    def __init__(self, model_config: OpenAIModelConfiguration):
        """
        Initialize the constructiveness evaluator.
        
        :param model_config: Configuration for the LLM model to use for evaluation
        :type model_config: OpenAIModelConfiguration
        """
        self.model_config = model_config
        from openai import OpenAI
        
        # Set up OpenAI client
        self.client = OpenAI(
            base_url=model_config.base_url,
            api_key=model_config.api_key
        )
    
    def __call__(self, *, original_content: str, reviewer_feedback: str, **kwargs) -> Dict[str, Union[str, float]]:
        """
        Execute the evaluation.
        
        :param original_content: The original content being reviewed
        :type original_content: str
        :param reviewer_feedback: The reviewer's feedback to evaluate
        :type reviewer_feedback: str
        :return: Dictionary containing the evaluation results
        :rtype: Dict[str, Union[str, float]]
        """
        try:
            prompt = f"""You are an expert evaluator assessing the constructiveness of reviewer feedback.

Please evaluate the following reviewer feedback based on these criteria:

**CONSTRUCTIVENESS CRITERIA:**
1. **Helpful Tone**: Is the feedback delivered in a respectful, encouraging, and supportive manner?
2. **Specific Suggestions**: Does the feedback provide concrete, actionable suggestions for improvement?
3. **Balanced Perspective**: Does the feedback acknowledge strengths while addressing areas for improvement?
4. **Clear Reasoning**: Are the suggestions well-explained with clear reasoning?
5. **Forward-Looking**: Does the feedback help the creator improve future work?

**ORIGINAL CONTENT:**
{original_content}

**REVIEWER FEEDBACK:**
{reviewer_feedback}

**EVALUATION INSTRUCTIONS:**
Rate the constructiveness of this feedback on a scale of 1-5:
- 1: Not constructive (harsh, vague, or unhelpful)
- 2: Minimally constructive (some issues identified but lacks helpful guidance)
- 3: Moderately constructive (provides some useful suggestions)
- 4: Constructive (provides clear, helpful suggestions with good reasoning)
- 5: Highly constructive (exceptional feedback that is specific, balanced, and encouraging)

Respond with a JSON object containing:
- "score": A number from 1 to 5
- "reasoning": A detailed explanation of your evaluation (2-3 sentences)

Example response format:
{{"score": 4, "reasoning": "The feedback demonstrates high constructiveness by providing specific suggestions for improvement while maintaining an encouraging tone. The reviewer clearly explains the reasoning behind each suggestion and balances criticism with recognition of strengths."}}"""
            
            # Get response from the model
            response = self.client.chat.completions.create(
                model=self.model_config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            
            return {
                "constructiveness": result.get("score", 0),
                "constructiveness_reasoning": result.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing constructiveness evaluation response: {e}")
            return {
                "constructiveness": 0,
                "constructiveness_reasoning": "Error in evaluation"
            }


class ReviewActionabilityEvaluator:
    """
    Evaluator to measure how actionable and specific reviewer feedback is.
    
    This evaluator assesses whether feedback provides concrete steps
    that the content creator can implement to improve their work.
    """
    
    def __init__(self, model_config: OpenAIModelConfiguration):
        """
        Initialize the actionability evaluator.
        
        :param model_config: Configuration for the LLM model to use for evaluation
        :type model_config: OpenAIModelConfiguration
        """
        self.model_config = model_config
        from openai import OpenAI
        
        # Set up OpenAI client
        self.client = OpenAI(
            base_url=model_config.base_url,
            api_key=model_config.api_key
        )
    
    def __call__(self, *, original_content: str, reviewer_feedback: str, **kwargs) -> Dict[str, Union[str, float]]:
        """
        Execute the evaluation.
        
        :param original_content: The original content being reviewed
        :type original_content: str
        :param reviewer_feedback: The reviewer's feedback to evaluate
        :type reviewer_feedback: str
        :return: Dictionary containing the evaluation results
        :rtype: Dict[str, Union[str, float]]
        """
        try:
            prompt = f"""You are an expert evaluator assessing the actionability of reviewer feedback.

Please evaluate the following reviewer feedback based on these criteria:

**ACTIONABILITY CRITERIA:**
1. **Specific Instructions**: Does the feedback provide clear, step-by-step guidance?
2. **Concrete Examples**: Are there specific examples or instances mentioned?
3. **Practical Implementation**: Can the suggestions be easily understood and implemented?
4. **Measurable Changes**: Are the recommended improvements specific enough to be measured?
5. **Clear Next Steps**: Does the feedback indicate exactly what the creator should do?

**ORIGINAL CONTENT:**
{original_content}

**REVIEWER FEEDBACK:**
{reviewer_feedback}

**EVALUATION INSTRUCTIONS:**
Rate the actionability of this feedback on a scale of 1-5:
- 1: Not actionable (vague suggestions that are difficult to implement)
- 2: Minimally actionable (general guidance but lacks specific steps)
- 3: Moderately actionable (some specific suggestions but could be clearer)
- 4: Actionable (clear, specific suggestions that can be readily implemented)
- 5: Highly actionable (exceptionally specific guidance with clear implementation steps)

Respond with a JSON object containing:
- "score": A number from 1 to 5
- "reasoning": A detailed explanation of your evaluation (2-3 sentences)

Example response format:
{{"score": 4, "reasoning": "The feedback provides highly actionable suggestions by identifying specific phrases to revise and offering concrete alternatives. The reviewer gives clear implementation steps that the writer can immediately apply to improve their work."}}"""
            
            # Get response from the model
            response = self.client.chat.completions.create(
                model=self.model_config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            
            return {
                "actionability": result.get("score", 0),
                "actionability_reasoning": result.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing actionability evaluation response: {e}")
            return {
                "actionability": 0,
                "actionability_reasoning": "Error in evaluation"
            }


class ReviewQualityEvaluator:
    """
    Evaluator to measure overall quality of reviewer feedback.
    
    This evaluator provides a comprehensive assessment combining multiple
    aspects of feedback quality including clarity, usefulness, and professionalism.
    """
    
    def __init__(self, model_config: OpenAIModelConfiguration):
        """
        Initialize the overall quality evaluator.
        
        :param model_config: Configuration for the LLM model to use for evaluation
        :type model_config: OpenAIModelConfiguration
        """
        self.model_config = model_config
        from openai import OpenAI
        
        # Set up OpenAI client
        self.client = OpenAI(
            base_url=model_config.base_url,
            api_key=model_config.api_key
        )
    
    def __call__(self, *, original_content: str, reviewer_feedback: str, **kwargs) -> Dict[str, Union[str, float]]:
        """
        Execute the evaluation.
        
        :param original_content: The original content being reviewed
        :type original_content: str
        :param reviewer_feedback: The reviewer's feedback to evaluate
        :type reviewer_feedback: str
        :return: Dictionary containing the evaluation results
        :rtype: Dict[str, Union[str, float]]
        """
        try:
            prompt = f"""You are an expert evaluator assessing the overall quality of reviewer feedback.

Please evaluate the following reviewer feedback holistically based on these criteria:

**OVERALL QUALITY CRITERIA:**
1. **Clarity**: Is the feedback easy to understand and well-organized?
2. **Relevance**: Does the feedback address important aspects of the content?
3. **Depth**: Does the feedback show thoughtful analysis rather than surface-level comments?
4. **Professionalism**: Is the feedback delivered in a professional, appropriate manner?
5. **Value**: Would this feedback genuinely help improve the work?
6. **Completeness**: Does the feedback address the content comprehensively?

**ORIGINAL CONTENT:**
{original_content}

**REVIEWER FEEDBACK:**
{reviewer_feedback}

**EVALUATION INSTRUCTIONS:**
Rate the overall quality of this feedback on a scale of 1-5:
- 1: Poor quality (unclear, irrelevant, or unprofessional)
- 2: Below average quality (some issues with clarity or relevance)
- 3: Average quality (adequate feedback but room for improvement)
- 4: Good quality (clear, relevant, and helpful feedback)
- 5: Excellent quality (exceptional feedback that is clear, insightful, and highly valuable)

Respond with a JSON object containing:
- "score": A number from 1 to 5
- "reasoning": A detailed explanation of your evaluation (2-3 sentences)

Example response format:
{{"score": 4, "reasoning": "The feedback demonstrates good overall quality with clear, relevant suggestions that address key aspects of the content. The reviewer provides thoughtful analysis with professional tone, though could be slightly more comprehensive in addressing all elements."}}"""
            
            # Get response from the model
            response = self.client.chat.completions.create(
                model=self.model_config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            
            return {
                "overall_quality": result.get("score", 0),
                "overall_quality_reasoning": result.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing overall quality evaluation response: {e}")
            return {
                "overall_quality": 0,
                "overall_quality_reasoning": "Error in evaluation"
            }