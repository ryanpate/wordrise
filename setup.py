#!/usr/bin/env python
"""
Setup script for WordRise Enhanced
Initializes database, word data, and token prices
"""
import os
import sys

def main():
    print("🏗️  WordRise Enhanced - Setup Script")
    print("=" * 50)
    
    # Step 1: Setup word data
    print("\n📚 Step 1: Setting up word database...")
    try:
        import setup_words
        setup_words.setup_word_list()
        print("✅ Word database created successfully!")
    except Exception as e:
        print(f"❌ Failed to setup words: {e}")
        sys.exit(1)
    
    # Step 2: Initialize Flask app and database
    print("\n🗄️  Step 2: Initializing database...")
    try:
        from run import app
        from app.models.models import db, TokenPrice
        
        with app.app_context():
            db.create_all()
            TokenPrice.initialize_prices()
        
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✨ Setup complete! You can now run the app with:")
    print("   python run.py")
    print("\n💡 For Railway deployment, environment variables needed:")
    print("   SECRET_KEY=<your-secret-key>")
    print("   DATABASE_URL=<postgresql-url> (auto-set by Railway)")
    print("=" * 50)

if __name__ == "__main__":
    main()
