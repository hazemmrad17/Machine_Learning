"""
Script to run the Streamlit Web UI.
"""

import subprocess
import sys
import os

def main():
    """Run Streamlit web UI."""
    web_ui_path = os.path.join(os.path.dirname(__file__), '..', 'web_ui', 'app.py')
    
    # Check if file exists
    if not os.path.exists(web_ui_path):
        print(f"Error: Web UI file not found at {web_ui_path}")
        return
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", web_ui_path,
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])

if __name__ == "__main__":
    main()

