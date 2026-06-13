#!/bin/bash
# Quick Design Installer
# Usage: git clone https://github.com/rishapgandhi/quick_design.git && cd quick_design && bash install.sh
set -e

echo "🎨 Installing Quick Design MCP Server..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.10+ required. Install it first."
    exit 1
fi

# Check wkhtmltopdf
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "📦 Installing wkhtmltopdf..."
    sudo apt-get install -y wkhtmltopdf 2>/dev/null || echo "⚠️  Install wkhtmltopdf manually: sudo apt install wkhtmltopdf"
fi

# Install Python deps
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Setup .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Edit .env and add your Gemini API key from https://aistudio.google.com/apikey"
fi

# Clone Open Design repo for skills + design systems (if not already present)
OD_PATH="/var/www/html/test/open-design"
if [ ! -d "$OD_PATH/design-systems" ]; then
    echo "📦 Cloning Open Design repo for skills and design systems..."
    git clone --depth 1 https://github.com/nexu-io/open-design.git "$OD_PATH"
fi

echo ""
echo "✅ Quick Design installed!"
echo ""
echo "Next steps:"
echo "  1. Edit .env → add your GEMINI_API_KEY"
echo "  2. Test: python3 -m src.server"
echo "  3. Add to your AI agent (OpenClaw, Claude Code, Kiro):"
echo ""
echo '     "quick_design": {'
echo '       "command": "python3",'
echo '       "args": ["-m", "src.server"],'
echo "       \"cwd\": \"$(pwd)\""
echo '     }'
