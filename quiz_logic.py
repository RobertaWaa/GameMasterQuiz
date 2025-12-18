"""
Quiz logic and scoring system for GameMaster Quiz
"""

import json
import os
import random
from datetime import datetime

SCORES_FILE = "data/scores.json"

class QuizGame:
    """Main quiz game logic"""
    
    def __init__(self, auth_system=None):
        """Initialize quiz game"""
        self.scores = self.load_scores()
        self.current_quiz = None
        self.current_questions = []
        self.current_question_index = 0
        self.score = 0
        self.current_user = None
        self.auth_system = auth_system  # Add reference to auth system
    
    def load_scores(self):
        """Load scores from JSON file"""
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"leaderboard": [], "user_stats": {}}
        return {"leaderboard": [], "user_stats": {}}
    
    def save_scores(self):
        """Save scores to JSON file"""
        os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
        with open(SCORES_FILE, 'w') as f:
            json.dump(self.scores, f, indent=2)
    
    def load_quiz(self, category, custom_quiz=None):
        """Load quiz questions from file"""
        try:
            if custom_quiz:
                quiz_file = f"data/quizzes/custom/{custom_quiz}.json"
            else:
                quiz_file = f"data/quizzes/{category.lower()}.json"
            
            # Check if file exists
            if not os.path.exists(quiz_file):
                print(f"Quiz file not found: {quiz_file}")
                return False
            
            # Check if file is empty
            if os.path.getsize(quiz_file) == 0:
                print(f"Quiz file is empty: {quiz_file}")
                return False
            
            with open(quiz_file, 'r') as f:
                quiz_data = json.load(f)
            
            self.current_quiz = category if not custom_quiz else custom_quiz
            self.current_questions = quiz_data["questions"]
            random.shuffle(self.current_questions)
            self.current_question_index = 0
            self.score = 0
            return True
        except json.JSONDecodeError as e:
            print(f"Error loading quiz JSON from {quiz_file}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error loading quiz: {e}")
            return False
    
    def get_current_question(self):
        """Get the current question"""
        if self.current_question_index < len(self.current_questions):
            return self.current_questions[self.current_question_index]
        return None
    
    def submit_answer(self, answer_index):
        """Submit answer for current question and move to next"""
        if self.current_question_index >= len(self.current_questions):
            return False, "No more questions"
        
        question = self.current_questions[self.current_question_index]
        is_correct = (answer_index == question["correct_answer"])
        
        if is_correct:
            self.score += 10
        
        self.current_question_index += 1
        
        # If quiz is complete, save score
        if self.current_question_index >= len(self.current_questions):
            self.save_score()
        
        return is_correct, question["correct_answer"]
    
    def save_score(self):
        """Save the user's score to leaderboard"""
        if not self.current_user:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        score_entry = {
            "username": self.current_user,
            "score": self.score,
            "quiz": self.current_quiz,
            "date": timestamp
        }
        
        # Add to leaderboard
        self.scores["leaderboard"].append(score_entry)
        
        # Update user stats
        if "user_stats" not in self.scores:
            self.scores["user_stats"] = {}
        
        if self.current_user not in self.scores["user_stats"]:
            self.scores["user_stats"][self.current_user] = {
                "total_games": 0,
                "total_score": 0,
                "average_score": 0
            }
        
        # Update stats
        stats = self.scores["user_stats"][self.current_user]
        stats["total_games"] += 1
        stats["total_score"] += self.score
        stats["average_score"] = stats["total_score"] / stats["total_games"]
        
        # Update auth system if available
        if self.auth_system and self.current_user in self.auth_system.users:
            self.auth_system.users[self.current_user]["games_played"] = stats["total_games"]
            self.auth_system.users[self.current_user]["total_score"] = stats["total_score"]
            self.auth_system.save_users()
        
        # Keep only top 50 scores in leaderboard
        self.scores["leaderboard"].sort(key=lambda x: x["score"], reverse=True)
        self.scores["leaderboard"] = self.scores["leaderboard"][:50]
        
        self.save_scores()
    
    def get_leaderboard(self, limit=10):
        """Get top scores from leaderboard"""
        return self.scores["leaderboard"][:limit]
    
    def get_user_stats_leaderboard(self, limit=10):
        """Get leaderboard based on total user stats"""
        if "user_stats" not in self.scores:
            return []
        
        # Create list from user stats
        stats_list = []
        for username, stats in self.scores["user_stats"].items():
            stats_list.append({
                "username": username,
                "total_games": stats["total_games"],
                "total_score": stats["total_score"],
                "average_score": stats["average_score"]
            })
        
        # Sort by total score (descending)
        stats_list.sort(key=lambda x: x["total_score"], reverse=True)
        return stats_list[:limit]
    
    def get_user_rank(self, username):
        """Get user's rank in the global leaderboard"""
        if "user_stats" not in self.scores or username not in self.scores["user_stats"]:
            return None
        
        stats_list = self.get_user_stats_leaderboard(limit=1000)  # Get all users
        
        for i, entry in enumerate(stats_list):
            if entry["username"] == username:
                return i + 1  # Rank is index + 1
        
        return None
    
    def get_progress(self):
        """Get current quiz progress"""
        total = len(self.current_questions)
        current = self.current_question_index
        return current, total
    
    def is_quiz_complete(self):
        """Check if quiz is complete"""
        return self.current_question_index >= len(self.current_questions)