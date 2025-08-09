#!/usr/bin/env python3
"""
Quick start script for ADGM Corporate Agent
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
        print("⚠️  Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Create directories
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    print("✅ Setup complete")
    print("🚀 Launching ADGM Corporate Agent...")
    print("📖 Open http://localhost:7860 in your browser")
    print("=" * 50)
    
    # Launch the application
    try:
        from app import create_interface
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

if __name__ == "__main__":
    main()