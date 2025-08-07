#!/usr/bin/env python3
"""
Setup script for Pagos - Expense Management System
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        print("📝 Please create a .env file with the following variables:")
        print("   SUPABASE_URL=your_supabase_url")
        print("   SUPABASE_ANON_KEY=your_supabase_anon_key")
        print("📋 You can copy from env.example as a starting point")
        return False
    else:
        print("✅ .env file found")
        return True

def check_supabase_config():
    """Check if Supabase configuration is set"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase configuration missing")
        print("📝 Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file")
        return False
    
    print("✅ Supabase configuration found")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Pagos - Expense Management System")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check environment configuration
    env_ok = check_env_file()
    if env_ok:
        supabase_ok = check_supabase_config()
        if supabase_ok:
            print("\n🎉 Setup completed successfully!")
            print("🚀 Run 'streamlit run app.py' to start the application")
        else:
            print("\n❌ Setup incomplete - please configure Supabase")
    else:
        print("\n❌ Setup incomplete - please create .env file")

if __name__ == "__main__":
    main() 