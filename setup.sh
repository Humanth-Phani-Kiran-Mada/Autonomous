#!/bin/bash
# Setup script for Self-Evolving AI System

echo "====================================================="
echo "SELF-EVOLVING AI SYSTEM - SETUP"
echo "====================================================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ Created .env file - update with your API keys if needed"
fi

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/memory data/knowledge data/cache logs

echo ""
echo "====================================================="
echo "✅ SETUP COMPLETE"
echo "====================================================="
echo ""
echo "To start the system, run:"
echo "  python main.py"
echo ""
echo "Or activate the virtual environment first:"
echo "  source venv/bin/activate"
echo ""
