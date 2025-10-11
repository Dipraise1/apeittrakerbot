# Meme Coin Scanner Telegram Bot

A comprehensive Telegram bot for scanning and analyzing meme coins on Solana, Ethereum, and Binance Smart Chain (BSC). The bot provides detailed token analysis including market data, security metrics, holder distribution, and risk assessment.

## Features

- 🔍 **Multi-Chain Support**: Solana, Ethereum, and BSC
- 📊 **Comprehensive Analysis**: Market cap, volume, liquidity, holders
- 🔒 **Security Assessment**: Rug pull detection, holder concentration analysis
- 📈 **Real-time Data**: Live price feeds and market data
- 👥 **User Management**: Watchlists, scan history, preferences
- 🎯 **Risk Scoring**: Automated risk assessment with detailed explanations

## Installation

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- RPC endpoints for blockchain access

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd apeitbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
   ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your_alchemy_key
   BSC_RPC_URL=https://bsc-dataseed.binance.org/
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Usage

### Commands

- `/start` - Welcome message and bot introduction
- `/help` - Show available commands and usage
- `/scan <token_address>` - Scan a specific token
- `/watchlist` - Manage your token watchlist
- `/history` - View your scan history
- `/stats` - View bot statistics

### Examples

```
/scan EHiuBorf3mGoja4RLXCy2LNRTf1wCmxXU1U7AB3ipump
/scan 0x1234567890abcdef1234567890abcdef12345678
/scan 0xabcdef1234567890abcdef1234567890abcdef12
```

## Token Analysis Features

### Market Data
- Current price and market cap
- 24h volume and liquidity
- Price changes and trends
- Trading activity metrics

### Security Analysis
- Holder distribution analysis
- Top holder concentration
- Liquidity depth assessment
- Contract verification status
- Rug pull risk indicators

### Risk Assessment
- Automated risk scoring (0-100)
- Color-coded risk levels
- Detailed risk explanations
- Security recommendations

## Supported Blockchains

### Solana (SOL)
- SPL token standard
- Jupiter DEX integration
- Raydium liquidity pools
- Solana program verification

### Ethereum (ETH)
- ERC-20 standard
- Uniswap integration
- OpenZeppelin security
- Gas optimization

### Binance Smart Chain (BSC)
- BEP-20 standard
- PancakeSwap integration
- Lower gas fees
- Binance ecosystem

## API Integrations

The bot integrates with various APIs for comprehensive data:

- **Jupiter API**: Solana price data and liquidity
- **DexScreener**: Multi-chain token data
- **CoinGecko**: Market data and analytics
- **Blockchain RPCs**: Direct blockchain queries

## Database

The bot uses SQLite for data storage:

- **Users**: User profiles and preferences
- **Token Scans**: Scan history and results
- **Watchlists**: User token watchlists
- **Statistics**: Bot usage analytics

## Security Features

- **Holder Analysis**: Distribution and concentration
- **Liquidity Checks**: Depth and stability
- **Contract Verification**: Code audit status
- **Risk Scoring**: Multi-factor risk assessment
- **Rug Pull Detection**: Early warning indicators

## Development

### Project Structure

```
apeitbot/
├── bot.py                 # Main bot application
├── token_scanner.py       # Token analysis logic
├── message_formatter.py   # Message formatting
├── database.py           # Database operations
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

### Adding New Features

1. **New Blockchain Support**: Add RPC client and analysis methods
2. **Enhanced Security**: Implement additional risk factors
3. **UI Improvements**: Modify message formatting
4. **Data Sources**: Integrate new APIs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot is for educational and informational purposes only. Always do your own research before investing in any cryptocurrency. The bot's analysis should not be considered as financial advice.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Roadmap

- [ ] Enhanced security analysis
- [ ] Social sentiment integration
- [ ] Price alerts and notifications
- [ ] Advanced charting features
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Caching improvements
- [ ] Mobile app integration
# apeittrakerbot
