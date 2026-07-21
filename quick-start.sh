#!/bin/bash
# MotoERP Quick Start Script
# Automează setup local în 3 comenzi

set -e

echo "🚀 MotoERP - Quick Start"
echo "========================"
echo ""

# 1. Creează .env din template
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your Supabase credentials:"
    echo "   SUPABASE_URL=https://xxxxx.supabase.co"
    echo "   SUPABASE_KEY=eyJhbGc..."
    echo ""
else
    echo "✅ .env already exists"
fi

# 2. Create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# 3. Activate venv and install dependencies
echo "📦 Installing dependencies..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Mac/Linux
    source venv/bin/activate
fi

pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env with Supabase credentials"
echo "2. Run Supabase schema: database/schema.sql"
echo "3. Start app: streamlit run app/app.py"
echo ""
echo "🌐 App will open at: http://localhost:8501"
