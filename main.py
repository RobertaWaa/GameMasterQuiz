#!/usr/bin/env python3
"""
GameMaster Quiz - Main Application Entry Point
A gaming quiz platform for video game enthusiasts
"""

import sys
import os
import traceback
from interface import GameMasterApp

def main():
    """Main function to run the GameMaster Quiz application"""
    try:
        print("Starting GameMaster Quiz...")
        
        # Create necessary directories
        os.makedirs("data/quizzes/custom", exist_ok=True)
        print("✓ Directories created/verified")
        
        # Initialize and run the application
        app = GameMasterApp()
        print("✓ Application initialized successfully")
        print("✓ GUI loaded. Enjoy the game!")
        app.run()
        
    except Exception as e:
        print(f"Error starting GameMaster Quiz: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()