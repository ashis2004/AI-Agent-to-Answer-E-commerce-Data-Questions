import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

import config


class DataLoader:
    """Utility class for loading and processing data"""
    
    def __init__(self):
        self.raw_data_dir = config.RAW_DATA_DIR
        self.processed_data_dir = config.PROCESSED_DATA_DIR
    
    def load_csv_files(self, file_mapping: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        """
        Load CSV files and return as dictionary of DataFrames
        
        Args:
            file_mapping: Dict mapping table names to CSV file paths
            
        Returns:
            Dictionary of DataFrames
        """
        dataframes = {}
        
        for table_name, file_path in file_mapping.items():
            file_path = Path(file_path)
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    dataframes[table_name] = df
                    print(f"Loaded {len(df)} records from {file_path}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
            else:
                print(f"File not found: {file_path}")
        
        return dataframes
    
    def clean_and_process_data(self, dataframes: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Clean and process the loaded data"""
        processed_data = {}
        
        for table_name, df in dataframes.items():
            # Make a copy to avoid modifying original
            processed_df = df.copy()
            
            # Common cleaning operations
            processed_df = self._clean_dataframe(processed_df, table_name)
            
            # Specific processing based on table type
            if table_name == 'product_eligibility':
                processed_df = self._process_eligibility_data(processed_df)
            elif table_name == 'product_ad_sales':
                processed_df = self._process_ad_sales_data(processed_df)
            elif table_name == 'product_total_sales':
                processed_df = self._process_total_sales_data(processed_df)
            
            processed_data[table_name] = processed_df
            print(f"Processed {table_name}: {len(processed_df)} records")
        
        return processed_data
    
    def _clean_dataframe(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Common cleaning operations for all dataframes"""
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Strip whitespace from string columns
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].astype(str).str.strip()
        
        # Replace empty strings with None
        df = df.replace('', None)
        df = df.replace('nan', None)
        df = df.replace('NaN', None)
        
        # Ensure product_id is consistent across tables
        if 'product_id' in df.columns:
            df['product_id'] = df['product_id'].astype(str).str.strip()
        
        return df
    
    def _process_eligibility_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process product eligibility data"""
        # Ensure required columns exist
        required_columns = ['product_id', 'product_name']
        for col in required_columns:
            if col not in df.columns:
                df[col] = ''
        
        # Convert eligibility to boolean (0/1)
        if 'is_eligible_for_ads' in df.columns:
            df['is_eligible_for_ads'] = df['is_eligible_for_ads'].map({
                'Yes': 1, 'yes': 1, 'Y': 1, 'y': 1, 1: 1, '1': 1, True: 1,
                'No': 0, 'no': 0, 'N': 0, 'n': 0, 0: 0, '0': 0, False: 0
            }).fillna(0).astype(int)
        
        # Clean category and brand names
        for col in ['category', 'subcategory', 'brand']:
            if col in df.columns:
                df[col] = df[col].str.title()
        
        return df
    
    def _process_ad_sales_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process ad sales data"""
        # Ensure numeric columns are properly typed
        numeric_columns = [
            'ad_spend', 'impressions', 'clicks', 'ctr', 'cpc', 
            'ad_sales', 'ad_orders', 'conversion_rate', 'acos'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calculate derived metrics if missing
        if 'ctr' not in df.columns and 'clicks' in df.columns and 'impressions' in df.columns:
            df['ctr'] = np.where(df['impressions'] > 0, 
                                (df['clicks'] / df['impressions']) * 100, 0)
        
        if 'cpc' not in df.columns and 'ad_spend' in df.columns and 'clicks' in df.columns:
            df['cpc'] = np.where(df['clicks'] > 0, 
                                df['ad_spend'] / df['clicks'], 0)
        
        if 'conversion_rate' not in df.columns and 'ad_orders' in df.columns and 'clicks' in df.columns:
            df['conversion_rate'] = np.where(df['clicks'] > 0, 
                                           (df['ad_orders'] / df['clicks']) * 100, 0)
        
        if 'acos' not in df.columns and 'ad_spend' in df.columns and 'ad_sales' in df.columns:
            df['acos'] = np.where(df['ad_sales'] > 0, 
                                 (df['ad_spend'] / df['ad_sales']) * 100, 0)
        
        return df
    
    def _process_total_sales_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process total sales data"""
        # Ensure numeric columns are properly typed
        numeric_columns = [
            'total_sales', 'total_orders', 'organic_sales', 'organic_orders',
            'sessions', 'session_percentage', 'page_views', 'page_view_percentage',
            'buy_box_percentage'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calculate organic sales if missing
        if 'organic_sales' not in df.columns:
            # This would need ad_sales data to calculate properly
            df['organic_sales'] = df.get('total_sales', 0)
        
        if 'organic_orders' not in df.columns:
            df['organic_orders'] = df.get('total_orders', 0)
        
        return df
    
    def save_to_database(self, dataframes: Dict[str, pd.DataFrame]):
        """Save processed dataframes to SQLite database"""
        conn = sqlite3.connect(config.DATABASE_PATH)
        
        # Table mapping
        table_mapping = {
            'eligibility': 'product_eligibility',
            'product_eligibility': 'product_eligibility',
            'ad_sales': 'product_ad_sales',
            'product_ad_sales': 'product_ad_sales',
            'total_sales': 'product_total_sales',
            'product_total_sales': 'product_total_sales'
        }
        
        for df_name, df in dataframes.items():
            table_name = table_mapping.get(df_name, df_name)
            
            try:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Saved {len(df)} records to table: {table_name}")
            except Exception as e:
                print(f"Error saving {df_name} to database: {e}")
        
        conn.close()
        print("Data saved to database successfully!")
    
    def validate_data_consistency(self, dataframes: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Validate data consistency across tables"""
        validation_results = {
            'issues': [],
            'summary': {},
            'recommendations': []
        }
        
        # Get product IDs from each table
        product_ids = {}
        for table_name, df in dataframes.items():
            if 'product_id' in df.columns:
                product_ids[table_name] = set(df['product_id'].dropna().unique())
        
        # Check for missing products across tables
        if len(product_ids) > 1:
            all_products = set()
            for products in product_ids.values():
                all_products.update(products)
            
            for table_name, products in product_ids.items():
                missing = all_products - products
                if missing:
                    validation_results['issues'].append(
                        f"Table {table_name} is missing {len(missing)} products: {list(missing)[:5]}{'...' if len(missing) > 5 else ''}"
                    )
        
        # Check for data quality issues
        for table_name, df in dataframes.items():
            # Check for missing values in important columns
            if table_name == 'product_eligibility' and 'product_name' in df.columns:
                missing_names = df['product_name'].isna().sum()
                if missing_names > 0:
                    validation_results['issues'].append(f"{table_name}: {missing_names} products without names")
            
            # Check for negative values where they shouldn't exist
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col in ['sales', 'spend', 'orders', 'impressions', 'clicks']:
                    negative_count = (df[col] < 0).sum()
                    if negative_count > 0:
                        validation_results['issues'].append(f"{table_name}.{col}: {negative_count} negative values")
        
        # Summary statistics
        for table_name, df in dataframes.items():
            validation_results['summary'][table_name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'missing_data_percentage': (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100
            }
        
        return validation_results
    
    def generate_sample_data(self) -> Dict[str, pd.DataFrame]:
        """Generate sample data for testing"""
        np.random.seed(42)  # For reproducible results
        
        # Sample product eligibility data
        products = []
        for i in range(1, 21):  # 20 products
            products.append({
                'product_id': f'PROD{i:03d}',
                'product_name': f'Product {i}',
                'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports']),
                'subcategory': f'Subcategory {np.random.randint(1, 6)}',
                'brand': f'Brand {np.random.choice(["A", "B", "C", "D", "E"])}',
                'is_eligible_for_ads': np.random.choice([0, 1], p=[0.2, 0.8]),
                'eligibility_reason': np.random.choice([
                    'Meets all criteria', 'Approved for advertising', 
                    'Pending review', 'Brand verification required'
                ])
            })
        
        # Sample ad sales data (only for eligible products)
        eligible_products = [p['product_id'] for p in products if p['is_eligible_for_ads'] == 1]
        ad_sales = []
        for product_id in eligible_products:
            ad_spend = np.random.uniform(100, 1000)
            impressions = np.random.randint(5000, 50000)
            clicks = int(impressions * np.random.uniform(0.01, 0.05))
            ad_sales_amount = ad_spend * np.random.uniform(1.5, 4.0)
            
            ad_sales.append({
                'product_id': product_id,
                'campaign_name': f'Campaign for {product_id}',
                'ad_spend': round(ad_spend, 2),
                'impressions': impressions,
                'clicks': clicks,
                'ctr': round((clicks / impressions) * 100, 2),
                'cpc': round(ad_spend / clicks, 2),
                'ad_sales': round(ad_sales_amount, 2),
                'ad_orders': np.random.randint(10, 100),
                'conversion_rate': round(np.random.uniform(3, 8), 2),
                'acos': round((ad_spend / ad_sales_amount) * 100, 2)
            })
        
        # Sample total sales data
        total_sales = []
        for product in products:
            total_sales_amount = np.random.uniform(1000, 10000)
            
            total_sales.append({
                'product_id': product['product_id'],
                'total_sales': round(total_sales_amount, 2),
                'total_orders': np.random.randint(50, 200),
                'organic_sales': round(total_sales_amount * np.random.uniform(0.5, 0.8), 2),
                'organic_orders': np.random.randint(25, 150),
                'sessions': np.random.randint(500, 5000),
                'session_percentage': round(np.random.uniform(5, 25), 2),
                'page_views': np.random.randint(1000, 10000),
                'page_view_percentage': round(np.random.uniform(8, 30), 2),
                'buy_box_percentage': round(np.random.uniform(60, 95), 2)
            })
        
        return {
            'product_eligibility': pd.DataFrame(products),
            'product_ad_sales': pd.DataFrame(ad_sales),
            'product_total_sales': pd.DataFrame(total_sales)
        }
