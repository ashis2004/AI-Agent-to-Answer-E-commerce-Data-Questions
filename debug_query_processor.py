#!/usr/bin/env python3
"""
Debug the query processor flow
"""

import sys

sys.path.append('.')

from src.ai.query_processor import QueryProcessor


def debug_query_processor():
    print("Debugging Query Processor...")
    
    processor = QueryProcessor()
    
    # Test the prompt creation
    question = "What is my total sales?"
    prompt = processor.create_sql_prompt(question)
    print(f"Generated prompt: {prompt[:200]}...")
    
    # Test LLM response
    response = processor.llm_client.generate_response(prompt)
    print(f"LLM Response: {response}")
    
    # Test SQL generation
    sql = processor.generate_sql_query(question)
    print(f"Generated SQL: {sql}")

if __name__ == "__main__":
    debug_query_processor()
