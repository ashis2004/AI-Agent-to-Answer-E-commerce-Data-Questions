import asyncio
import json
import sqlite3
from typing import Any, Dict, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (FileResponse, HTMLResponse, JSONResponse,
                               StreamingResponse)
from pydantic import BaseModel

import config
from src.ai.query_processor import QueryProcessor
from src.visualization.charts import ChartGenerator


# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    include_chart: bool = False

class QuestionResponse(BaseModel):
    answer: str
    data: list
    query: str
    success: bool
    chart_url: Optional[str] = ""

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce AI Agent",
    description="AI-powered agent for answering e-commerce data questions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
query_processor = QueryProcessor()
chart_generator = ChartGenerator()

@app.get("/")
async def root():
    """Serve the web interface"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Web interface not found</h1>", status_code=404)

@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {"message": "E-commerce AI Agent API", "status": "running"}

@app.get("/charts/{filename}")
async def serve_chart(filename: str):
    """Serve generated chart files"""
    import os
    chart_path = f"static/charts/{filename}"
    if os.path.exists(chart_path):
        return FileResponse(chart_path)
    else:
        raise HTTPException(status_code=404, detail="Chart not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM product_eligibility")
        product_count = cursor.fetchone()[0]
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "products_in_db": product_count,
            "llm_available": query_processor.llm_client.is_available() if hasattr(query_processor.llm_client, 'is_available') else False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get counts from each table
        cursor.execute("SELECT COUNT(*) FROM product_eligibility")
        eligibility_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM product_ad_sales")
        ad_sales_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM product_total_sales")
        total_sales_count = cursor.fetchone()[0]
        
        # Get total sales sum
        cursor.execute("SELECT SUM(total_sales) FROM product_total_sales")
        total_sales_sum = cursor.fetchone()[0] or 0
        
        # Get total ad spend
        cursor.execute("SELECT SUM(ad_spend) FROM product_ad_sales")
        total_ad_spend = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "tables": {
                "product_eligibility": eligibility_count,
                "product_ad_sales": ad_sales_count,
                "product_total_sales": total_sales_count
            },
            "metrics": {
                "total_sales": total_sales_sum,
                "total_ad_spend": total_ad_spend,
                "estimated_roas": total_sales_sum / total_ad_spend if total_ad_spend > 0 else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question about the data"""
    try:
        # Process the question with SQL query included
        result = query_processor.process_query_with_sql(request.question)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Format the response
        formatted_answer = query_processor.format_response(result)
        
        # Generate chart if requested
        chart_url = None
        if request.include_chart and result["data"]:
            try:
                chart_url = chart_generator.create_chart(result["data"], request.question)
            except Exception as chart_error:
                print(f"Chart generation failed: {chart_error}")
        
        return QuestionResponse(
            answer=formatted_answer,
            data=result["data"],
            query=result.get("sql_query", ""),
            success=True,
            chart_url=chart_url or ""
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")

@app.post("/ask/stream")
async def ask_question_stream(request: QuestionRequest):
    """Ask a question with streaming response"""
    
    async def generate_streaming_response():
        try:
            # First, show the question processing
            yield f"data: {json.dumps({'type': 'status', 'content': '🤔 Processing your question...'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Process the question to get SQL and data
            result = query_processor.process_query_with_sql(request.question)
            
            if not result["success"]:
                yield f"data: {json.dumps({'type': 'error', 'content': result['error']})}\n\n"
                return
            
            # Show the generated SQL query
            yield f"data: {json.dumps({'type': 'sql', 'content': result.get('sql_query', '')})}\n\n"
            await asyncio.sleep(1)
            
            # Format the response
            formatted_answer = query_processor.format_response(result)
            
            # Stream the response character by character
            yield f"data: {json.dumps({'type': 'answer_start'})}\n\n"
            for char in formatted_answer:
                yield f"data: {json.dumps({'type': 'token', 'content': char})}\n\n"
                await asyncio.sleep(0.03)  # Add delay for typing effect
            
            # Generate chart if requested
            chart_url = None
            if request.include_chart:
                try:
                    yield f"data: {json.dumps({'type': 'status', 'content': '📊 Generating chart...'})}\n\n"
                    chart_url = chart_generator.create_chart(result["data"], request.question)
                except Exception as chart_error:
                    print(f"Chart generation failed: {chart_error}")
            
            # Send completion signal with chart
            completion_data = {
                'type': 'complete',
                'data': result['data'], 
                'query': result.get('sql_query', '')
            }
            if chart_url:
                completion_data['chart_url'] = chart_url
                
            yield f"data: {json.dumps(completion_data)}\n\n"
            yield f"data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_streaming_response(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/sample-questions")
async def get_sample_questions():
    """Get sample questions for testing"""
    return {
        "sample_questions": [
            "What is my total sales?",
            "Calculate the RoAS (Return on Ad Spend)",
            "Which product had the highest CPC (Cost Per Click)?",
            "Show me the top performing products by sales",
            "What is the average conversion rate?",
            "Which products are eligible for advertising?",
            "What is the total ad spend across all campaigns?",
            "Show me products with the highest organic sales"
        ]
    }

# Include error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )
