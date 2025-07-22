import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATABASE_PATH = DATA_DIR / "database.db"

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# LLM Configuration
GEMINI_API_KEY = "AIzaSyDbrh5S78ezWjIrx3Bx5xFNLhFBSthaKx8"
LLM_MODEL = "llama3.2"  # Ollama model
LLM_BASE_URL = "http://localhost:11434"

# Database Configuration
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
