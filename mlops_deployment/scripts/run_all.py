"""
Script to run both API and Web UI together.
Requires running in separate processes.
"""

import subprocess
import sys
import os
import time
import signal

def main():
    """Run both API and Web UI."""
    print("="*60)
    print("Starting Breast Cancer Detection System")
    print("="*60)
    
    # Check if model exists
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'mlp_model.pkl')
    if not os.path.exists(model_path):
        print("⚠️  Warning: Model not found!")
        print("Please train the model first:")
        print("  python scripts/train.py")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Start API
    print("\n[1/2] Starting API server on port 8000...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    
    # Wait for API to start
    print("Waiting for API to start...")
    time.sleep(3)
    
    # Start Web UI
    print("[2/2] Starting Web UI on port 8501...")
    web_ui_path = os.path.join(os.path.dirname(__file__), '..', 'web_ui', 'app.py')
    web_ui_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", web_ui_path, "--server.port", "8501"],
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    
    print("\n" + "="*60)
    print("✅ System Started Successfully!")
    print("="*60)
    print("\n📍 Access Points:")
    print("  🌐 Web UI:  http://localhost:8501")
    print("  🔌 API:     http://localhost:8000")
    print("  📚 API Docs: http://localhost:8000/docs")
    print("\n⚠️  Press Ctrl+C to stop both services")
    print("="*60)
    
    try:
        # Wait for processes
        api_process.wait()
        web_ui_process.wait()
    except KeyboardInterrupt:
        print("\n\nStopping services...")
        api_process.terminate()
        web_ui_process.terminate()
        print("✅ Services stopped")

if __name__ == "__main__":
    main()

