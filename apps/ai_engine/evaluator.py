from openai import OpenAI
from django.conf import settings
import json


def get_openai_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def build_evaluation_prompt(
    question_title,
    question_description,
    expected_answer,
    candidate_answer,
    difficulty
):
    prompt = f"""
You are an expert technical interviewer evaluating a candidate's answer.

QUESTION: {question_title}
DESCRIPTION: {question_description}
DIFFICULTY: {difficulty}

EXPECTED ANSWER:
{expected_answer}

CANDIDATE'S ANSWER:
{candidate_answer}

Evaluate the candidate's answer and respond with ONLY a JSON object in this exact format:
{{
    "score": <number between 0 and 10>,
    "feedback": "<detailed feedback explaining the score>",
    "strengths": ["<strength 1>", "<strength 2>"],
    "improvements": ["<improvement 1>", "<improvement 2>"],
    "keywords_matched": ["<keyword 1>", "<keyword 2>"],
    "keywords_missed": ["<keyword 1>", "<keyword 2>"],
    "confidence_level": "<low/medium/high>"
}}

Scoring guide:
0-2: Completely wrong or no answer
3-4: Partially correct, major gaps
5-6: Mostly correct, some gaps
7-8: Good answer, minor gaps
9-10: Excellent, comprehensive answer

Return ONLY the JSON. No extra text.
"""
    return prompt


def evaluate_answer(
    question_title,
    question_description,
    expected_answer,
    candidate_answer,
    difficulty='medium'
):
    if not candidate_answer or len(candidate_answer.strip()) < 10:
        return {
            'score': 0.0,
            'feedback': 'No answer provided',
            'strengths': [],
            'improvements': ['Please provide a detailed answer'],
            'keywords_matched': [],
            'keywords_missed': [],
            'confidence_level': 'high',
            'tokens_used': 0,
            'model_used': 'mock',
        }

    expected_words = set(expected_answer.lower().split())
    candidate_words = set(candidate_answer.lower().split())
    matched = expected_words.intersection(candidate_words)
    score = min(10.0, len(matched) / max(len(expected_words), 1) * 10)
    score = round(score, 1)

    return {
        'score': score,
        'feedback': f'Answer evaluated. You matched {len(matched)} key concepts.',
        'strengths': ['Attempted the answer', 'Used relevant terminology'],
        'improvements': ['Add more detail', 'Include examples'],
        'keywords_matched': list(matched)[:5],
        'keywords_missed': list(expected_words - candidate_words)[:5],
        'confidence_level': 'medium',
        'tokens_used': 0,
        'model_used': 'mock',
    }