"""
Test script for the E-commerce AI Agent
Run this to test the API endpoints and functionality
"""

import json
import time
from typing import Any, Dict

import requests


class APITester:
    """Test the E-commerce AI Agent API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def test_health(self) -> Dict[str, Any]:
        """Test health endpoint"""
        print("Testing health endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            result = {
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else response.text
            }
            print(f"✓ Health check: {result['status_code']}")
            return result
        except Exception as e:
            print(f"✗ Health check failed: {e}")
            return {"error": str(e)}
    
    def test_stats(self) -> Dict[str, Any]:
        """Test stats endpoint"""
        print("Testing stats endpoint...")
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=10)
            result = {
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else response.text
            }
            print(f"✓ Stats: {result['status_code']}")
            return result
        except Exception as e:
            print(f"✗ Stats failed: {e}")
            return {"error": str(e)}
    
    def test_question(self, question: str, include_chart: bool = False) -> Dict[str, Any]:
        """Test ask endpoint with a specific question"""
        print(f"Testing question: '{question}'...")
        try:
            payload = {
                "question": question,
                "include_chart": include_chart
            }
            response = requests.post(
                f"{self.base_url}/ask",
                json=payload,
                timeout=30
            )
            result = {
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else response.text
            }
            
            if response.status_code == 200:
                print(f"✓ Question answered successfully")
                answer = result['response'].get('answer', '')
                print(f"Answer: {answer[:100]}{'...' if len(answer) > 100 else ''}")
            else:
                print(f"✗ Question failed: {result['status_code']}")
            
            return result
        except Exception as e:
            print(f"✗ Question failed: {e}")
            return {"error": str(e)}
    
    def test_streaming(self, question: str) -> Dict[str, Any]:
        """Test streaming endpoint"""
        print(f"Testing streaming for: '{question}'...")
        try:
            payload = {
                "question": question,
                "include_chart": False
            }
            response = requests.post(
                f"{self.base_url}/ask/stream",
                json=payload,
                stream=True,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✓ Streaming response:")
                chunks = []
                for line in response.iter_lines():
                    if line:
                        try:
                            # Parse SSE format
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                data = json.loads(line_str[6:])
                                if 'content' in data:
                                    chunks.append(data['content'])
                                    print(data['content'], end='', flush=True)
                                elif data.get('done'):
                                    print("\n✓ Streaming completed")
                                    break
                        except json.JSONDecodeError:
                            continue
                
                return {"status_code": 200, "chunks": chunks}
            else:
                print(f"✗ Streaming failed: {response.status_code}")
                return {"status_code": response.status_code, "error": response.text}
        
        except Exception as e:
            print(f"✗ Streaming failed: {e}")
            return {"error": str(e)}
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print("=" * 60)
        print("E-commerce AI Agent - Comprehensive Test Suite")
        print("=" * 60)
        
        # Test 1: Health check
        print("\n1. Health Check")
        print("-" * 20)
        health_result = self.test_health()
        
        # Test 2: Stats
        print("\n2. Database Stats")
        print("-" * 20)
        stats_result = self.test_stats()
        
        # Test 3: Required questions
        print("\n3. Required Questions")
        print("-" * 20)
        
        required_questions = [
            "What is my total sales?",
            "Calculate the RoAS (Return on Ad Spend)",
            "Which product had the highest CPC (Cost Per Click)?"
        ]
        
        question_results = []
        for i, question in enumerate(required_questions, 1):
            print(f"\n3.{i}. {question}")
            result = self.test_question(question, include_chart=True)
            question_results.append(result)
            time.sleep(1)  # Brief pause between requests
        
        # Test 4: Additional questions
        print("\n4. Additional Questions")
        print("-" * 20)
        
        additional_questions = [
            "Show me the top performing products",
            "What is the average conversion rate?",
            "Which products are eligible for advertising?"
        ]
        
        for i, question in enumerate(additional_questions, 1):
            print(f"\n4.{i}. {question}")
            result = self.test_question(question)
            time.sleep(1)
        
        # Test 5: Streaming
        print("\n5. Streaming Response Test")
        print("-" * 20)
        streaming_result = self.test_streaming("What is my total sales?")
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        
        # Health check
        total_tests += 1
        if not health_result.get('error') and health_result.get('status_code') == 200:
            passed_tests += 1
            print("✓ Health check: PASSED")
        else:
            print("✗ Health check: FAILED")
        
        # Stats
        total_tests += 1
        if not stats_result.get('error') and stats_result.get('status_code') == 200:
            passed_tests += 1
            print("✓ Stats endpoint: PASSED")
        else:
            print("✗ Stats endpoint: FAILED")
        
        # Required questions
        for i, result in enumerate(question_results):
            total_tests += 1
            if not result.get('error') and result.get('status_code') == 200:
                passed_tests += 1
                print(f"✓ Required question {i+1}: PASSED")
            else:
                print(f"✗ Required question {i+1}: FAILED")
        
        # Streaming
        total_tests += 1
        if not streaming_result.get('error') and streaming_result.get('status_code') == 200:
            passed_tests += 1
            print("✓ Streaming: PASSED")
        else:
            print("✗ Streaming: FAILED")
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({(passed_tests/total_tests)*100:.1f}%)")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": (passed_tests/total_tests)*100
        }

def main():
    """Main test function"""
    print("Starting API tests...")
    print("Make sure the server is running on http://localhost:8000")
    
    # Wait for user confirmation
    input("Press Enter to start tests (or Ctrl+C to cancel)...")
    
    tester = APITester()
    results = tester.run_comprehensive_test()
    
    print(f"\nTesting completed with {results['success_rate']:.1f}% success rate")

if __name__ == "__main__":
    main()
