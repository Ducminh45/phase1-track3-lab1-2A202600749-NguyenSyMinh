from __future__ import annotations
import os
import time
from typing import Tuple
from openai import OpenAI
from pydantic import BaseModel
from .schemas import QAExample, JudgeResult, ReflectionEntry
from .prompts import ACTOR_SYSTEM, EVALUATOR_SYSTEM, REFLECTOR_SYSTEM
from .utils import normalize_answer

FAILURE_MODE_BY_QID = {}

# Make sure OPENAI_API_KEY is set in environment or pass it explicitly.
api_key = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=api_key) if api_key else None

def actor_answer(example: QAExample, attempt_id: int, agent_type: str, reflection_memory: list[str]) -> Tuple[str, int, int]:
    if not client:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    context_str = "\n".join([f"Source: {c.title}\n{c.text}" for c in example.context])
    user_prompt = f"Context:\n{context_str}\n\nQuestion: {example.question}\n"
    
    if reflection_memory:
        user_prompt += f"\nReflection History and Strategies to use:\n" + "\n".join(reflection_memory)
        
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ACTOR_SYSTEM},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
    )
    latency_ms = int((time.time() - start_time) * 1000)
    tokens = response.usage.total_tokens if response.usage else 0
    
    return response.choices[0].message.content.strip(), tokens, latency_ms

def evaluator(example: QAExample, answer: str) -> Tuple[JudgeResult, int, int]:
    if not client:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    if normalize_answer(example.gold_answer) in normalize_answer(answer) or normalize_answer(answer) in normalize_answer(example.gold_answer):
        return JudgeResult(score=1, reason="Match after normalization."), 0, 0
        
    user_prompt = f"Context:\n" + "\n".join([f"Source: {c.title}\n{c.text}" for c in example.context])
    user_prompt += f"\n\nQuestion: {example.question}"
    user_prompt += f"\nGold Answer: {example.gold_answer}"
    user_prompt += f"\nPredicted Answer: {answer}"
    
    start_time = time.time()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EVALUATOR_SYSTEM},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        response_format=JudgeResult,
    )
    latency_ms = int((time.time() - start_time) * 1000)
    tokens = response.usage.total_tokens if response.usage else 0
    
    return response.choices[0].message.parsed, tokens, latency_ms

def reflector(example: QAExample, attempt_id: int, judge: JudgeResult) -> Tuple[ReflectionEntry, int, int]:
    if not client:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    user_prompt = f"Question: {example.question}\n"
    user_prompt += f"Context:\n" + "\n".join([f"Source: {c.title}\n{c.text}" for c in example.context])
    user_prompt += f"\n\nEvaluator's Feedback:\nScore: {judge.score}\nReason: {judge.reason}\nMissing Evidence: {judge.missing_evidence}\nSpurious Claims: {judge.spurious_claims}"
    
    start_time = time.time()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": REFLECTOR_SYSTEM},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        response_format=ReflectionEntry,
    )
    latency_ms = int((time.time() - start_time) * 1000)
    tokens = response.usage.total_tokens if response.usage else 0
    
    reflection = response.choices[0].message.parsed
    reflection.attempt_id = attempt_id
    return reflection, tokens, latency_ms
