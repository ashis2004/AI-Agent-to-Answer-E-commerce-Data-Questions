import sqlite3
from pathlib import Path

import pandas as pd

import config
from src.database.models import create_tables, engine


def initialize_database():
    """Initialize the database with tables"""
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")

def load_sample_data():
    """Load sample data for testing purposes"""
    print("Loading sample data...")
    
    # Sample product eligibility data
    eligibility_data = [
        {
            'product_id': 'PROD001',
            'product_name': 'Wireless Bluetooth Headphones',
            'category': 'Electronics',
            'subcategory': 'Audio',
            'brand': 'TechBrand',
            'is_eligible_for_ads': 1,
            'eligibility_reason': 'Meets all advertising criteria'
        },
        {
            'product_id': 'PROD002',
            'product_name': 'Gaming Mechanical Keyboard',
            'category': 'Electronics',
            'subcategory': 'Computer Accessories',
            'brand': 'GamerPro',
            'is_eligible_for_ads': 1,
            'eligibility_reason': 'Approved for advertising'
        },
        {
            'product_id': 'PROD003',
            'product_name': 'Organic Cotton T-Shirt',
            'category': 'Clothing',
            'subcategory': 'Men\'s Apparel',
            'brand': 'EcoWear',
            'is_eligible_for_ads': 0,
            'eligibility_reason': 'Pending brand verification'
        }
    ]
    
    # Sample ad sales data
    ad_sales_data = [
        {
            'product_id': 'PROD001',
            'campaign_name': 'Headphones Summer Sale',
            'ad_spend': 500.00,
            'impressions': 25000,
            'clicks': 750,
            'ctr': 3.0,
            'cpc': 0.67,
            'ad_sales': 2250.00,
            'ad_orders': 45,
            'conversion_rate': 6.0,
            'acos': 22.22
        },
        {
            'product_id': 'PROD002',
            'campaign_name': 'Gaming Gear Promotion',
            'ad_spend': 800.00,
            'impressions': 40000,
            'clicks': 1200,
            'ctr': 3.0,
            'cpc': 0.67,
            'ad_sales': 3600.00,
            'ad_orders': 60,
            'conversion_rate': 5.0,
            'acos': 22.22
        }
    ]
    
    # Sample total sales data
    total_sales_data = [
        {
            'product_id': 'PROD001',
            'total_sales': 5000.00,
            'total_orders': 100,
            'organic_sales': 2750.00,
            'organic_orders': 55,
            'sessions': 2500,
            'session_percentage': 15.5,
            'page_views': 5000,
            'page_view_percentage': 12.5,
            'buy_box_percentage': 85.0
        },
        {
            'product_id': 'PROD002',
            'total_sales': 7200.00,
            'total_orders': 120,
            'organic_sales': 3600.00,
            'organic_orders': 60,
            'sessions': 3000,
            'session_percentage': 18.0,
            'page_views': 6000,
            'page_view_percentage': 15.0,
            'buy_box_percentage': 90.0
        },
        {
            'product_id': 'PROD003',
            'total_sales': 1500.00,
            'total_orders': 50,
            'organic_sales': 1500.00,
            'organic_orders': 50,
            'sessions': 800,
            'session_percentage': 8.5,
            'page_views': 1600,
            'page_view_percentage': 7.0,
            'buy_box_percentage': 75.0
        }
    ]
    
    # Load data into database
    conn = sqlite3.connect(config.DATABASE_PATH)
    
    # Load eligibility data
    df_eligibility = pd.DataFrame(eligibility_data)
    df_eligibility.to_sql('product_eligibility', conn, if_exists='replace', index=False)
    
    # Load ad sales data
    df_ad_sales = pd.DataFrame(ad_sales_data)
    df_ad_sales.to_sql('product_ad_sales', conn, if_exists='replace', index=False)
    
    # Load total sales data
    df_total_sales = pd.DataFrame(total_sales_data)
    df_total_sales.to_sql('product_total_sales', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Sample data loaded successfully!")

def load_csv_data(csv_files_dict):
    """
    Load data from CSV files
    csv_files_dict should be like:
    {
        'eligibility': 'path/to/eligibility.csv',
        'ad_sales': 'path/to/ad_sales.csv',
        'total_sales': 'path/to/total_sales.csv'
    }
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    
    for table_name, csv_path in csv_files_dict.items():
        if Path(csv_path).exists():
            df = pd.read_csv(csv_path)
            
            # Map table names to database table names
            table_mapping = {
                'eligibility': 'product_eligibility',
                'ad_sales': 'product_ad_sales',
                'total_sales': 'product_total_sales'
            }
            
            db_table_name = table_mapping.get(table_name, table_name)
            df.to_sql(db_table_name, conn, if_exists='replace', index=False)
            print(f"Loaded {len(df)} records into {db_table_name}")
        else:
            print(f"CSV file not found: {csv_path}")
    
    conn.close()

if __name__ == "__main__":
    initialize_database()
    load_sample_data()
