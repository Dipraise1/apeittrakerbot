#!/usr/bin/env python3
"""
Start script for the Telegram bot
"""
import os
import sys
from bot import main

if __name__ == "__main__":
    # Set up environment
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("ERROR: TELEGRAM_BOT_TOKEN environment variable not set!")
        sys.exit(1)
    
    print("Starting Telegram Bot...")
    main()
