#!/usr/bin/env python3
"""
Debug the FallbackLLM pattern matching
"""

import sys

sys.path.append('.')

from src.ai.llm_client import FallbackLLM


def debug_fallback():
    print("Debugging FallbackLLM pattern matching...")
    
    fallback = FallbackLLM()
    
    # Test questions
    questions = [
        "What is my total sales?",
        "Calculate the RoAS (Return on Ad Spend)",
        "Which product had the highest CPC (Cost Per Click)?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print(f"Lowercase: {question.lower()}")
        
        # Check what matches
        question_lower = question.lower()
        if "total sales" in question_lower:
            print("Matches: total sales")
        elif "roas" in question_lower or "return on ad spend" in question_lower:
            print("Matches: roas")
        elif "highest cpc" in question_lower or "cost per click" in question_lower:
            print("Matches: highest cpc")
        else:
            print("Matches: default")
        
        response = fallback.generate_response(question)
        print(f"Response: {response[:100]}...")

if __name__ == "__main__":
    debug_fallback()
