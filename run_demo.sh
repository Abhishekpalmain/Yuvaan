#!/bin/bash
# Intelli-Credit Quick Setup & Demo Script
# For Linux/Mac

echo "=================================="
echo "Intelli-Credit Quick Start"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+')
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "⚠️ Some dependencies may have failed. Check requirements.txt"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To run the pipeline:"
echo "  source venv/bin/activate  # Activate virtual environment"
echo "  python main.py            # Run complete pipeline"
echo "  python main.py --help     # See all options"
echo ""
echo "To view the dashboard:"
echo "  Open frontend/dashboard.html in your browser"
echo ""
echo "Documentation:"
echo "  README.md     - Full project documentation"
echo "  aboutus.txt   - Complete project overview"
echo "  docs/         - Detailed architecture docs"
echo ""

# Ask if user wants to run now
read -p "Run the pipeline now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python main.py
fi
