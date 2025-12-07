"""
Script to run the API server.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import uvicorn
import yaml

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

if __name__ == "__main__":
    api_config = config.get('api', {})
    uvicorn.run(
        "api.app:app",
        host=api_config.get('host', '0.0.0.0'),
        port=api_config.get('port', 8000),
        reload=api_config.get('debug', False)
    )

