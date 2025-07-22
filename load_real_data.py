from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from src.database.models import (ProductAdSales, ProductEligibility,
                                 ProductTotalSales, SessionLocal, engine)


def load_real_datasets():
    """Load the actual CSV datasets into the database"""
    
    # Create database session
    session = SessionLocal()
    
    try:
        print("Loading real e-commerce datasets...")
        
        # Clear existing data
        session.query(ProductEligibility).delete()
        session.query(ProductAdSales).delete()
        session.query(ProductTotalSales).delete()
        session.commit()
        
        # Load Product Eligibility data
        print("Loading Product Eligibility data...")
        eligibility_df = pd.read_csv('dataset/Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv')
        
        for _, row in eligibility_df.iterrows():
            eligibility = ProductEligibility(
                eligibility_datetime_utc=str(row['eligibility_datetime_utc']),
                item_id=int(row['item_id']),
                eligibility=bool(row['eligibility']),
                message=str(row['message']) if pd.notna(row['message']) else None
            )
            session.add(eligibility)
        
        print(f"Loaded {len(eligibility_df)} eligibility records")
        
        # Load Product Ad Sales data
        print("Loading Product Ad Sales data...")
        ad_sales_df = pd.read_csv('dataset/Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv')
        
        for _, row in ad_sales_df.iterrows():
            ad_sales = ProductAdSales(
                date=pd.to_datetime(row['date']).date(),
                item_id=int(row['item_id']),
                ad_sales=float(row['ad_sales']),
                impressions=int(row['impressions']),
                ad_spend=float(row['ad_spend']),
                clicks=int(row['clicks']),
                units_sold=int(row['units_sold'])
            )
            session.add(ad_sales)
        
        print(f"Loaded {len(ad_sales_df)} ad sales records")
        
        # Load Product Total Sales data
        print("Loading Product Total Sales data...")
        total_sales_df = pd.read_csv('dataset/Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv')
        
        for _, row in total_sales_df.iterrows():
            total_sales = ProductTotalSales(
                date=pd.to_datetime(row['date']).date(),
                item_id=int(row['item_id']),
                total_sales=float(row['total_sales']),
                total_units_ordered=int(row['total_units_ordered'])
            )
            session.add(total_sales)
        
        print(f"Loaded {len(total_sales_df)} total sales records")
        
        # Commit all changes
        session.commit()
        
        print("✅ Successfully loaded all real datasets!")
        
        # Print summary statistics
        print("\n📊 Dataset Summary:")
        print(f"- Product Eligibility: {len(eligibility_df)} records")
        print(f"- Product Ad Sales: {len(ad_sales_df)} records")
        print(f"- Product Total Sales: {len(total_sales_df)} records")
        
        # Show date ranges
        print(f"\n📅 Date Ranges:")
        print(f"- Ad Sales: {ad_sales_df['date'].min()} to {ad_sales_df['date'].max()}")
        print(f"- Total Sales: {total_sales_df['date'].min()} to {total_sales_df['date'].max()}")
        
        # Show unique items
        unique_items_ad = ad_sales_df['item_id'].nunique()
        unique_items_total = total_sales_df['item_id'].nunique()
        unique_items_eligible = eligibility_df['item_id'].nunique()
        
        print(f"\n🏷️ Unique Items:")
        print(f"- In Ad Sales: {unique_items_ad} items")
        print(f"- In Total Sales: {unique_items_total} items")
        print(f"- In Eligibility: {unique_items_eligible} items")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error loading datasets: {e}")
        raise e
    finally:
        session.close()

def get_dataset_info():
    """Get information about the loaded datasets"""
    session = SessionLocal()
    
    try:
        eligibility_count = session.query(ProductEligibility).count()
        ad_sales_count = session.query(ProductAdSales).count()
        total_sales_count = session.query(ProductTotalSales).count()
        
        return {
            "eligibility_records": eligibility_count,
            "ad_sales_records": ad_sales_count,
            "total_sales_records": total_sales_count
        }
    finally:
        session.close()

if __name__ == "__main__":
    load_real_datasets()
