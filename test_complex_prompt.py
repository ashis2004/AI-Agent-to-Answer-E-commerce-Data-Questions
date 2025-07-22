#!/usr/bin/env python3
"""
Test the prompt that gets sent to FallbackLLM
"""

import sys

sys.path.append('.')

from src.ai.llm_client import FallbackLLM


def test_prompt():
    print("Testing what happens when FallbackLLM receives complex prompt...")
    
    fallback = FallbackLLM()
    
    # This is what the query processor sends
    complex_prompt = """
You are a SQL expert. Given the following database schema and a user question, generate a SQL query that answers the question.

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
        

Important notes:
- RoAS (Return on Ad Spend) = ad_sales / ad_spend
- Use proper JOINs when accessing data from multiple tables
- Always use proper table aliases
- Return only the SQL query, no explanations
- Ensure the query is syntactically correct for SQLite

User Question: Calculate the RoAS (Return on Ad Spend)

SQL Query:
"""
    
    print("FallbackLLM response to complex prompt:")
    response = fallback.generate_response(complex_prompt)
    print(repr(response))

if __name__ == "__main__":
    test_prompt()
