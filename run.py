#!/usr/bin/env python
"""
Entry point for running the Billions Network Agent Portal
Can be used as an alternative to running: flask run
Usage: python run.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import create_app
from config import get_config

if __name__ == '__main__':
    # Get environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Get configuration
    config = get_config(env)
    
    # Create app
    app = create_app(env)
    
    # Display information
    print("=" * 50)
    print("Billions Network Agent Portal")
    print("=" * 50)
    print(f"Environment: {env}")
    print(f"Debug: {app.config['DEBUG']}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Run the app
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Server running at http://{host}:{port}")
    print("=" * 50)
    print("Press CTRL+C to stop\n")
    
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG'],
        use_reloader=app.config['DEBUG']
    )
