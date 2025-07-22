import asyncio
import json
from typing import AsyncGenerator


class StreamingResponseGenerator:
    """Handles streaming responses for real-time interaction"""
    
    def __init__(self, query_processor):
        self.query_processor = query_processor
    
    async def stream_question_response(self, question: str) -> AsyncGenerator[str, None]:
        """Stream the response to a question with typing effect"""
        try:
            # Process the question
            result = self.query_processor.process_question(question)
            
            if not result["success"]:
                yield f"data: {json.dumps({'error': result['error'], 'done': True})}\n\n"
                return
            
            # Format the response
            formatted_answer = self.query_processor.format_response(result)
            
            # Send initial metadata
            yield f"data: {json.dumps({'type': 'start', 'question': question})}\n\n"
            
            # Stream the response with typing effect
            for i, char in enumerate(formatted_answer):
                yield f"data: {json.dumps({'type': 'content', 'content': char, 'position': i})}\n\n"
                await asyncio.sleep(0.03)  # Typing effect delay
            
            # Send final data
            yield f"data: {json.dumps({
                'type': 'complete',
                'data': result['data'],
                'query': result['query'],
                'row_count': result['row_count'],
                'done': True
            })}\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e), 'done': True})}\n\n"
    
    async def stream_with_llm(self, question: str) -> AsyncGenerator[str, None]:
        """Stream response directly from LLM for more natural interaction"""
        try:
            # Create SQL prompt
            sql_prompt = self.query_processor.create_sql_prompt(question)
            
            # Stream SQL generation
            yield f"data: {json.dumps({'type': 'thinking', 'message': 'Analyzing your question...'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Generate SQL
            sql_query = self.query_processor.generate_sql_query(question)
            
            yield f"data: {json.dumps({'type': 'sql_generated', 'query': sql_query})}\n\n"
            await asyncio.sleep(0.3)
            
            # Execute query
            yield f"data: {json.dumps({'type': 'executing', 'message': 'Fetching data from database...'})}\n\n"
            result = self.query_processor.execute_query(sql_query)
            
            if not result["success"]:
                yield f"data: {json.dumps({'type': 'error', 'error': result['error'], 'done': True})}\n\n"
                return
            
            # Stream formatted response
            yield f"data: {json.dumps({'type': 'responding', 'message': 'Formatting response...'})}\n\n"
            await asyncio.sleep(0.3)
            
            formatted_answer = self.query_processor.format_response(result)
            
            # Stream the final answer
            for i, char in enumerate(formatted_answer):
                yield f"data: {json.dumps({'type': 'content', 'content': char, 'position': i})}\n\n"
                await asyncio.sleep(0.02)
            
            # Send completion
            yield f"data: {json.dumps({
                'type': 'complete',
                'data': result['data'],
                'query': sql_query,
                'row_count': result['row_count'],
                'done': True
            })}\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e), 'done': True})}\n\n"
