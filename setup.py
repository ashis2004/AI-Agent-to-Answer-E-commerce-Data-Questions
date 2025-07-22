"""
Setup script for E-commerce AI Agent
Run this script to set up the complete environment
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} is not compatible. Python 3.8+ required.")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling Python dependencies...")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print("✓ pip is available")
    except subprocess.CalledProcessError:
        print("✗ pip is not available. Please install pip first.")
        return False
    
    # Install requirements
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing requirements"
    )
    
    return success

def setup_ollama():
    """Setup Ollama for local LLM"""
    print("\n" + "="*50)
    print("OLLAMA SETUP (Optional but Recommended)")
    print("="*50)
    
    print("""
Ollama provides local LLM capabilities for better performance.
You can either:
1. Install Ollama and download a model (recommended)
2. Skip this step and use the fallback LLM (basic functionality)

To install Ollama:
1. Visit: https://ollama.ai/download
2. Download and install Ollama for Windows
3. Open a new command prompt and run: ollama pull llama3.2
4. Start Ollama service

The application will work without Ollama but with limited AI capabilities.
""")
    
    choice = input("Do you want to check/install Ollama now? (y/n): ").lower()
    
    if choice == 'y':
        print("\nChecking Ollama installation...")
        
        # Check if ollama command is available
        try:
            result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✓ Ollama is installed")
                
                # Check if llama3.2 model is available
                result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
                if "llama3.2" in result.stdout:
                    print("✓ Llama 3.2 model is available")
                    return True
                else:
                    print("⚠ Llama 3.2 model not found")
                    choice = input("Download Llama 3.2 model? (y/n): ").lower()
                    if choice == 'y':
                        return run_command("ollama pull llama3.2", "Downloading Llama 3.2 model")
            else:
                print("✗ Ollama command not found")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("✗ Ollama is not installed or not in PATH")
        
        print("\nTo install Ollama manually:")
        print("1. Visit: https://ollama.ai/download")
        print("2. Download and install Ollama for Windows")
        print("3. Open command prompt and run: ollama pull llama3.2")
        print("4. Restart this setup script")
    
    return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "data/raw",
        "data/processed",
        "static",
        "static/charts",
        "logs"
    ]
    
    print("\nCreating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")
    
    return True

def setup_database():
    """Initialize the database"""
    print("\nSetting up database...")
    try:
        from src.database.setup import initialize_database, load_sample_data
        
        initialize_database()
        print("✓ Database tables created")
        
        load_sample_data()
        print("✓ Sample data loaded")
        
        return True
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return False

def create_run_scripts():
    """Create convenient run scripts"""
    print("\nCreating run scripts...")
    
    # Windows batch file
    batch_content = """@echo off
echo Starting E-commerce AI Agent...
python main.py
pause
"""
    
    with open("run_server.bat", "w") as f:
        f.write(batch_content)
    print("✓ Created: run_server.bat")
    
    # PowerShell script
    ps_content = """# E-commerce AI Agent Startup Script
Write-Host "Starting E-commerce AI Agent..." -ForegroundColor Green
python main.py
Read-Host "Press Enter to exit"
"""
    
    with open("run_server.ps1", "w") as f:
        f.write(ps_content)
    print("✓ Created: run_server.ps1")
    
    return True

def main():
    """Main setup function"""
    print("="*60)
    print("E-COMMERCE AI AGENT - SETUP SCRIPT")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        print("\nPlease upgrade to Python 3.8 or higher and run this script again.")
        return False
    
    # Create directories
    if not create_directories():
        print("\nSetup failed at directory creation.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed at dependency installation.")
        return False
    
    # Setup Ollama (optional)
    ollama_available = setup_ollama()
    
    # Setup database
    if not setup_database():
        print("\nSetup failed at database initialization.")
        return False
    
    # Create run scripts
    if not create_run_scripts():
        print("\nWarning: Failed to create run scripts, but setup can continue.")
    
    # Final instructions
    print("\n" + "="*60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\nTo start the application:")
    print("1. Run: python main.py")
    print("   OR")
    print("2. Double-click: run_server.bat")
    print("   OR")
    print("3. Right-click run_server.ps1 -> Run with PowerShell")
    
    print(f"\nOnce started, the API will be available at:")
    print("- Main API: http://localhost:8000")
    print("- Documentation: http://localhost:8000/docs")
    print("- Health Check: http://localhost:8000/health")
    
    print(f"\nTest the API:")
    print("- Run: python test_api.py")
    
    if not ollama_available:
        print(f"\nNote: Ollama is not set up. The application will use fallback LLM.")
        print("For better AI capabilities, install Ollama and Llama 3.2 model.")
    
    print(f"\nFor custom data:")
    print("1. Place CSV files in data/raw/ directory")
    print("2. Run: python load_data.py")
    
    print("\nHappy coding! 🚀")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        # Ask if user wants to start the server now
        choice = input("\nStart the server now? (y/n): ").lower()
        if choice == 'y':
            print("\nStarting server...")
            try:
                subprocess.run([sys.executable, "main.py"])
            except KeyboardInterrupt:
                print("\nServer stopped.")
    else:
        print("\nSetup failed. Please check the errors above and try again.")
        sys.exit(1)
