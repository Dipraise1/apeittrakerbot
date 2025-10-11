import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import json

class Database:
    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Token scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS token_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                token_address TEXT,
                chain TEXT,
                scan_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                default_chain TEXT DEFAULT 'solana',
                notifications_enabled BOOLEAN DEFAULT TRUE,
                risk_threshold INTEGER DEFAULT 50,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Token watchlist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                token_address TEXT,
                chain TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Add a new user to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, last_active)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, username, first_name, last_name))
        
        # Initialize user preferences
        cursor.execute('''
            INSERT OR IGNORE INTO user_preferences (user_id)
            VALUES (?)
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def log_token_scan(self, user_id: int, token_address: str, chain: str, scan_data: Dict):
        """Log a token scan."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO token_scans (user_id, token_address, chain, scan_data)
            VALUES (?, ?, ?, ?)
        ''', (user_id, token_address, chain, json.dumps(scan_data)))
        
        conn.commit()
        conn.close()
    
    def get_user_scan_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's scan history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT token_address, chain, scan_data, created_at
            FROM token_scans
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'token_address': row[0],
                'chain': row[1],
                'scan_data': json.loads(row[2]),
                'created_at': row[3]
            })
        
        conn.close()
        return results
    
    def add_to_watchlist(self, user_id: int, token_address: str, chain: str) -> bool:
        """Add a token to user's watchlist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already in watchlist
        cursor.execute('''
            SELECT id FROM watchlist
            WHERE user_id = ? AND token_address = ? AND chain = ?
        ''', (user_id, token_address, chain))
        
        if cursor.fetchone():
            conn.close()
            return False  # Already in watchlist
        
        cursor.execute('''
            INSERT INTO watchlist (user_id, token_address, chain)
            VALUES (?, ?, ?)
        ''', (user_id, token_address, chain))
        
        conn.commit()
        conn.close()
        return True
    
    def remove_from_watchlist(self, user_id: int, token_address: str, chain: str) -> bool:
        """Remove a token from user's watchlist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM watchlist
            WHERE user_id = ? AND token_address = ? AND chain = ?
        ''', (user_id, token_address, chain))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    
    def get_watchlist(self, user_id: int) -> List[Dict]:
        """Get user's watchlist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT token_address, chain, added_at
            FROM watchlist
            WHERE user_id = ?
            ORDER BY added_at DESC
        ''', (user_id,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'token_address': row[0],
                'chain': row[1],
                'added_at': row[2]
            })
        
        conn.close()
        return results
    
    def update_user_preferences(self, user_id: int, preferences: Dict):
        """Update user preferences."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_preferences
            SET default_chain = ?, notifications_enabled = ?, risk_threshold = ?
            WHERE user_id = ?
        ''', (
            preferences.get('default_chain', 'solana'),
            preferences.get('notifications_enabled', True),
            preferences.get('risk_threshold', 50),
            user_id
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, user_id: int) -> Dict:
        """Get user preferences."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT default_chain, notifications_enabled, risk_threshold
            FROM user_preferences
            WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'default_chain': row[0],
                'notifications_enabled': bool(row[1]),
                'risk_threshold': row[2]
            }
        else:
            return {
                'default_chain': 'solana',
                'notifications_enabled': True,
                'risk_threshold': 50
            }
    
    def get_popular_tokens(self, limit: int = 10) -> List[Dict]:
        """Get most scanned tokens."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT token_address, chain, COUNT(*) as scan_count
            FROM token_scans
            GROUP BY token_address, chain
            ORDER BY scan_count DESC
            LIMIT ?
        ''', (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'token_address': row[0],
                'chain': row[1],
                'scan_count': row[2]
            })
        
        conn.close()
        return results
    
    def get_scan_stats(self) -> Dict:
        """Get overall scan statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total scans
        cursor.execute('SELECT COUNT(*) FROM token_scans')
        total_scans = cursor.fetchone()[0]
        
        # Unique users
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM token_scans')
        unique_users = cursor.fetchone()[0]
        
        # Scans by chain
        cursor.execute('''
            SELECT chain, COUNT(*) as count
            FROM token_scans
            GROUP BY chain
        ''')
        scans_by_chain = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_scans': total_scans,
            'unique_users': unique_users,
            'scans_by_chain': scans_by_chain
        }
