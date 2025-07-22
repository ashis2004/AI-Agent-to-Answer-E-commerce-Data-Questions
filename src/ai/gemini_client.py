import google.generativeai as genai
import requests
import json
import config

class GeminiLLMClient:
    """Google Gemini AI client for natural language to SQL conversion"""
    
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.available = True
        
    def generate_sql_query(self, question: str, schema_info: str) -> str:
        """Generate SQL query using Gemini AI"""
        try:
            prompt = f"""
You are an expert SQL assistant for an e-commerce database. Convert the user's natural language question into a precise SQL query.

DATABASE SCHEMA:
{schema_info}

IMPORTANT RULES:
1. Only use tables and columns that exist in the schema
2. Return ONLY the SQL query, no explanations
3. Use proper SQL syntax for SQLite
4. For aggregations, include appropriate GROUP BY clauses
5. Use meaningful column aliases for calculated fields

USER QUESTION: {question}

SQL QUERY:"""

            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # Clean up the response (remove markdown formatting if present)
            if sql_query.startswith('```sql'):
                sql_query = sql_query[6:]
            if sql_query.endswith('```'):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to simple SQL generation
            return self._fallback_sql_generation(question)
    
    def _fallback_sql_generation(self, question: str) -> str:
        """Fallback SQL generation for common questions"""
        question_lower = question.lower()
        
        if "total sales" in question_lower:
            return "SELECT SUM(total_sales) as total_sales FROM product_total_sales"
        elif "roas" in question_lower:
            return """
            SELECT 
                SUM(ad_sales) / SUM(ad_spend) as roas,
                SUM(ad_sales) as total_ad_sales,
                SUM(ad_spend) as total_ad_spend
            FROM product_ad_sales 
            WHERE ad_spend > 0
            """
        elif "highest cpc" in question_lower or "cost per click" in question_lower:
            return """
            SELECT product_id, cpc, ad_spend, clicks 
            FROM product_ad_sales 
            WHERE clicks > 0 
            ORDER BY cpc DESC 
            LIMIT 10
            """
        elif "high clicks" in question_lower and "low conversion" in question_lower:
            return """
            SELECT product_id, clicks, conversion_rate, ad_spend, ad_sales
            FROM product_ad_sales 
            WHERE clicks > (SELECT AVG(clicks) FROM product_ad_sales)
            AND conversion_rate < (SELECT AVG(conversion_rate) FROM product_ad_sales)
            ORDER BY clicks DESC, conversion_rate ASC
            LIMIT 10
            """
        else:
            return "SELECT * FROM product_total_sales LIMIT 10"
    
    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        return self.available

class OllamaLLMClient:
    """Ollama LLM client as backup"""
    
    def __init__(self):
        self.base_url = config.LLM_BASE_URL
        self.model = config.LLM_MODEL
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_sql_query(self, question: str, schema_info: str) -> str:
        """Generate SQL query using Ollama"""
        if not self.available:
            return self._fallback_sql_generation(question)
            
        try:
            prompt = f"""Convert this question to SQL for an e-commerce database:
            
Database Schema:
{schema_info}

Question: {question}

Return only the SQL query:"""

            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(f"{self.base_url}/api/generate", json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return self._fallback_sql_generation(question)
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._fallback_sql_generation(question)
    
    def _fallback_sql_generation(self, question: str) -> str:
        """Same fallback as Gemini"""
        question_lower = question.lower()
        
        if "total sales" in question_lower:
            return "SELECT SUM(total_sales) as total_sales FROM product_total_sales"
        elif "roas" in question_lower:
            return """
            SELECT 
                SUM(ad_sales) / SUM(ad_spend) as roas,
                SUM(ad_sales) as total_ad_sales,
                SUM(ad_spend) as total_ad_spend
            FROM product_ad_sales 
            WHERE ad_spend > 0
            """
        elif "highest cpc" in question_lower:
            return """
            SELECT product_id, cpc, ad_spend, clicks 
            FROM product_ad_sales 
            WHERE clicks > 0 
            ORDER BY cpc DESC 
            LIMIT 10
            """
        else:
            return "SELECT * FROM product_total_sales LIMIT 10"

class FallbackLLMClient:
    """Pattern-based fallback for offline use"""
    
    def __init__(self):
        self.available = True
    
    def generate_sql_query(self, question: str, schema_info: str) -> str:
        """Generate SQL using pattern matching"""
        # Extract the actual user question from complex prompts
        if "User Question:" in question:
            question = question.split("User Question:")[-1].strip()
        
        question_lower = question.lower()
        
        if "total sales" in question_lower:
            return "SELECT SUM(total_sales) as total_sales FROM product_total_sales"
        elif "roas" in question_lower:
            return """
            SELECT 
                SUM(ad_sales) / SUM(ad_spend) as roas,
                SUM(ad_sales) as total_ad_sales,
                SUM(ad_spend) as total_ad_spend
            FROM product_ad_sales 
            WHERE ad_spend > 0
            """
        elif "highest cpc" in question_lower or "cost per click" in question_lower:
            return """
            SELECT product_id, cpc, ad_spend, clicks 
            FROM product_ad_sales 
            WHERE clicks > 0 
            ORDER BY cpc DESC 
            LIMIT 10
            """
        elif "high clicks" in question_lower and "low conversion" in question_lower:
            return """
            SELECT product_id, clicks, conversion_rate, ad_spend, ad_sales
            FROM product_ad_sales 
            WHERE clicks > (SELECT AVG(clicks) FROM product_ad_sales)
            AND conversion_rate < (SELECT AVG(conversion_rate) FROM product_ad_sales)
            ORDER BY clicks DESC, conversion_rate ASC
            LIMIT 10
            """
        elif "top performing" in question_lower or "best product" in question_lower:
            return """
            SELECT product_id, total_sales, total_orders 
            FROM product_total_sales 
            ORDER BY total_sales DESC 
            LIMIT 10
            """
        elif "eligible" in question_lower:
            return """
            SELECT product_id, product_name, is_eligible_for_ads, eligibility_reason 
            FROM product_eligibility 
            WHERE is_eligible_for_ads = 1
            LIMIT 10
            """
        elif "ad spend" in question_lower:
            return """
            SELECT SUM(ad_spend) as total_ad_spend, COUNT(*) as campaigns 
            FROM product_ad_sales
            """
        else:
            return "SELECT * FROM product_total_sales ORDER BY total_sales DESC LIMIT 10"
    
    def is_available(self) -> bool:
        return True

def get_llm_client():
    """Get the best available LLM client"""
    # Try Gemini first
    try:
        gemini_client = GeminiLLMClient()
        print("Using Gemini AI for query generation")
        return gemini_client
    except Exception as e:
        print(f"Gemini not available: {e}")
    
    # Try Ollama as backup
    try:
        ollama_client = OllamaLLMClient()
        if ollama_client.available:
            print("Using Ollama for query generation")
            return ollama_client
    except Exception as e:
        print(f"Ollama not available: {e}")
    
    # Use fallback
    print("Using fallback LLM for query generation")
    return FallbackLLMClient()
