"""
Script to run the React Web UI.
"""

import subprocess
import sys
import os
import shutil

def main():
    """Run React web UI."""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    
    # Check if frontend directory exists
    if not os.path.exists(frontend_path):
        print(f"Error: Frontend directory not found at {frontend_path}")
        print("Please make sure the React frontend is set up.")
        return
    
    # Check if npm is available
    npm_cmd = 'npm.cmd' if os.name == 'nt' else 'npm'
    npm_path = shutil.which(npm_cmd)
    
    if not npm_path:
        print("⚠️  Error: npm (Node.js) is not installed or not in PATH!")
        print("\nPlease install Node.js from: https://nodejs.org/")
        print("After installation:")
        print("  1. Restart your terminal")
        print("  2. Navigate to the frontend directory:")
        print(f"     cd {frontend_path}")
        print("  3. Run: npm install")
        print("  4. Run: npm run dev")
        return
    
    # Check if node_modules exists, install if not
    node_modules_path = os.path.join(frontend_path, 'node_modules')
    if not os.path.exists(node_modules_path):
        print("Installing dependencies...")
        try:
            subprocess.run([npm_cmd, 'install'], cwd=frontend_path, check=True, shell=(os.name == 'nt'))
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error installing dependencies: {e}")
            print("Please run 'npm install' manually in the frontend directory.")
            return
        except Exception as e:
            print(f"⚠️  Error: {e}")
            return
    
    # Run React dev server
    print("Starting React development server on http://localhost:3000")
    try:
        subprocess.run([npm_cmd, 'run', 'dev'], cwd=frontend_path, shell=(os.name == 'nt'))
    except KeyboardInterrupt:
        print("\n\nStopping React dev server...")
    except Exception as e:
        print(f"⚠️  Error starting React dev server: {e}")

if __name__ == "__main__":
    main()

