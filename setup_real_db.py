import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from load_real_data import load_real_datasets
from src.database.models import create_tables


def initialize_database():
    """Initialize database with real e-commerce data"""
    print("🔄 Initializing database with real e-commerce datasets...")
    
    # Create tables
    create_tables()
    print("✅ Database tables created")
    
    # Load real data from CSV files
    load_real_datasets()
    
    print("🎉 Database initialization complete with real data!")

if __name__ == "__main__":
    initialize_database()
