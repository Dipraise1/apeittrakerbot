#!/usr/bin/env python3
"""
Deep Token Analysis Module
Provides comprehensive analysis including DexScreener pricing, holder analysis, and security metrics
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class DeepTokenAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_token(self, token_address: str, chain: str) -> Dict:
        """Perform comprehensive token analysis."""
        try:
            # Get basic token data
            basic_data = self.get_basic_token_data(token_address, chain)
            if not basic_data:
                return None
            
            # Get DexScreener pricing info
            dex_pricing = self.get_dex_pricing_info(token_address, chain)
            
            # Get holder analysis
            holder_analysis = self.get_holder_analysis(token_address, chain)
            
            # If no real holder data available, return None
            if not holder_analysis:
                logger.warning(f"No real holder data available for {token_address}")
                return None
            
            # Get security analysis
            security_analysis = self.get_security_analysis(token_address, chain)
            
            # Combine all data
            analysis = {
                **basic_data,
                'dex_pricing': dex_pricing,
                'holder_analysis': holder_analysis,
                'security_analysis': security_analysis,
                'analysis_timestamp': int(time.time())
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in deep analysis: {e}")
            return None
    
    def get_basic_token_data(self, token_address: str, chain: str) -> Dict:
        """Get basic token data from DexScreener."""
        try:
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
            response = self.session.get(url, timeout=10)
            
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
                        'pair_created_at': pair.get('pairCreatedAt', 0),
                        'fdv': float(pair.get('fdv', 0)),
                        'price_change_1h': float(pair.get('priceChange', {}).get('h1', 0)),
                        'price_change_6h': float(pair.get('priceChange', {}).get('h6', 0))
                    }
        except Exception as e:
            logger.error(f"Error fetching basic token data: {e}")
        
        return None
    
    def get_dex_pricing_info(self, token_address: str, chain: str) -> Dict:
        """Get DexScreener pricing and promotion information."""
        try:
            # Check if token is promoted/paid on DexScreener
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                
                if pairs:
                    pair = pairs[0]
                    
                    # Check for paid promotion indicators
                    boosts = pair.get('boosts', {})
                    is_promoted = boosts.get('active', 0) > 0
                    
                    # Extract social media links
                    social_links = []
                    websites = []
                    
                    if 'info' in pair:
                        info = pair['info']
                        
                        # Get social media links
                        if 'socials' in info:
                            for social in info['socials']:
                                social_links.append({
                                    'type': social.get('type', 'unknown'),
                                    'url': social.get('url', '')
                                })
                        
                        # Get website links
                        if 'websites' in info:
                            for website in info['websites']:
                                websites.append({
                                    'label': website.get('label', 'Website'),
                                    'url': website.get('url', '')
                                })
                    
                    return {
                        'is_promoted': is_promoted,
                        'promotion_type': 'paid' if is_promoted else 'free',
                        'boost_count': boosts.get('active', 0),
                        'dex_id': pair.get('dexId', 'unknown'),
                        'pair_address': pair.get('pairAddress', ''),
                        'pair_created_at': pair.get('pairCreatedAt', 0),
                        'liquidity_usd': float(pair.get('liquidity', {}).get('usd', 0)),
                        'liquidity_eth': float(pair.get('liquidity', {}).get('eth', 0)),
                        'liquidity_btc': float(pair.get('liquidity', {}).get('btc', 0)),
                        'social_links': social_links,
                        'websites': websites
                    }
        except Exception as e:
            logger.error(f"Error fetching DexScreener pricing info: {e}")
        
        return {
            'is_promoted': False,
            'promotion_type': 'free',
            'boost_count': 0,
            'dex_id': 'unknown',
            'pair_address': '',
            'pair_created_at': 0,
            'liquidity_usd': 0,
            'liquidity_eth': 0,
            'liquidity_btc': 0,
            'social_links': [],
            'websites': []
        }
    
    def get_holder_analysis(self, token_address: str, chain: str) -> Dict:
        """Analyze token holders and distribution."""
        try:
            if chain == 'solana':
                return self.analyze_solana_holders(token_address)
            elif chain == 'ethereum':
                return self.analyze_ethereum_holders(token_address)
            elif chain == 'bsc':
                return self.analyze_bsc_holders(token_address)
        except Exception as e:
            logger.error(f"Error in holder analysis: {e}")
        
        return {
            'total_holders': 0,
            'top_10_percentage': 0,
            'top_50_percentage': 0,
            'dev_wallet_percentage': 0,
            'dev_has_sold': False,
            'bundle_detected': False,
            'bundle_percentage': 0,
            'holder_distribution': 'unknown'
        }
    
    def analyze_solana_holders(self, token_address: str) -> Dict:
        """Analyze Solana token holders using Helius API."""
        try:
            # Use Helius API for real Solana holder data
            return self.get_solana_holders_from_helius(token_address)
            
        except Exception as e:
            logger.error(f"Error analyzing Solana holders: {e}")
            return self.get_default_holder_analysis()
    
    def analyze_ethereum_holders(self, token_address: str) -> Dict:
        """Analyze Ethereum token holders using real APIs."""
        try:
            # Try Moralis API for Ethereum holder data
            return self.get_ethereum_holders_from_moralis(token_address)
        except Exception as e:
            logger.error(f"Error analyzing Ethereum holders: {e}")
            return self.get_default_holder_analysis()
    
    def analyze_bsc_holders(self, token_address: str) -> Dict:
        """Analyze BSC token holders using real APIs."""
        try:
            # Try Moralis API for BSC holder data
            return self.get_bsc_holders_from_moralis(token_address)
        except Exception as e:
            logger.error(f"Error analyzing BSC holders: {e}")
            return self.get_default_holder_analysis()
    
    def get_ethereum_holders_from_moralis(self, token_address: str) -> Dict:
        """Get Ethereum holders from Moralis API."""
        try:
            # Moralis API endpoint for token holders
            url = f"https://deep-index.moralis.io/api/v2.2/{token_address}/owners"
            params = {
                'chain': 'eth',
                'limit': 100
            }
            headers = {
                'X-API-Key': 'YOUR_MORALIS_API_KEY'  # Would need actual API key
            }
            
            # For now, try without API key and see what happens
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                holders = data.get('result', [])
                
                if holders and len(holders) > 0:
                    return self.process_holder_data(holders)
            
            return self.get_default_holder_analysis()
            
        except Exception as e:
            logger.error(f"Error getting Ethereum holders from Moralis: {e}")
            return self.get_default_holder_analysis()
    
    def get_bsc_holders_from_moralis(self, token_address: str) -> Dict:
        """Get BSC holders from Moralis API."""
        try:
            # Moralis API endpoint for BSC token holders
            url = f"https://deep-index.moralis.io/api/v2.2/{token_address}/owners"
            params = {
                'chain': 'bsc',
                'limit': 100
            }
            headers = {
                'X-API-Key': 'YOUR_MORALIS_API_KEY'  # Would need actual API key
            }
            
            # For now, try without API key and see what happens
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                holders = data.get('result', [])
                
                if holders and len(holders) > 0:
                    return self.process_holder_data(holders)
            
            return self.get_default_holder_analysis()
            
        except Exception as e:
            logger.error(f"Error getting BSC holders from Moralis: {e}")
            return self.get_default_holder_analysis()
    
    def detect_bundles(self, holders: List[Dict]) -> Tuple[bool, float]:
        """Detect if there are bundled wallets (similar amounts)."""
        try:
            if len(holders) < 5:
                return False, 0
            
            # Group holders by similar amounts (within 5% variance)
            bundles = []
            used_indices = set()
            
            for i, holder in enumerate(holders):
                if i in used_indices:
                    continue
                
                amount = float(holder.get('amount', 0))
                bundle = [holder]
                
                for j, other_holder in enumerate(holders[i+1:], i+1):
                    if j in used_indices:
                        continue
                    
                    other_amount = float(other_holder.get('amount', 0))
                    if other_amount > 0 and abs(amount - other_amount) / amount < 0.05:  # 5% variance
                        bundle.append(other_holder)
                        used_indices.add(j)
                
                if len(bundle) >= 3:  # At least 3 similar wallets
                    bundles.append(bundle)
                    for holder in bundle:
                        used_indices.add(holders.index(holder))
            
            if bundles:
                total_bundle_amount = sum(
                    sum(float(h.get('amount', 0)) for h in bundle) 
                    for bundle in bundles
                )
                total_supply = sum(float(h.get('amount', 0)) for h in holders)
                bundle_percentage = (total_bundle_amount / total_supply * 100) if total_supply > 0 else 0
                
                return True, bundle_percentage
            
            return False, 0
        except Exception as e:
            logger.error(f"Error detecting bundles: {e}")
            return False, 0
    
    def classify_holder_distribution(self, holders: List[Dict]) -> str:
        """Classify holder distribution pattern."""
        try:
            if not holders:
                return 'unknown'
            
            total_supply = sum(float(h.get('amount', 0)) for h in holders)
            if total_supply == 0:
                return 'unknown'
            
            # Calculate concentration
            top_5_amount = sum(float(h.get('amount', 0)) for h in holders[:5])
            top_5_percentage = (top_5_amount / total_supply * 100)
            
            if top_5_percentage > 80:
                return 'highly_concentrated'
            elif top_5_percentage > 50:
                return 'concentrated'
            elif top_5_percentage > 20:
                return 'moderate'
            else:
                return 'distributed'
        except Exception as e:
            logger.error(f"Error classifying holder distribution: {e}")
            return 'unknown'
    
    def process_holder_data(self, holders: List[Dict]) -> Dict:
        """Process holder data from API response."""
        try:
            if not holders:
                return self.get_default_holder_analysis()
            
            total_supply = sum(float(h.get('amount', 0)) for h in holders)
            if total_supply == 0:
                return self.get_default_holder_analysis()
            
            top_10_amount = sum(float(h.get('amount', 0)) for h in holders[:10])
            top_50_amount = sum(float(h.get('amount', 0)) for h in holders[:50])
            
            # Detect potential dev wallet (usually the largest holder)
            dev_wallet = holders[0] if holders else None
            dev_percentage = (float(dev_wallet.get('amount', 0)) / total_supply * 100) if dev_wallet and total_supply > 0 else 0
            
            # Detect bundles (multiple wallets with similar amounts)
            bundle_detected, bundle_percentage = self.detect_bundles(holders)
            
            return {
                'total_holders': len(holders),
                'top_10_percentage': (top_10_amount / total_supply * 100) if total_supply > 0 else 0,
                'top_50_percentage': (top_50_amount / total_supply * 100) if total_supply > 0 else 0,
                'dev_wallet_percentage': dev_percentage,
                'dev_has_sold': False,  # Would need historical data
                'bundle_detected': bundle_detected,
                'bundle_percentage': bundle_percentage,
                'holder_distribution': self.classify_holder_distribution(holders)
            }
        except Exception as e:
            logger.error(f"Error processing holder data: {e}")
            return self.get_default_holder_analysis()
    
    def get_solana_holders_from_helius(self, token_address: str) -> Dict:
        """Get Solana holders from Helius API only with top 10 holders analysis."""
        try:
            # Use Helius API directly
            helius_api_key = "9f2ddbee-ea85-4114-a09f-0690cd0488be"
            holder_data = self.get_holder_distribution_from_helius(token_address, helius_api_key)
            
            # If we get valid data, return it
            if holder_data and holder_data.get('total_holders', 0) > 0:
                return holder_data
            
            # If Helius fails, return None to indicate no real data available
            return None
            
        except Exception as e:
            logger.error(f"Error getting Solana holders from Helius: {e}")
            return None
    
    def get_holder_distribution_from_helius(self, token_address: str, api_key: str) -> Dict:
        """Get holder distribution using Helius token accounts API with top 10 holders."""
        try:
            # Use Helius getTokenAccounts method with higher limit for better analysis
            url = f"https://mainnet.helius-rpc.com/?api-key={api_key}"
            
            payload = {
                "jsonrpc": "2.0",
                "id": "helius-test",
                "method": "getTokenAccounts",
                "params": {
                    "mint": token_address,
                    "limit": 1000  # Increased limit for better analysis
                }
            }
            
            response = self.session.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and data['result']:
                    result = data['result']
                    token_accounts = result.get('token_accounts', [])
                    
                    # Process token accounts to get holder data
                    holders = []
                    total_supply = 0
                    
                    for account in token_accounts:
                        try:
                            # Debug: log the structure of the first account
                            if len(holders) == 0:
                                logger.info(f"Account structure: {account}")
                            
                            # Check if account has the expected structure
                            if not account or not isinstance(account, dict):
                                continue
                                
                            # Get amount directly from the account
                            amount = account.get('amount', 0)
                            if amount and amount > 0:
                                holders.append({
                                    'amount': amount,
                                    'owner': account.get('owner', ''),
                                    'address': account.get('address', '')
                                })
                                total_supply += amount
                                
                        except Exception as e:
                            logger.error(f"Error processing account: {e}")
                            logger.error(f"Account data: {account}")
                            continue
                    
                    if holders:
                        # Sort by amount descending
                        holders.sort(key=lambda x: x['amount'], reverse=True)
                        
                        # Get top 10 holders
                        top_10_holders = holders[:10]
                        top_10_balance = sum(h['amount'] for h in top_10_holders)
                        top_10_percentage = (top_10_balance / total_supply * 100) if total_supply > 0 else 0
                        
                        # Dev wallet analysis (largest holder)
                        dev_wallet = holders[0] if holders else None
                        dev_percentage = (dev_wallet['amount'] / total_supply * 100) if dev_wallet and total_supply > 0 else 0
                        
                        # Calculate other metrics
                        top_50_holders = holders[:50]
                        top_50_balance = sum(h['amount'] for h in top_50_holders)
                        top_50_percentage = (top_50_balance / total_supply * 100) if total_supply > 0 else 0
                        
                        return {
                            'total_holders': len(holders),
                            'total_supply': total_supply,
                            'top_10_percentage': top_10_percentage,
                            'top_50_percentage': top_50_percentage,
                            'dev_wallet_percentage': dev_percentage,
                            'dev_has_sold': False,  # Would need historical data
                            'bundle_detected': top_10_percentage > 50,  # If top 10 hold > 50%
                            'bundle_percentage': top_10_percentage if top_10_percentage > 50 else 0,
                            'holder_distribution': self.classify_holder_distribution(holders),
                            'top_10_holders': [
                                {
                                    'address': h['address'],
                                    'balance': h['amount'],
                                    'percentage': (h['amount'] / total_supply * 100) if total_supply > 0 else 0
                                } for h in top_10_holders
                            ]
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting holder distribution from Helius: {e}")
            return None
    
    def get_solana_holders_from_jupiter(self, token_address: str) -> Dict:
        """Get Solana holders from Jupiter API."""
        try:
            # Try Jupiter API for token info
            url = f"https://quote-api.jup.ag/v6/tokens/{token_address}"
            
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                # Jupiter doesn't provide holder data directly, but we can get token info
                # For now, return default analysis
                return self.get_default_holder_analysis()
            
            return self.get_default_holder_analysis()
            
        except Exception as e:
            logger.error(f"Error getting Solana holders from Jupiter: {e}")
            return self.get_default_holder_analysis()
    
    
    def get_bubblemaps_data(self, token_address: str) -> Dict:
        """Get holder and bundle data from Bubblemaps API."""
        try:
            # Bubblemaps API endpoint for Solana tokens
            url = f"https://api.bubblemaps.io/maps/solana/{token_address}"
            headers = {
                'User-Agent': 'MemeCoinBot/1.0'
            }
            
            response = self.session.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Process Bubblemaps data
                nodes = data.get('nodes', [])
                clusters = data.get('clusters', [])
                relationships = data.get('relationships', [])
                
                if nodes:
                    # Calculate holder statistics
                    total_holders = len(nodes)
                    
                    # Sort by share to get top holders
                    sorted_nodes = sorted(nodes, key=lambda x: x.get('share', 0), reverse=True)
                    
                    # Calculate top holder percentages
                    top_10_shares = sum(node.get('share', 0) for node in sorted_nodes[:10])
                    top_50_shares = sum(node.get('share', 0) for node in sorted_nodes[:50])
                    
                    # Detect dev wallet (usually the largest holder)
                    dev_share = sorted_nodes[0].get('share', 0) if sorted_nodes else 0
                    
                    # Analyze clusters for bundle detection
                    bundle_detected, bundle_percentage = self.analyze_bubblemaps_clusters(clusters, nodes)
                    
                    return {
                        'total_holders': total_holders,
                        'top_10_percentage': top_10_shares,
                        'top_50_percentage': top_50_shares,
                        'dev_wallet_percentage': dev_share,
                        'dev_has_sold': False,  # Would need historical data
                        'bundle_detected': bundle_detected,
                        'bundle_percentage': bundle_percentage,
                        'holder_distribution': self.classify_holder_distribution_from_bubblemaps(sorted_nodes)
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting Bubblemaps data: {e}")
            return None
    
    def analyze_bubblemaps_clusters(self, clusters: List[Dict], nodes: List[Dict]) -> Tuple[bool, float]:
        """Analyze Bubblemaps clusters for bundle detection."""
        try:
            if not clusters or not nodes:
                return False, 0
            
            # Calculate total bundle percentage from clusters
            total_bundle_share = 0
            bundle_count = 0
            
            for cluster in clusters:
                if cluster.get('size', 0) >= 3:  # Clusters with 3+ addresses
                    cluster_share = cluster.get('share', 0)
                    total_bundle_share += cluster_share
                    bundle_count += 1
            
            # Consider it a bundle if we have significant clusters
            bundle_detected = bundle_count > 0 and total_bundle_share > 5  # 5% threshold
            
            return bundle_detected, total_bundle_share
            
        except Exception as e:
            logger.error(f"Error analyzing Bubblemaps clusters: {e}")
            return False, 0
    
    def classify_holder_distribution_from_bubblemaps(self, sorted_nodes: List[Dict]) -> str:
        """Classify holder distribution from Bubblemaps data."""
        try:
            if not sorted_nodes:
                return 'unknown'
            
            # Get top 5 holders' share
            top_5_share = sum(node.get('share', 0) for node in sorted_nodes[:5])
            
            if top_5_share > 80:
                return 'highly_concentrated'
            elif top_5_share > 50:
                return 'concentrated'
            elif top_5_share > 20:
                return 'moderate'
            else:
                return 'distributed'
                
        except Exception as e:
            logger.error(f"Error classifying holder distribution: {e}")
            return 'unknown'
    
    def get_estimated_holder_data(self, token_address: str) -> Dict:
        """Get estimated holder data when APIs fail."""
        try:
            # Try to get basic token info from DexScreener to estimate holder data
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                
                if pairs:
                    pair = pairs[0]
                    market_cap = float(pair.get('marketCap', 0))
                    liquidity = float(pair.get('liquidity', {}).get('usd', 0))
                    
                    # Estimate holders based on market cap and liquidity
                    estimated_holders = self.estimate_holders_from_market_data(market_cap, liquidity)
                    
                    # Calculate realistic percentages based on market cap
                    if market_cap > 10_000_000:  # Large cap tokens
                        top_10_pct = 25.0
                        dev_pct = 8.0
                        bundle_detected = False
                        bundle_pct = 0.0
                        distribution = 'distributed'
                    elif market_cap > 1_000_000:  # Mid cap tokens
                        top_10_pct = 35.0
                        dev_pct = 12.0
                        bundle_detected = False
                        bundle_pct = 0.0
                        distribution = 'moderate'
                    elif market_cap > 100_000:  # Small cap tokens
                        top_10_pct = 45.0
                        dev_pct = 18.0
                        bundle_detected = True
                        bundle_pct = 8.0
                        distribution = 'concentrated'
                    else:  # Micro cap tokens
                        top_10_pct = 60.0
                        dev_pct = 25.0
                        bundle_detected = True
                        bundle_pct = 15.0
                        distribution = 'highly_concentrated'
                    
                    return {
                        'total_holders': estimated_holders,
                        'top_10_percentage': top_10_pct,
                        'top_50_percentage': top_10_pct + 25.0,
                        'dev_wallet_percentage': dev_pct,
                        'dev_has_sold': False,
                        'bundle_detected': bundle_detected,
                        'bundle_percentage': bundle_pct,
                        'holder_distribution': distribution
                    }
            
            # Fallback to reasonable estimates
            return {
                'total_holders': 150,
                'top_10_percentage': 45.0,
                'top_50_percentage': 75.0,
                'dev_wallet_percentage': 15.0,
                'dev_has_sold': False,
                'bundle_detected': True,
                'bundle_percentage': 12.0,
                'holder_distribution': 'moderate'
            }
            
        except Exception as e:
            logger.error(f"Error getting estimated holder data: {e}")
            return self.get_default_holder_analysis()
    
    def estimate_holders_from_market_data(self, market_cap: float, liquidity: float) -> int:
        """Estimate number of holders based on market data."""
        try:
            # Rough estimation based on market cap
            if market_cap > 10_000_000:  # > $10M
                return max(500, int(market_cap / 20_000))
            elif market_cap > 1_000_000:  # > $1M
                return max(200, int(market_cap / 5_000))
            elif market_cap > 100_000:  # > $100K
                return max(100, int(market_cap / 1_000))
            else:
                return max(50, int(market_cap / 500))
        except:
            return 150
    
    def get_default_holder_analysis(self) -> Dict:
        """Return default holder analysis when API calls fail."""
        return {
            'total_holders': 0,
            'top_10_percentage': 0,
            'top_50_percentage': 0,
            'dev_wallet_percentage': 0,
            'dev_has_sold': False,
            'bundle_detected': False,
            'bundle_percentage': 0,
            'holder_distribution': 'unknown'
        }
    
    def get_security_analysis(self, token_address: str, chain: str) -> Dict:
        """Perform security analysis with holder concentration analysis."""
        try:
            # Get holder analysis for security scoring
            holder_analysis = self.get_holder_analysis(token_address, chain)
            
            # Basic security checks
            security_score = 100
            warnings = []
            
            # Check if token is verified
            is_verified = self.check_contract_verification(token_address, chain)
            if not is_verified:
                security_score -= 20
                warnings.append("Contract not verified")
            
            # CRITICAL: Check holder concentration for rug pull risk
            if holder_analysis:
                dev_pct = holder_analysis.get('dev_wallet_percentage', 0)
                top_10_pct = holder_analysis.get('top_10_percentage', 0)
                bundle_detected = holder_analysis.get('bundle_detected', False)
                
                # Dev wallet concentration (CRITICAL RISK)
                if dev_pct > 50:
                    security_score -= 60  # CRITICAL: Dev holds >50%
                    warnings.append("CRITICAL: Dev holds >50% - Extreme rug risk")
                elif dev_pct > 30:
                    security_score -= 40  # HIGH: Dev holds >30%
                    warnings.append("HIGH RISK: Dev holds >30% - High rug risk")
                elif dev_pct > 20:
                    security_score -= 25  # MEDIUM: Dev holds >20%
                    warnings.append("MEDIUM RISK: Dev holds >20% - Moderate rug risk")
                
                # Top 10 holder concentration (BUNDLE RISK)
                if top_10_pct > 70:
                    security_score -= 50  # CRITICAL: Top 10 hold >70%
                    warnings.append("CRITICAL: Top 10 hold >70% - Extreme concentration")
                elif top_10_pct > 50:
                    security_score -= 30  # HIGH: Top 10 hold >50%
                    warnings.append("HIGH RISK: Top 10 hold >50% - High concentration")
                elif top_10_pct > 40:
                    security_score -= 15  # MEDIUM: Top 10 hold >40%
                    warnings.append("MEDIUM RISK: Top 10 hold >40% - Moderate concentration")
                
                # Bundle detection
                if bundle_detected:
                    bundle_pct = holder_analysis.get('bundle_percentage', 0)
                    if bundle_pct > 30:
                        security_score -= 40  # CRITICAL: Bundle >30%
                        warnings.append("CRITICAL: Bundle manipulation detected")
                    elif bundle_pct > 15:
                        security_score -= 25  # HIGH: Bundle >15%
                        warnings.append("HIGH RISK: Bundle manipulation detected")
                    else:
                        security_score -= 10  # MEDIUM: Bundle detected
                        warnings.append("Bundle manipulation detected")
            
            # Check for honeypot indicators
            is_honeypot = self.check_honeypot_indicators(token_address, chain)
            if is_honeypot:
                security_score -= 50
                warnings.append("Potential honeypot detected")
            
            # Check for rug pull indicators
            rug_indicators = self.check_rug_pull_indicators(token_address, chain)
            if rug_indicators:
                security_score -= 30
                warnings.append("Rug pull indicators detected")
            
            return {
                'security_score': max(0, security_score),
                'is_verified': is_verified,
                'is_honeypot': is_honeypot,
                'rug_indicators': rug_indicators,
                'warnings': warnings,
                'risk_level': self.classify_risk_level(security_score)
            }
        except Exception as e:
            logger.error(f"Error in security analysis: {e}")
            return {
                'security_score': 50,
                'is_verified': False,
                'is_honeypot': False,
                'rug_indicators': False,
                'warnings': ['Analysis failed'],
                'risk_level': 'medium'
            }
    
    def check_contract_verification(self, token_address: str, chain: str) -> bool:
        """Check if contract is verified."""
        # This would require specific API calls to each blockchain's explorer
        # For now, return False as default
        return False
    
    def check_honeypot_indicators(self, token_address: str, chain: str) -> bool:
        """Check for honeypot indicators."""
        # This would require specific analysis of contract code
        # For now, return False as default
        return False
    
    def check_rug_pull_indicators(self, token_address: str, chain: str) -> bool:
        """Check for rug pull indicators."""
        # This would require analysis of liquidity, holder distribution, etc.
        # For now, return False as default
        return False
    
    def classify_risk_level(self, security_score: int) -> str:
        """Classify risk level based on security score."""
        if security_score >= 85:
            return 'low'
        elif security_score >= 70:
            return 'medium'
        elif security_score >= 50:
            return 'high'
        else:
            return 'critical'
