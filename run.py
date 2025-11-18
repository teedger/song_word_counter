#!/usr/bin/env python3
"""
Simple script to run the Artist Lyrics Analyzer
"""
import os
import sys
import subprocess


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("📝 Creating .env file from template...")

        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created!")
            print("\n🔑 Please edit .env and add your Genius API token:")
            print("   GENIUS_API_TOKEN=your_token_here")
            print("\n   Get your free token at: https://genius.com/api-clients")
            print("\nThen run this script again.")
            sys.exit(0)
        else:
            print("❌ .env.example not found. Please create a .env file manually.")
            sys.exit(1)


def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import plotly
        import nltk
        import lyricsgenius
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\n📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed!")


def run_app():
    """Run the Streamlit app"""
    print("🎵 Starting Artist Lyrics Analyzer...")
    print("🌐 Opening app in your browser...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])


if __name__ == "__main__":
    check_env_file()
    check_dependencies()
    run_app()
