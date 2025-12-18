"""
Authentication module for GameMaster Quiz
Handles user registration and login with password hashing
"""

import json
import hashlib
import os

DATA_FILE = "data/users.json"

class UserAuth:
    """Handles user authentication and registration"""
    
    def __init__(self):
        """Initialize authentication system"""
        self.users = self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA-256 with salt"""
        salt = "gamesalt2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register(self, username, password):
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        
        # Hash the password before storing
        hashed_password = self.hash_password(password)
        self.users[username] = {
            "password_hash": hashed_password,
            "games_played": 0,
            "total_score": 0
        }
        
        self.save_users()
        return True, "Registration successful"
    
    def login(self, username, password):
        """Authenticate a user"""
        if username not in self.users:
            return False, "User not found"
        
        hashed_password = self.hash_password(password)
        if self.users[username]["password_hash"] == hashed_password:
            return True, "Login successful"
        
        return False, "Incorrect password"
    
    def get_user_stats(self, username):
        """Get user statistics"""
        if username in self.users:
            return self.users[username]
        return None
    
    def update_user_stats(self, username, games_played, total_score):
        """Update user statistics"""
        if username in self.users:
            self.users[username]["games_played"] = games_played
            self.users[username]["total_score"] = total_score
            self.save_users()