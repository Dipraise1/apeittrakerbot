#!/usr/bin/env python3
"""
Test script to verify the bot setup and dependencies
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    required_modules = [
        'telegram',
        'requests',
        'web3',
        'solana',
        'aiohttp'
    ]
    
    print("🔍 Testing imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies: pip install -r requirements.txt")
        return False
    
    print("\n✅ All imports successful!")
    return True

def test_config():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import TELEGRAM_BOT_TOKEN, SUPPORTED_CHAINS
        print("✅ Config module loaded")
        
        if not TELEGRAM_BOT_TOKEN:
            print("⚠️  TELEGRAM_BOT_TOKEN not set in environment")
        else:
            print("✅ TELEGRAM_BOT_TOKEN found")
        
        print(f"✅ Supported chains: {', '.join(SUPPORTED_CHAINS)}")
        return True
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_database():
    """Test database initialization."""
    print("\n🔍 Testing database...")
    
    try:
        from database import Database
        db = Database(":memory:")  # Use in-memory database for testing
        print("✅ Database module loaded")
        print("✅ Database initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_bot_modules():
    """Test bot module imports."""
    print("\n🔍 Testing bot modules...")
    
    try:
        from token_scanner import TokenScanner
        from message_formatter import MessageFormatter
        print("✅ Token scanner module loaded")
        print("✅ Message formatter module loaded")
        return True
        
    except Exception as e:
        print(f"❌ Bot modules error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Meme Coin Scanner Bot - Setup Test\n")
    
    tests = [
        test_imports,
        test_config,
        test_database,
        test_bot_modules
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot is ready to run.")
        print("\nTo start the bot, run: python run.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
