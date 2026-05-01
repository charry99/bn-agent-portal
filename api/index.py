import sys
import os
import traceback
from flask import Flask, jsonify

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import and use the main app
    from app import application
    app = application
except Exception as e:
    # Create fallback app with error details
    app = Flask(__name__)
    error_trace = traceback.format_exc()
    
    @app.route('/')
    def error():
        return jsonify({
            'error': 'Failed to initialize application',
            'message': str(e),
            'trace': error_trace
        }), 500
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404
