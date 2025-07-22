"""
E-commerce AI Agent
Main application entry point
"""

from pathlib import Path

import uvicorn

import config
from src.api.routes import app
from src.database.setup import initialize_database, load_sample_data


def setup_application():
    """Setup the application - database, sample data, etc."""
    print("Setting up E-commerce AI Agent...")
    
    # Create necessary directories
    config.DATA_DIR.mkdir(exist_ok=True)
    config.RAW_DATA_DIR.mkdir(exist_ok=True)
    config.PROCESSED_DATA_DIR.mkdir(exist_ok=True)
    
    # Initialize database
    print("Initializing database...")
    initialize_database()
    
    # Load sample data if database is empty
    if not config.DATABASE_PATH.exists() or config.DATABASE_PATH.stat().st_size == 0:
        print("Loading sample data...")
        load_sample_data()
    
    print("Application setup completed!")

def main():
    """Main application entry point"""
    print("=" * 50)
    print("E-commerce AI Agent")
    print("=" * 50)
    
    # Setup application
    setup_application()
    
    print(f"\nStarting server on {config.API_HOST}:{config.API_PORT}")
    print(f"API Documentation: http://localhost:{config.API_PORT}/docs")
    print(f"Database: {config.DATABASE_PATH}")
    print("\nSample API Endpoints:")
    print(f"  GET  http://localhost:{config.API_PORT}/health")
    print(f"  GET  http://localhost:{config.API_PORT}/stats")
    print(f"  POST http://localhost:{config.API_PORT}/ask")
    print(f"  GET  http://localhost:{config.API_PORT}/sample-questions")
    
    print("\nExample API Usage:")
    print("curl -X POST http://localhost:8000/ask \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"question\": \"What is my total sales?\", \"include_chart\": true}'")
    
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        reload=False,  # Set to True for development
        log_level="info"
    )

if __name__ == "__main__":
    main()
