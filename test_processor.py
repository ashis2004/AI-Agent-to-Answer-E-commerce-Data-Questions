#!/usr/bin/env python3
"""
Direct test of the query processor
"""

import os
import sys

sys.path.append('.')

from src.ai.query_processor import QueryProcessor


def test_processor():
    print("Testing Query Processor directly...")
    
    processor = QueryProcessor()
    
    questions = [
        "What is my total sales?",
        "Calculate the RoAS (Return on Ad Spend)",
        "Which product had the highest CPC (Cost Per Click)?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        
        try:
            result = processor.process_question(question)
            print(f"Success: {result['success']}")
            if result['success']:
                print(f"Answer: {processor.format_response(result)}")
                print(f"SQL: {result['query']}")
                print(f"Data: {result['data']}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_processor()
