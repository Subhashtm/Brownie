#!/usr/bin/env python3
"""
Brownie Shop Server Startup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import supabase
        from PIL import Image
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    if not env_path.exists():
        print("✗ .env file not found")
        print("Please copy .env.example to .env and fill in your credentials")
        return False
    
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_KEY", 
        "SECRET_KEY"
    ]
    
    with open(env_path) as f:
        env_content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if f"{var}=your_" in env_content or f"{var}=" not in env_content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"✗ Please configure these environment variables in .env:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    
    print("✓ Environment configuration looks good")
    return True

def start_server():
    """Start the FastAPI server"""
    print("Starting Brownie Shop server...")
    print("Server will be available at: http://localhost:8000")
    print("Admin login: admin@brownieshop.com / admin123")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to backend directory and run the server
        os.chdir("backend")
        # Load environment variables from parent directory
        from dotenv import load_dotenv
        load_dotenv("../.env")
        
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    print("Brownie Shop - Server Startup")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()