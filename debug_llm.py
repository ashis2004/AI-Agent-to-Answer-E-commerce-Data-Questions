#!/usr/bin/env python3
"""
Debug the LLM client selection
"""

import sys

sys.path.append('.')

from src.ai.llm_client import FallbackLLM, get_llm_client


def debug_llm():
    print("Testing LLM Client Selection...")
    
    client = get_llm_client()
    print(f"Client type: {type(client)}")
    print(f"Is FallbackLLM: {isinstance(client, FallbackLLM)}")
    
    if hasattr(client, 'basic_queries'):
        print("Has basic_queries attribute")
    else:
        print("Does not have basic_queries attribute")
    
    # Test each question type
    questions = [
        "What is my total sales?",
        "Calculate the RoAS (Return on Ad Spend)",
        "Which product had the highest CPC (Cost Per Click)?"
    ]
    
    for question in questions:
        print(f"\nTesting: {question}")
        response = client.generate_response(question)
        print(f"Response: {response}")

if __name__ == "__main__":
    debug_llm()
