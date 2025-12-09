"""
Script to run both API and Web UI together.
Requires running in separate processes.
"""

import subprocess
import sys
import os
import time
import signal
import shutil

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
        [sys.executable, "-m", "uvicorn", "api.app:app", "--host", "localhost", "--port", "8000"],
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    
    # Wait for API to start
    print("Waiting for API to start...")
    time.sleep(3)
    
    # Start Web UI (React)
    print("[2/2] Starting React Web UI on port 3000...")
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    
    # Check if frontend exists
    if not os.path.exists(frontend_path):
        print("⚠️  Warning: Frontend directory not found!")
        print("Please make sure the React frontend is set up.")
        web_ui_process = None
    else:
        # Check if npm is available
        npm_cmd = 'npm.cmd' if os.name == 'nt' else 'npm'
        npm_path = shutil.which(npm_cmd)
        
        if not npm_path:
            print("⚠️  Error: npm (Node.js) is not installed or not in PATH!")
            print("\nPlease install Node.js from: https://nodejs.org/")
            print("After installation, restart your terminal and try again.")
            print("\nYou can still use the API at http://localhost:8000")
            web_ui_process = None
        else:
            # Check if node_modules exists and if key packages are installed
            node_modules_path = os.path.join(frontend_path, 'node_modules')
            package_json_path = os.path.join(frontend_path, 'package.json')
            tailwind_path = os.path.join(node_modules_path, 'tailwindcss')
            
            # Check if dependencies need to be installed
            needs_install = False
            if not os.path.exists(node_modules_path):
                needs_install = True
                print("⚠️  node_modules not found. Dependencies need to be installed.")
            elif not os.path.exists(tailwind_path):
                needs_install = True
                print("⚠️  Tailwind CSS not found. Dependencies may be incomplete.")
            
            if needs_install:
                print("=" * 60)
                print("⚠️  DEPENDENCIES NOT INSTALLED")
                print("=" * 60)
                print("\nThe frontend requires npm dependencies to be installed first.")
                print("\nPlease run the following command:")
                print(f"  cd {frontend_path}")
                print("  npm install")
                print("\nThis will install TypeScript, Tailwind CSS, and other dependencies.")
                print("After installation completes, run this script again.")
                print("=" * 60)
                web_ui_process = None
                # Don't return - let API start even if frontend can't
            
            # Start React dev server if we got this far
            if not needs_install or os.path.exists(tailwind_path):
                try:
                    print("Starting React development server...")
                    web_ui_process = subprocess.Popen(
                        [npm_cmd, 'run', 'dev'],
                        cwd=frontend_path,
                        shell=(os.name == 'nt')
                    )
                except Exception as e:
                    print(f"⚠️  Error starting React dev server: {e}")
                    web_ui_process = None
            else:
                print("⚠️  Cannot start React dev server. Please install dependencies first.")
                web_ui_process = None
    
    print("\n" + "="*60)
    print("✅ System Started Successfully!")
    print("="*60)
    print("\n📍 Access Points:")
    if web_ui_process:
        print("  🌐 Web UI:  http://localhost:3000")
    print("  🔌 API:     http://localhost:8000")
    print("  📚 API Docs: http://localhost:8000/docs")
    print("\n⚠️  Press Ctrl+C to stop both services")
    print("="*60)
    
    try:
        # Wait for processes
        api_process.wait()
        if web_ui_process:
            web_ui_process.wait()
    except KeyboardInterrupt:
        print("\n\nStopping services...")
        api_process.terminate()
        if web_ui_process:
            web_ui_process.terminate()
        print("✅ Services stopped")

if __name__ == "__main__":
    main()

