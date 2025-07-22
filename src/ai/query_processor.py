import re
import sqlite3
from typing import Any, Dict, List, Optional

import config
from src.ai.llm_client import get_llm_client


class QueryProcessor:
    """Processes natural language questions and converts them to SQL queries"""
    
    def __init__(self):
        self.llm_client = get_llm_client()
        self.database_schema = self._get_database_schema()
    
    def _get_database_schema(self) -> str:
        """Get database schema information"""
        schema_info = """
        Database Schema:
        
        Table: product_eligibility
        - product_id (TEXT): Unique product identifier
        - product_name (TEXT): Name of the product
        - category (TEXT): Product category
        - subcategory (TEXT): Product subcategory
        - brand (TEXT): Product brand
        - is_eligible_for_ads (INTEGER): 1 if eligible for ads, 0 otherwise
        - eligibility_reason (TEXT): Reason for eligibility status
        
        Table: product_ad_sales
        - product_id (TEXT): Unique product identifier
        - campaign_name (TEXT): Name of advertising campaign
        - ad_spend (REAL): Amount spent on advertising
        - impressions (INTEGER): Number of ad impressions
        - clicks (INTEGER): Number of ad clicks
        - ctr (REAL): Click-through rate (%)
        - cpc (REAL): Cost per click
        - ad_sales (REAL): Sales generated from ads
        - ad_orders (INTEGER): Orders generated from ads
        - conversion_rate (REAL): Conversion rate (%)
        - acos (REAL): Advertising Cost of Sales (%)
        
        Table: product_total_sales
        - product_id (TEXT): Unique product identifier
        - total_sales (REAL): Total sales amount
        - total_orders (INTEGER): Total number of orders
        - organic_sales (REAL): Sales not from ads
        - organic_orders (INTEGER): Orders not from ads
        - sessions (INTEGER): Number of product page sessions
        - session_percentage (REAL): Session percentage
        - page_views (INTEGER): Number of page views
        - page_view_percentage (REAL): Page view percentage
        - buy_box_percentage (REAL): Buy box percentage
        """
        return schema_info
    
    def create_sql_prompt(self, question: str) -> str:
        """Create a prompt for SQL generation"""
        prompt = f"""
You are a SQL expert. Given the following database schema and a user question, generate a SQL query that answers the question.

{self.database_schema}

Important notes:
- RoAS (Return on Ad Spend) = ad_sales / ad_spend
- Use proper JOINs when accessing data from multiple tables
- Always use proper table aliases
- Return only the SQL query, no explanations
- Ensure the query is syntactically correct for SQLite

User Question: {question}

SQL Query:
"""
        return prompt
    
    def generate_sql_query(self, question: str) -> str:
        """Generate SQL query from natural language question using Gemini AI"""
        try:
            # Use the new Gemini client's generate_sql_query method
            if hasattr(self.llm_client, 'generate_sql_query'):
                sql_query = self.llm_client.generate_sql_query(question, self.database_schema)
                return sql_query
            else:
                # Fallback for legacy clients
                prompt = self.create_sql_prompt(question)
                response = self.llm_client.generate_response(prompt)
                if response:
                    sql_query = self._extract_sql_from_response(response)
                    return sql_query
                else:
                    return self._fallback_query(question)
        except Exception as e:
            print(f"Error generating SQL: {e}")
            return self._fallback_query(question)
    
    def _extract_sql_from_response(self, response: str) -> str:
        """Extract SQL query from LLM response"""
        # Remove common prefixes and clean up the response
        response = response.strip()
        
        # Remove markdown code blocks if present
        if '```sql' in response:
            response = response.split('```sql')[1].split('```')[0]
        elif '```' in response:
            response = response.split('```')[1].split('```')[0]
        
        # Remove common prefixes
        prefixes_to_remove = [
            'SQL Query:', 'Query:', 'SELECT', 'sql query:', 'query:'
        ]
        
        for prefix in prefixes_to_remove:
            if response.upper().startswith(prefix.upper()):
                response = response[len(prefix):].strip()
                break
        
        # If response doesn't start with SELECT, add it back
        if not response.upper().startswith('SELECT'):
            response = 'SELECT ' + response
        
        return response.strip()
    
    def _fallback_query(self, question: str) -> str:
        """Generate fallback query for common questions"""
        question_lower = question.lower()
        
        if "total sales" in question_lower:
            return "SELECT SUM(total_sales) as total_sales FROM product_total_sales WHERE total_sales IS NOT NULL"
        elif "roas" in question_lower or "return on ad spend" in question_lower:
            return """SELECT 
                ROUND(SUM(ad_sales) / NULLIF(SUM(ad_spend), 0), 2) as roas,
                SUM(ad_sales) as total_ad_sales,
                SUM(ad_spend) as total_ad_spend
            FROM product_ad_sales 
            WHERE ad_spend > 0 AND ad_sales IS NOT NULL"""
        elif "highest cpc" in question_lower or "cost per click" in question_lower:
            return """SELECT 
                product_id, 
                cpc, 
                ad_spend, 
                clicks 
            FROM product_ad_sales 
            WHERE cpc IS NOT NULL AND cpc > 0
            ORDER BY cpc DESC 
            LIMIT 10"""
        elif "conversion rate" in question_lower:
            return """SELECT 
                product_id,
                conversion_rate,
                clicks,
                ad_orders
            FROM product_ad_sales 
            WHERE conversion_rate IS NOT NULL
            ORDER BY conversion_rate DESC 
            LIMIT 10"""
        elif "top performing" in question_lower or "best product" in question_lower:
            return """SELECT 
                product_id, 
                total_sales, 
                total_orders 
            FROM product_total_sales 
            WHERE total_sales IS NOT NULL
            ORDER BY total_sales DESC 
            LIMIT 10"""
        elif "eligible" in question_lower:
            return """SELECT 
                product_id, 
                product_name, 
                is_eligible_for_ads, 
                eligibility_reason 
            FROM product_eligibility 
            WHERE is_eligible_for_ads = 1
            LIMIT 10"""
        elif "ad spend" in question_lower:
            return """SELECT 
                SUM(ad_spend) as total_ad_spend, 
                COUNT(*) as campaigns,
                AVG(ad_spend) as avg_ad_spend
            FROM product_ad_sales 
            WHERE ad_spend IS NOT NULL"""
        else:
            return """SELECT 
                product_id, 
                total_sales, 
                total_orders 
            FROM product_total_sales 
            WHERE total_sales IS NOT NULL
            ORDER BY total_sales DESC 
            LIMIT 10"""
    
    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query and return results"""
        try:
            conn = sqlite3.connect(config.DATABASE_PATH)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            # Convert to list of dictionaries
            result_list = []
            if results:
                columns = [description[0] for description in cursor.description]
                for row in results:
                    result_list.append(dict(zip(columns, row)))
            
            conn.close()
            
            return {
                "success": True,
                "data": result_list,
                "query": sql_query,
                "row_count": len(result_list)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": sql_query,
                "data": []
            }
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """Process a question end-to-end"""
        # Generate SQL query
        sql_query = self.generate_sql_query(question)
        
        # Execute query
        result = self.execute_query(sql_query)
        
        # Add original question to result
        result["question"] = question
        
        return result
    
    def format_response(self, result: Dict[str, Any]) -> str:
        """Format the result into a human-readable response"""
        if not result["success"]:
            return f"Sorry, I encountered an error: {result['error']}"
        
        data = result["data"]
        question = result.get("question", "")
        
        if not data:
            return "No data found for your question."
        
        # Format based on question type
        question_lower = question.lower()
        
        if "total sales" in question_lower:
            total = data[0].get("total_sales", 0)
            return f"The total sales amount is ${total:,.2f}"
        
        elif "roas" in question_lower:
            roas = data[0].get("roas", 0)
            return f"The Return on Ad Spend (RoAS) is {roas:.2f}. This means for every $1 spent on advertising, you generated ${roas:.2f} in sales."
        
        elif "highest cpc" in question_lower:
            if data:
                product = data[0].get("product_name", "Unknown")
                cpc = data[0].get("cpc", 0)
                return f"The product with the highest Cost Per Click (CPC) is '{product}' with a CPC of ${cpc:.2f}"
        
        # Generic formatting for other queries
        if len(data) == 1 and len(data[0]) == 1:
            # Single value result
            key = list(data[0].keys())[0]
            value = data[0][key]
            return f"The {key.replace('_', ' ')} is {value}"
        
        # Multiple rows or columns
        response = f"Here are the results for your question:\n\n"
        for i, row in enumerate(data[:5]):  # Limit to first 5 results
            response += f"{i+1}. "
            for key, value in row.items():
                if isinstance(value, float):
                    response += f"{key.replace('_', ' ').title()}: {value:.2f}, "
                else:
                    response += f"{key.replace('_', ' ').title()}: {value}, "
            response = response.rstrip(", ") + "\n"
        
        if len(data) > 5:
            response += f"\n... and {len(data) - 5} more results."
        
        return response

    def process_query_with_sql(self, question: str) -> Dict[str, Any]:
        """Process a question and return both SQL query and results"""
        # Generate SQL query
        sql_query = self.generate_sql_query(question)
        
        # Execute the query
        result = self.execute_query(sql_query)
        
        # Add SQL query and question to result
        result["sql_query"] = sql_query
        result["question"] = question
        
        return result
