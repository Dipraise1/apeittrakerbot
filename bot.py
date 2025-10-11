#!/usr/bin/env python3
"""
Basic Meme Coin Scanner Bot - Working Version
"""

import logging
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from deep_analyzer import DeepTokenAnalyzer

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MemeCoinBot:
    def __init__(self):
        self.deep_analyzer = DeepTokenAnalyzer()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        welcome_message = """🚀 Meme Coin Scanner Bot 🚀

Welcome! I can scan meme coins on:
• Solana (SOL)
• Ethereum (ETH) 
• Binance Smart Chain (BSC)

Commands:
/scan <token_address> - Scan a specific token
/help - Show this help message

Usage:
Just send me a token contract address and I'll analyze it for you!

Example: /scan EHiuBorf3mGoja4RLXCy2LNRTf1wCmxXU1U7AB3ipump"""
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        help_text = """📋 How to use the bot:

1. Scan a token: /scan <contract_address>
   - Works with Solana, Ethereum, and BSC tokens
   - Example: /scan EHiuBorf3mGoja4RLXCy2LNRTf1wCmxXU1U7AB3ipump

2. Supported chains:
   - Solana (SOL)
   - Ethereum (ETH)
   - Binance Smart Chain (BSC)

3. What I analyze:
   - Market cap and volume
   - Liquidity and holders
   - Security metrics
   - Developer activity
   - Rug pull indicators

Just paste a token contract address and I'll do the rest! 🔍"""
        await update.message.reply_text(help_text)
    
    def detect_chain(self, token_address: str) -> str:
        """Detect which blockchain the token belongs to."""
        # Solana addresses are base58 encoded and typically 32-44 characters
        if len(token_address) >= 32 and len(token_address) <= 44 and not token_address.startswith('0x'):
            return 'solana'
        
        # Ethereum/BSC addresses are 42 characters starting with 0x
        if token_address.startswith('0x') and len(token_address) == 42:
            return 'ethereum'
        
        return 'unknown'
    
    async def scan_token(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle token scanning requests."""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide a token contract address.\n\n"
                "Usage: /scan <contract_address>"
            )
            return
        
        token_address = context.args[0]
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        
        try:
            # Determine chain
            chain = self.detect_chain(token_address)
            if chain == 'unknown':
                await update.message.reply_text(
                    "❌ Could not determine the blockchain for this token address.\n"
                    "Please make sure the address is valid for Solana, Ethereum, or BSC."
                )
                return
            
            # Get comprehensive token analysis
            token_analysis = self.deep_analyzer.analyze_token(token_address, chain)
            
            if not token_analysis:
                await update.message.reply_text(
                    "❌ Could not retrieve real holder data from Helius API.\n"
                    "This token may not have sufficient holder data or the API is unavailable.\n"
                    "Please try a different token or check back later."
                )
                return
            
            # Format and send the message
            formatted_message = self.format_deep_analysis(token_analysis)
            
            # Create inline keyboard with additional actions
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{token_address}")],
                [InlineKeyboardButton("📊 More Details", callback_data=f"details_{token_address}")],
                [InlineKeyboardButton("👥 Show All Holders", callback_data=f"holders_{token_address}")],
                [InlineKeyboardButton("🔗 View on Explorer", callback_data=f"explorer_{token_address}_{chain}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send banner image with short caption, then detailed message
            try:
                with open("/Users/divine/Desktop/apeitbot/apebanner.jpeg", "rb") as photo:
                    # Short caption for the image
                    short_caption = f"🟣 {token_analysis.get('name', 'Unknown')} (${token_analysis.get('symbol', 'UNKNOWN')})\n📍 {token_analysis.get('address', '')[:8]}...{token_analysis.get('address', '')[-8:]}\n💰 MC: ${market_cap_formatted} | 🔴 Risk: {risk_level.upper()}"
                    
                    await update.message.reply_photo(
                        photo=photo,
                        caption=short_caption,
                        reply_markup=reply_markup
                    )
                    
                    # Send detailed analysis as separate message
                    await update.message.reply_text(
                        formatted_message,
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
            except Exception as e:
                logger.error(f"Error sending banner image: {e}")
                # Fallback to text message if image fails
                await update.message.reply_text(
                    formatted_message, 
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            logger.error(f"Error scanning token {token_address}: {e}")
            await update.message.reply_text(
                "❌ An error occurred while scanning the token. Please try again later."
            )
    
    def get_token_data(self, token_address: str, chain: str) -> dict:
        """Get token data from DexScreener API."""
        try:
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                
                if pairs:
                    pair = pairs[0]
                    return {
                        'chain': chain,
                        'address': token_address,
                        'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                        'symbol': pair.get('baseToken', {}).get('symbol', 'UNKNOWN'),
                        'price': float(pair.get('priceUsd', 0)),
                        'market_cap': float(pair.get('marketCap', 0)),
                        'volume_24h': float(pair.get('volume', {}).get('h24', 0)),
                        'liquidity': float(pair.get('liquidity', {}).get('usd', 0)),
                        'price_change_24h': float(pair.get('priceChange', {}).get('h24', 0)),
                        'dex': pair.get('dexId', 'Unknown'),
                        'pair_created_at': pair.get('pairCreatedAt', 0)
                    }
        except Exception as e:
            logger.error(f"Error fetching token data: {e}")
        
        return None
    
    def format_deep_analysis(self, analysis: dict) -> str:
        """Format comprehensive token analysis into a message."""
        if not analysis:
            return "❌ Could not retrieve token data."
        
        # Extract basic data
        chain = analysis.get('chain', 'unknown')
        name = analysis.get('name', 'Unknown Token')
        symbol = analysis.get('symbol', 'UNKNOWN')
        address = analysis.get('address', '')
        market_cap = analysis.get('market_cap', 0)
        price = analysis.get('price', 0)
        volume_24h = analysis.get('volume_24h', 0)
        liquidity = analysis.get('liquidity', 0)
        price_change = analysis.get('price_change_24h', 0)
        dex = analysis.get('dex', 'Unknown')
        
        # Extract deep analysis data
        dex_pricing = analysis.get('dex_pricing', {})
        holder_analysis = analysis.get('holder_analysis', {})
        security_analysis = analysis.get('security_analysis', {})
        
        # Format numbers
        market_cap_formatted = self.format_number(market_cap)
        volume_formatted = self.format_number(volume_24h)
        liquidity_formatted = self.format_number(liquidity)
        
        # Calculate age
        created_at = analysis.get('pair_created_at', 0)
        age_hours = 0
        if created_at:
            import time
            age_hours = int((time.time() - created_at / 1000) / 3600)
        
        # Price change emoji
        change_emoji = "🟢" if price_change >= 0 else "🔴"
        
        # Chain emoji
        chain_emoji = {'solana': '🟣', 'ethereum': '🔷', 'bsc': '🟡'}.get(chain, '🔗')
        
        # DexScreener promotion status
        is_promoted = dex_pricing.get('is_promoted', False)
        boost_count = dex_pricing.get('boost_count', 0)
        promotion_emoji = "💰" if is_promoted else "🆓"
        promotion_text = f"PAID PROMOTION ({boost_count} boosts)" if is_promoted else "Free listing"
        
        # Social media links
        social_links = dex_pricing.get('social_links', [])
        websites = dex_pricing.get('websites', [])
        
        # Holder analysis
        total_holders = holder_analysis.get('total_holders', 0)
        top_10_pct = holder_analysis.get('top_10_percentage', 0)
        dev_pct = holder_analysis.get('dev_wallet_percentage', 0)
        bundle_detected = holder_analysis.get('bundle_detected', False)
        bundle_pct = holder_analysis.get('bundle_percentage', 0)
        top_10_holders = holder_analysis.get('top_10_holders', [])
        
        # Security analysis
        security_score = security_analysis.get('security_score', 50)
        risk_level = security_analysis.get('risk_level', 'medium')
        warnings = security_analysis.get('warnings', [])
        
        # Risk emoji based on score
        risk_emoji = {
            'low': '🟢',
            'medium': '🟡', 
            'high': '🟠',
            'critical': '🔴'
        }.get(risk_level, '🟡')
        
        # Bundle warning
        bundle_warning = ""
        if bundle_detected:
            bundle_warning = f"\n⚠️ BUNDLE DETECTED: {bundle_pct:.1f}%"
        
        # Dev wallet warning
        dev_warning = ""
        if dev_pct > 20:
            dev_warning = f"\n⚠️ DEV HOLDS: {dev_pct:.1f}%"
        
        # Security warnings
        security_warnings = ""
        if warnings:
            security_warnings = f"\n⚠️ {', '.join(warnings)}"
        
        # Format top 5 holders with copyable addresses (collapsible)
        top_holders_text = ""
        if top_10_holders:
            top_holders_text = "\n\n🏆 Top 5 Holders:"
            for i, holder in enumerate(top_10_holders[:5], 1):  # Show only top 5 initially
                address = holder.get('address', '')
                percentage = holder.get('percentage', 0)
                balance = holder.get('balance', 0)
                # Make address copyable by using monospace formatting
                top_holders_text += f"\n{i}. `{address}`: {percentage:.2f}% ({balance:,.0f} tokens)"
            
            # Add "show more" indicator if there are more than 5 holders
            if len(top_10_holders) > 5:
                top_holders_text += f"\n... and {len(top_10_holders) - 5} more holders"
        
        # Format social media links
        social_text = ""
        if social_links or websites:
            social_text = "\n\n🌐 **SOCIAL MEDIA & LINKS**"
            
            if websites:
                social_text += "\n **Websites:**"
                for website in websites:
                    social_text += f"\n•  [{website['label']}]({website['url']})"
            
            if social_links:
                social_text += "\n📱 **Social Media:**"
                for social in social_links:
                    platform_icon = {
                        'twitter': '𝕏',  # X (formerly Twitter)
                        'telegram': '✈️',
                        'discord': '💬',
                        'tiktok': '🎵',
                        'youtube': '📺',
                        'website': '🌐'
                    }.get(social['type'], '🔗')
                    social_text += f"\n• {platform_icon} [{social['type'].title()}]({social['url']})"
        
        message = f"""🔍 **DEEP ANALYSIS REPORT** 🔍

{chain_emoji} **{name} (${symbol})** {promotion_emoji}
📍 `{address[:8]}...{address[-8:] if len(address) > 16 else address}`
⛓️ {chain.upper()} | 🕐 {age_hours}h | {promotion_text}

📊 **MARKET DATA**
💰 MC: ${market_cap_formatted}
💵 Price: ${price:.8f} {change_emoji} {price_change:+.2f}%
📈 Vol: ${volume_formatted} [24h]
💧 Liq: ${liquidity_formatted}

👥 **HOLDER ANALYSIS**
👤 Total: {total_holders:,}
🔝 Top 10: {top_10_pct:.1f}%
👨‍💻 Dev: {dev_pct:.1f}%{dev_warning}{bundle_warning}{top_holders_text}

🔒 **SECURITY ASSESSMENT**
🛡️ Score: {security_score}/100 {risk_emoji}
⚠️ Risk: **{risk_level.upper()}**{security_warnings}

🏪 **DEX**: {dex}{social_text}"""
        
        return message.strip()
    
    def format_all_holders(self, analysis: dict) -> str:
        """Format all top 10 holders for detailed view with copyable addresses."""
        if not analysis:
            return "❌ Could not retrieve holder data."
        
        holder_analysis = analysis.get('holder_analysis', {})
        top_10_holders = holder_analysis.get('top_10_holders', [])
        
        if not top_10_holders:
            return "❌ No holder data available."
        
        holders_text = "🏆 **ALL TOP 10 HOLDERS:**\n\n"
        for i, holder in enumerate(top_10_holders, 1):
            address = holder.get('address', '')
            percentage = holder.get('percentage', 0)
            balance = holder.get('balance', 0)
            # Make addresses copyable with monospace formatting
            holders_text += f"{i}. `{address}`\n   📊 {percentage:.2f}% ({balance:,.0f} tokens)\n\n"
        
        # Add back button
        holders_text += "\n🔙 **Click any button below to go back**"
        
        return holders_text.strip()
    
    def format_token_analysis(self, token_data: dict) -> str:
        """Format token analysis into a message (legacy method)."""
        return self.format_deep_analysis(token_data)
    
    def format_number(self, num: float) -> str:
        """Format large numbers with K, M, B suffixes."""
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return f"{num:.2f}"
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("refresh_"):
            token_address = data.replace("refresh_", "")
            # Re-scan the token
            try:
                chain = self.detect_chain(token_address)
                if chain == 'unknown':
                    await query.edit_message_text(
                        "❌ Could not determine the blockchain for this token address."
                    )
                    return
                
                # Get comprehensive token analysis
                token_analysis = self.deep_analyzer.analyze_token(token_address, chain)
                
                if not token_analysis:
                    await query.edit_message_text(
                        "❌ Could not retrieve real holder data from Helius API.\n"
                        "This token may not have sufficient holder data or the API is unavailable.\n"
                        "Please try a different token or check back later."
                    )
                    return
                
                # Format and send the message
                formatted_message = self.format_deep_analysis(token_analysis)
                
                # Create inline keyboard with additional actions
                keyboard = [
                    [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{token_address}")],
                    [InlineKeyboardButton("📊 More Details", callback_data=f"details_{token_address}")],
                    [InlineKeyboardButton("👥 Show All Holders", callback_data=f"holders_{token_address}")],
                    [InlineKeyboardButton("🔗 View on Explorer", callback_data=f"explorer_{token_address}_{chain}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                # Try to edit with photo, fallback to text if needed
                try:
                    with open("/Users/divine/Desktop/apeitbot/apebanner.jpeg", "rb") as photo:
                        await query.edit_message_media(
                            media=InputMediaPhoto(media=photo, caption=formatted_message),
                            reply_markup=reply_markup
                        )
                except Exception as e:
                    logger.error(f"Error updating with banner image: {e}")
                    # Fallback to text message
                    await query.edit_message_text(
                        formatted_message, 
                        reply_markup=reply_markup
                    )
                
            except Exception as e:
                logger.error(f"Error refreshing token {token_address}: {e}")
                await query.edit_message_text(
                    "❌ An error occurred while refreshing the token. Please try again later."
                )
        
        elif data.startswith("details_"):
            token_address = data.replace("details_", "")
            # Show more detailed analysis
            detailed_message = """📈 Deep Analysis Report

🔍 Advanced Metrics:
• Liquidity depth analysis
• Holder distribution patterns  
• Trading volume trends
• Bundle detection algorithms
• Dev wallet tracking

⚠️ Security Analysis:
• Contract verification status
• Honeypot detection
• Rug pull indicators
• Holder concentration risk
• Bundle manipulation detection

📊 Market Intelligence:
• DexScreener promotion status
• Top holder percentages
• Dev sell detection
• Bundle percentage analysis
• Risk scoring algorithm

🔒 Security Score Breakdown:
• Contract verification: +20 points
• Holder distribution: +30 points  
• Liquidity analysis: +25 points
• Bundle detection: +15 points
• Dev wallet analysis: +10 points"""
            await query.edit_message_text(detailed_message)
        
        elif data.startswith("holders_"):
            # Show all holders
            token_address = data.replace("holders_", "")
            await query.answer("👥 Loading all holders...")
            
            # Get fresh analysis
            chain = self.detect_chain(token_address)
            token_analysis = self.deep_analyzer.analyze_token(token_address, chain)
            
            if token_analysis:
                holders_message = self.format_all_holders(token_analysis)
                
                # Create navigation keyboard
                keyboard = [
                    [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{token_address}")],
                    [InlineKeyboardButton("📊 Back to Analysis", callback_data=f"details_{token_address}")],
                    [InlineKeyboardButton("🔗 View on Explorer", callback_data=f"explorer_{token_address}_{chain}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    f"👥 **HOLDER BREAKDOWN** 👥\n\n{holders_message}",
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            else:
                await query.edit_message_text("❌ Could not retrieve holder data.")
        
        elif data.startswith("explorer_"):
            parts = data.replace("explorer_", "").split("_")
            token_address = parts[0]
            chain = parts[1]
            # Open blockchain explorer
            explorer_url = self.get_explorer_url(token_address, chain)
            await query.edit_message_text(f"🔗 Blockchain Explorer:\n{explorer_url}")
    
    def get_explorer_url(self, token_address: str, chain: str) -> str:
        """Get blockchain explorer URL for the token."""
        if chain == 'solana':
            return f"https://solscan.io/token/{token_address}"
        elif chain == 'ethereum':
            return f"https://etherscan.io/token/{token_address}"
        elif chain == 'bsc':
            return f"https://bscscan.com/token/{token_address}"
        return ""

def main():
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Create bot instance
    bot = MemeCoinBot()
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("scan", bot.scan_token))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.scan_token))
    application.add_handler(CallbackQueryHandler(bot.handle_callback))
    
    # Start the bot
    logger.info("Starting Meme Coin Scanner Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
