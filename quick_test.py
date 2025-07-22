#!/usr/bin/env python3
"""
Quick test of the E-commerce AI Agent
Tests the three required questions
"""

import json

import requests


def test_question(question):
    print(f'\nTesting: {question}')
    print('='*60)
    
    try:
        response = requests.post('http://localhost:8000/ask', 
                               json={'question': question, 'include_chart': False},
                               timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print(f'✓ Answer: {result["answer"]}')
            print(f'✓ SQL Query: {result["query"]}')
            print(f'✓ Data: {result["data"]}')
            print(f'✓ Success: {result["success"]}')
        else:
            print(f'✗ Error: {response.status_code} - {response.text}')
    
    except Exception as e:
        print(f'✗ Exception: {e}')
    
    print('='*60)

def main():
    print("🚀 E-COMMERCE AI AGENT - QUICK TEST")
    print("Testing the three required questions...")
    
    # Test server health first
    try:
        health_response = requests.get('http://localhost:8000/health', timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✓ Server is healthy")
            print(f"✓ Database: {health_data.get('database')}")
            print(f"✓ Products: {health_data.get('products_in_db')}")
            print(f"✓ LLM Available: {health_data.get('llm_available')}")
        else:
            print(f"✗ Server health check failed: {health_response.status_code}")
            return
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        print("Please make sure the server is running with: python main.py")
        return
    
    # Test the required questions
    required_questions = [
        "What is my total sales?",
        "Calculate the RoAS (Return on Ad Spend)",
        "Which product had the highest CPC (Cost Per Click)?"
    ]
    
    for question in required_questions:
        test_question(question)
    
    print("\n🎉 TESTING COMPLETED!")
    print("All three required questions have been tested.")
    print("\nFor a full demo, run: python demo.py")
    print("For comprehensive testing, run: python test_api.py")

if __name__ == "__main__":
    main()
