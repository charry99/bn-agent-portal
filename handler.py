import sys
import os
import traceback
from flask import Flask, jsonify

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = None
init_error = None

try:
    from app import application
    app = application
except Exception as e:
    init_error = e
    app = Flask(__name__)
    error_trace = traceback.format_exc()
    
    @app.route('/')
    def error():
        return jsonify({
            'error': 'Failed to initialize application',
            'message': str(init_error),
            'trace': error_trace
        }), 500

