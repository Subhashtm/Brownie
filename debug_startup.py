#!/usr/bin/env python3
"""
Debug startup script to help identify deployment issues
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY', 
        'SECRET_KEY',
        'ADMIN_EMAIL',
        'ADMIN_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'vercel.json',
        'frontend/index.html',
        'frontend/script.js',
        'frontend/styles.css'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
        return True

def check_imports():
    """Check if all required packages can be imported"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'supabase',
        'pydantic',
        'jose',
        'bcrypt',
        'PIL'
    ]
    
    failed_imports = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            failed_imports.append(f"{package}: {e}")
            print(f"❌ Failed to import {package}: {e}")
    
    return len(failed_imports) == 0

def main():
    print("🔍 Running deployment diagnostics...\n")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    env_ok = check_environment()
    print()
    
    files_ok = check_files()
    print()
    
    imports_ok = check_imports()
    print()
    
    if env_ok and files_ok and imports_ok:
        print("🎉 All checks passed! The app should deploy successfully.")
        
        # Try to import the main app
        try:
            from app import app
            print("✅ Main app imported successfully")
        except Exception as e:
            print(f"❌ Failed to import main app: {e}")
            return False
            
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)