#!/usr/bin/env python3
"""
Quick start script for ADGM Corporate Agent - Simplified Version
"""

import os
import sys
import subprocess

def main():
    """Main runner function"""
    print("🏛️  ADGM Corporate Agent - Starting...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        return
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check if requirements are installed
    try:
        import gradio
        print("✅ Dependencies found")
    except ImportError:
        print("⚠️  Installing simplified dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_simple.txt"])
            print("✅ Dependencies installed successfully")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            print("💡 Try manually: pip install gradio python-docx python-dotenv pandas requests")
            return
    
    # Create directories
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("src", exist_ok=True)
    
    print("✅ Setup complete")
    print("🚀 Launching ADGM Corporate Agent...")
    print("📖 Open http://localhost:7860 in your browser")
    print("=" * 50)
    
    # Launch the application
    try:
        from app_simple import create_interface
        interface = create_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            debug=False,
            share=False
        )
    except KeyboardInterrupt:
        print("\n👋 ADGM Corporate Agent stopped")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Make sure all files are in the correct location")

if __name__ == "__main__":
    main()