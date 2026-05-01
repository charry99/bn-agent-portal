#!/bin/bash
# Startup script for Billions Network Agent Portal

set -e

echo "======================================"
echo "Billions Network Agent Portal"
echo "Starting Application..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo "Installing/Updating dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs uploads instance

# Load environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables from .env"
    export $(cat .env | grep -v '#' | xargs)
else
    echo "WARNING: .env file not found. Create one from .env.example"
    echo "cp .env.example .env"
    exit 1
fi

# Initialize database if needed
if [ ! -f "instance/agent_portal.db" ]; then
    echo "Initializing database..."
    flask db upgrade || flask init-db
    echo "Database initialized!"
fi

# Display startup information
echo ""
echo "======================================"
echo "Configuration:"
echo "  Environment: $FLASK_ENV"
echo "  Debug Mode: $DEBUG"
echo "  Host: $HOST:$PORT"
echo "======================================"
echo ""

# Start the application
if [ "$FLASK_ENV" = "production" ]; then
    echo "Starting production server with Gunicorn..."
    gunicorn --bind $HOST:$PORT --workers 4 --timeout 120 "app:create_app()"
else
    echo "Starting development server..."
    echo "Application available at http://localhost:$PORT"
    echo "Press CTRL+C to stop"
    echo ""
    flask run --host=$HOST --port=$PORT
fi
