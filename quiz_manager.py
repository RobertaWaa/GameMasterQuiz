"""
Quiz file management for GameMaster Quiz
Handles creation and management of custom quizzes
"""

import json
import os

class QuizManager:
    """Manages quiz files and custom quiz creation"""
    
    def __init__(self):
        """Initialize quiz manager"""
        self.default_categories = ["HISTORY", "CHARACTERS", "MECHANICS"]
        self.init_default_quizzes()
    
    def init_default_quizzes(self):
        """Initialize default quiz files if they don't exist"""
        # Create directories first
        os.makedirs("data/quizzes", exist_ok=True)
        os.makedirs("data/quizzes/custom", exist_ok=True)
        
        print("Creating default quiz files...")
        
        # Default HISTORY quiz
        history_file = "data/quizzes/history.json"
        if not os.path.exists(history_file) or os.path.getsize(history_file) == 0:
            history_quiz = {
                "category": "HISTORY",
                "description": "Test your knowledge of gaming history",
                "questions": [
                    {
                        "question": "Which company created the first commercially successful video game 'Pong'?",
                        "options": ["Nintendo", "Atari", "Sega", "Microsoft"],
                        "correct_answer": 1
                    },
                    {
                        "question": "What year was the original PlayStation released?",
                        "options": ["1992", "1994", "1996", "1998"],
                        "correct_answer": 1
                    },
                    {
                        "question": "Which game is credited with popularizing the battle royale genre?",
                        "options": ["Fortnite", "PUBG", "Apex Legends", "Call of Duty: Warzone"],
                        "correct_answer": 1
                    },
                    {
                        "question": "What was the first video game to feature a save function?",
                        "options": ["The Legend of Zelda", "Super Mario Bros.", "Final Fantasy", "Metroid"],
                        "correct_answer": 0
                    },
                    {
                        "question": "Which console was the first to use CDs instead of cartridges?",
                        "options": ["Sega Saturn", "PlayStation", "Sega CD", "Nintendo 64"],
                        "correct_answer": 2
                    }
                ]
            }
            self.save_quiz("history", history_quiz)
            print(f"  Created {history_file}")
        
        # Default CHARACTERS quiz
        characters_file = "data/quizzes/characters.json"
        if not os.path.exists(characters_file) or os.path.getsize(characters_file) == 0:
            characters_quiz = {
                "category": "CHARACTERS",
                "description": "How well do you know gaming characters?",
                "questions": [
                    {
                        "question": "Which character is known for saying 'It's-a me!'?",
                        "options": ["Sonic", "Mario", "Link", "Pikachu"],
                        "correct_answer": 1
                    },
                    {
                        "question": "What is the name of the protagonist in The Legend of Zelda series?",
                        "options": ["Zelda", "Link", "Ganon", "Epona"],
                        "correct_answer": 1
                    },
                    {
                        "question": "Which character is a blue hedgehog?",
                        "options": ["Mario", "Sonic", "Crash Bandicoot", "Spyro"],
                        "correct_answer": 1
                    },
                    {
                        "question": "What is the name of the main character in the Halo series?",
                        "options": ["Master Chief", "Commander Shepard", "Samus Aran", "Gordon Freeman"],
                        "correct_answer": 0
                    },
                    {
                        "question": "Which character uses a crowbar as their primary weapon?",
                        "options": ["Duke Nukem", "Gordon Freeman", "Solid Snake", "Lara Croft"],
                        "correct_answer": 1
                    }
                ]
            }
            self.save_quiz("characters", characters_quiz)
            print(f"  Created {characters_file}")
        
        # Default MECHANICS quiz
        mechanics_file = "data/quizzes/mechanics.json"
        if not os.path.exists(mechanics_file) or os.path.getsize(mechanics_file) == 0:
            mechanics_quiz = {
                "category": "MECHANICS",
                "description": "Test your knowledge of game mechanics",
                "questions": [
                    {
                        "question": "What does 'DPS' stand for in gaming?",
                        "options": ["Damage Per Second", "Defense Point System", "Digital Play Style", "Double Player Score"],
                        "correct_answer": 0
                    },
                    {
                        "question": "What is a 'speedrun'?",
                        "options": ["Completing a game as fast as possible", "Playing with increased movement speed", "A type of racing game", "A game bug"],
                        "correct_answer": 0
                    },
                    {
                        "question": "What does 'NPC' stand for?",
                        "options": ["Non-Player Character", "New Player Character", "Network Play Control", "Non-Playable Content"],
                        "correct_answer": 0
                    },
                    {
                        "question": "What is 'respawning' in games?",
                        "options": ["Repeating a level", "A character coming back to life after death", "Saving the game", "A type of power-up"],
                        "correct_answer": 1
                    },
                    {
                        "question": "What does 'MMO' stand for?",
                        "options": ["Massive Multiplayer Online", "Multiple Mode Operation", "Main Mission Objective", "Multiplayer Match Online"],
                        "correct_answer": 0
                    }
                ]
            }
            self.save_quiz("mechanics", mechanics_quiz)
            print(f"  Created {mechanics_file}")
        
        print("Default quiz files created successfully!")
    
    def save_quiz(self, filename, quiz_data):
        """Save quiz to file"""
        filepath = f"data/quizzes/{filename}.json"
        with open(filepath, 'w') as f:
            json.dump(quiz_data, f, indent=2)
    
    def create_custom_quiz(self, username, quiz_name, questions):
        """Create a custom quiz for a user"""
        quiz_data = {
            "category": "CUSTOM",
            "description": f"Custom quiz by {username}",
            "created_by": username,
            "questions": questions
        }
        
        # Sanitize quiz name for filename
        safe_name = "".join(c for c in quiz_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_').lower()
        
        filename = f"{username}_{safe_name}"
        filepath = f"data/quizzes/custom/{filename}.json"
        
        with open(filepath, 'w') as f:
            json.dump(quiz_data, f, indent=2)
        
        return filename

    def get_available_quizzes(self):
        """Get list of all available quizzes"""
        quizzes = []

        # Add quizzes from data/quizzes/ directory (DEFAULT quizzes)
        quizzes_dir = "data/quizzes"
        if os.path.exists(quizzes_dir):
            for filename in os.listdir(quizzes_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(quizzes_dir, filename)
                    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
                        quiz_name = filename[:-5]  # Remove .json
                        # All quizzes in main directory are default (not custom)
                        quizzes.append((quiz_name, filepath, False))  # False = not custom

        # Add CUSTOM quizzes from custom subdirectory
        custom_dir = "data/quizzes/custom"
        if os.path.exists(custom_dir):
            for filename in os.listdir(custom_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(custom_dir, filename)
                    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
                        quiz_name = filename[:-5]  # Remove .json
                        quizzes.append((quiz_name, filepath, True))  # True = custom

        return quizzes