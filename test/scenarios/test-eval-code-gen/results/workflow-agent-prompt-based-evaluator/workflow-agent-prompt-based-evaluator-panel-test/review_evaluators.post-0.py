# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import json
import logging
from typing import Dict, Union, Optional
from azure.ai.evaluation._evaluators._common import PromptyEvaluatorBase
from azure.ai.evaluation._common._experimental import experimental
from azure.ai.evaluation._model_configurations import OpenAIModelConfiguration

logger = logging.getLogger(__name__)


@experimental
class ReviewConstructivenessEvaluator(PromptyEvaluatorBase[Union[str, float]]):
    """
    Evaluator to measure how constructive and helpful reviewer feedback is.
    
    This evaluator uses an LLM to assess whether feedback is constructive,
    offers specific suggestions for improvement, and maintains a helpful tone.
    """
    
    _RESULT_KEY = "constructiveness"
    
    def __init__(self, model_config: OpenAIModelConfiguration):
        """
        Initialize the constructiveness evaluator.
        
        :param model_config: Configuration for the LLM model to use for evaluation
        :type model_config: OpenAIModelConfiguration
        """
        super().__init__(model_config=model_config)
        self._evaluation_prompt = self._create_evaluation_prompt()
    
    def _create_evaluation_prompt(self) -> str:
        """Create the prompt template for evaluating constructiveness."""
        return """You are an expert evaluator assessing the constructiveness of reviewer feedback.

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

    async def _flow(self, *, original_content: str, reviewer_feedback: str, **kwargs) -> Dict[str, Union[str, float]]:
        """
        Execute the evaluation flow.
        
        :param original_content: The original content being reviewed
        :type original_content: str
        :param reviewer_feedback: The reviewer's feedback to evaluate
        :type reviewer_feedback: str
        :return: Dictionary containing the evaluation results
        :rtype: Dict[str, Union[str, float]]
        """
        try:
            # Format the prompt with the provided content
            formatted_prompt = self._evaluation_prompt.format(
                original_content=original_content,
                reviewer_feedback=reviewer_feedback
            )
            
            # Get response from the model
            response = await self._model_client.complete(
                messages=[{"role": "user", "content": formatted_prompt}]
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            
            return {
                self._RESULT_KEY: result.get("score", 0),
                f"{self._RESULT_KEY}_reasoning": result.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing constructiveness evaluation response: {e}")
            return {
                self._RESULT_KEY: 0,
                f"{self._RESULT_KEY}_reasoning": "Error in evaluation"
            }


@experimental  
class ReviewActionabilityEvaluator(PromptyEvaluatorBase[Union[str, float]]):
    """
    Evaluator to measure how actionable and specific reviewer feedback is.
    
    This evaluator assesses whether feedback provides concrete steps
    that the content creator can implement to improve their work.
    """
    
    _RESULT_KEY = "actionability"
    
    def __init__(self, model_config: OpenAIModelConfiguration):
        """
        Initialize the actionability evaluator.
        
        :param model_config: Configuration for the LLM model to use for evaluation
        :type model_config: OpenAIModelConfiguration
        """
        super().__init__(model_config=model_config)
        self._evaluation_prompt = self._create_evaluation_prompt()
    
    def _create_evaluation_prompt(self) -> str:
        """Create the prompt template for evaluating actionability."""
        return """You are an expert evaluator assessing the actionability of reviewer feedback.

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

    async def _flow(self, *, original_content: str, reviewer_feedback: str, **kwargs) -> Dict[str, Union[str, float]]:
        """
        Execute the evaluation flow.
        
        :param original_content: The original content being reviewed
        :type original_content: str
        :param reviewer_feedback: The reviewer's feedback to evaluate
        :type reviewer_feedback: str
        :return: Dictionary containing the evaluation results
        :rtype: Dict[str, Union[str, float]]
        """
        try:
            # Format the prompt with the provided content
            formatted_prompt = self._evaluation_prompt.format(
                original_content=original_content,
                reviewer_feedback=reviewer_feedback
            )
            
            # Get response from the model
            response = await self._model_client.complete(
                messages=[{"role": "user", "content": formatted_prompt}]
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            
            return {
                self._RESULT_KEY: result.get("score", 0),
                f"{self._RESULT_KEY}_reasoning": result.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing actionability evaluation response: {e}")
            return {
                self._RESULT_KEY: 0,
                f"{self._RESULT_KEY}_reasoning": "Error in evaluation"
            }


@experimental
class ReviewQualityEvaluator(PromptyEvaluatorBase[Union[str, float]]):
    """
    Evaluator to measure overall quality of reviewer feedback.
    
    This evaluator provides a comprehensive assessment combining multiple
    aspects of feedback quality including clarity, usefulness, and professionalism.
    """
    
    _RESULT_KEY = "overall_quality"
    
    def __init__(self, model_config: OpenAIModelConfiguration):
        """
        Initialize the overall quality evaluator.
        
        :param model_config: Configuration for the LLM model to use for evaluation
        :type model_config: OpenAIModelConfiguration
        """
        super().__init__(model_config=model_config)
        self._evaluation_prompt = self._create_evaluation_prompt()
    
    def _create_evaluation_prompt(self) -> str:
        """Create the prompt template for evaluating overall quality."""
        return """You are an expert evaluator assessing the overall quality of reviewer feedback.

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

    async def _flow(self, *, original_content: str, reviewer_feedback: str, **kwargs) -> Dict[str, Union[str, float]]:
        """
        Execute the evaluation flow.
        
        :param original_content: The original content being reviewed
        :type original_content: str
        :param reviewer_feedback: The reviewer's feedback to evaluate
        :type reviewer_feedback: str
        :return: Dictionary containing the evaluation results
        :rtype: Dict[str, Union[str, float]]
        """
        try:
            # Format the prompt with the provided content
            formatted_prompt = self._evaluation_prompt.format(
                original_content=original_content,
                reviewer_feedback=reviewer_feedback
            )
            
            # Get response from the model
            response = await self._model_client.complete(
                messages=[{"role": "user", "content": formatted_prompt}]
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            
            return {
                self._RESULT_KEY: result.get("score", 0),
                f"{self._RESULT_KEY}_reasoning": result.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error parsing overall quality evaluation response: {e}")
            return {
                self._RESULT_KEY: 0,
                f"{self._RESULT_KEY}_reasoning": "Error in evaluation"
            }