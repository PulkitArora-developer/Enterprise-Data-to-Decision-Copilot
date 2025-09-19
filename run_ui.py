#!/usr/bin/env python3
"""
Launch script for Streamlit UI
"""
import subprocess
import sys
import os

def main():
    print("🚀 Launching BedrockAgentCore Streamlit UI...")
    print("=" * 50)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down UI...")
    except Exception as e:
        print(f"❌ Error launching UI: {e}")

if __name__ == "__main__":
    main()