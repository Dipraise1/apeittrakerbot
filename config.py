import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Blockchain RPC URLs
SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL', 'https://api.mainnet-beta.solana.com')
ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL', 'https://eth-mainnet.g.alchemy.com/v2/your_key')
BSC_RPC_URL = os.getenv('BSC_RPC_URL', 'https://bsc-dataseed.binance.org/')

# Optional API Keys
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
DEXSCREENER_API_KEY = os.getenv('DEXSCREENER_API_KEY')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_data.db')

# Supported chains
SUPPORTED_CHAINS = ['solana', 'ethereum', 'bsc']
