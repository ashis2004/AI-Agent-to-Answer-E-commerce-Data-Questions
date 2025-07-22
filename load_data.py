"""
Data setup script
Use this to load your own CSV data into the system
"""

import sys
from pathlib import Path

from src.database.setup import initialize_database
from src.utils.data_loader import DataLoader


def load_custom_data():
    """Load custom CSV data from the raw data directory"""
    
    # Initialize database
    initialize_database()
    
    # Initialize data loader
    loader = DataLoader()
    
    # Define CSV file mapping - update these paths to match your actual files
    csv_files = {
        'product_eligibility': 'data/raw/product_eligibility.csv',
        'product_ad_sales': 'data/raw/product_ad_sales.csv',
        'product_total_sales': 'data/raw/product_total_sales.csv'
    }
    
    print("Looking for CSV files in data/raw/ directory...")
    
    # Check which files exist
    existing_files = {}
    for table_name, file_path in csv_files.items():
        if Path(file_path).exists():
            existing_files[table_name] = file_path
            print(f"✓ Found: {file_path}")
        else:
            print(f"✗ Missing: {file_path}")
    
    if not existing_files:
        print("\nNo CSV files found. Please place your CSV files in the data/raw/ directory with these names:")
        for table_name, file_path in csv_files.items():
            print(f"  - {file_path}")
        print("\nAlternatively, run the main application to use sample data.")
        return
    
    # Load and process data
    print(f"\nLoading {len(existing_files)} CSV files...")
    dataframes = loader.load_csv_files(existing_files)
    
    if dataframes:
        print("Processing data...")
        processed_data = loader.clean_and_process_data(dataframes)
        
        print("Validating data consistency...")
        validation = loader.validate_data_consistency(processed_data)
        
        if validation['issues']:
            print("\nData validation issues found:")
            for issue in validation['issues']:
                print(f"  - {issue}")
            
            response = input("\nContinue with loading? (y/n): ")
            if response.lower() != 'y':
                print("Data loading cancelled.")
                return
        
        print("Saving to database...")
        loader.save_to_database(processed_data)
        
        print("\nData loading completed successfully!")
        print("Summary:")
        for table_name, stats in validation['summary'].items():
            print(f"  {table_name}: {stats['rows']} rows, {stats['columns']} columns")
    
    else:
        print("No data was loaded.")

def generate_sample_data():
    """Generate sample data for testing"""
    
    # Initialize database
    initialize_database()
    
    # Initialize data loader
    loader = DataLoader()
    
    print("Generating sample data...")
    sample_data = loader.generate_sample_data()
    
    print("Saving sample data to database...")
    loader.save_to_database(sample_data)
    
    print("Sample data generated successfully!")
    print("Summary:")
    for table_name, df in sample_data.items():
        print(f"  {table_name}: {len(df)} rows")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        generate_sample_data()
    else:
        load_custom_data()
