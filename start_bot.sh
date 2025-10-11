#!/bin/bash
# Meme Coin Scanner Bot Startup Script

echo "🚀 Starting Meme Coin Scanner Bot..."

# Kill any existing bot processes
echo "🔄 Stopping any existing bot instances..."
pkill -f "python3 bot.py" 2>/dev/null || true
pkill -f "bot.py" 2>/dev/null || true
sleep 2

# Navigate to bot directory
cd /Users/divine/Desktop/apeitbot

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Start the bot
echo "🤖 Starting bot..."
python3 bot.py &

# Get the process ID
BOT_PID=$!

echo "✅ Bot started successfully!"
echo "📱 Bot Username: @apeitscannerbot"
echo "🔗 Test with: /scan 51aXwxgrWKRXJGwWVVgE3Jrs2tWKhuNadfsEt6j2pump"
echo "🛑 To stop: kill $BOT_PID"
echo ""
echo "📊 Bot Features:"
echo "• Real-time holder analysis from Helius API"
echo "• Top 10 holders with copyable addresses"
echo "• Dev wallet detection and bundle analysis"
echo "• Custom banner image integration"
echo "• Professional security scoring"
echo ""
echo "Bot is running in the background. Check logs for activity."