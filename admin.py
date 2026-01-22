"""
Admin module for GameMaster Quiz
Handles admin-only operations
"""

import json
import os
import shutil
from datetime import datetime


class AdminManager:
    """Handles admin operations"""

    def __init__(self, quiz_game, auth_system, quiz_manager):
        """Initialize admin manager"""
        self.quiz_game = quiz_game
        self.auth_system = auth_system
        self.quiz_manager = quiz_manager

    def backup_data(self, backup_name=None):
        """Create a backup of all data"""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"

        backup_dir = f"backups/{backup_name}"

        try:
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)

            # Copy all data files
            data_files = ["data/users.json", "data/scores.json"]
            data_files.extend(self._get_all_quiz_files())

            for filepath in data_files:
                if os.path.exists(filepath):
                    # Create directory structure in backup
                    rel_path = os.path.relpath(filepath, ".")
                    backup_path = os.path.join(backup_dir, rel_path)
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                    shutil.copy2(filepath, backup_path)

            return True, f"Backup created: {backup_dir}"
        except Exception as e:
            return False, f"Backup failed: {e}"

    def _get_all_quiz_files(self):
        """Get all quiz file paths"""
        quiz_files = []

        # Default quizzes
        for category in ["history", "characters", "mechanics"]:
            filepath = f"data/quizzes/{category}.json"
            if os.path.exists(filepath):
                quiz_files.append(filepath)

        # Custom quizzes
        custom_dir = "data/quizzes/custom"
        if os.path.exists(custom_dir):
            for filename in os.listdir(custom_dir):
                if filename.endswith('.json'):
                    quiz_files.append(os.path.join(custom_dir, filename))

        return quiz_files

    def restore_backup(self, backup_dir):
        """Restore data from backup"""
        if not os.path.exists(backup_dir):
            return False, "Backup directory not found"

        try:
            # Find all JSON files in backup
            backup_files = []
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    if file.endswith('.json'):
                        backup_files.append(os.path.join(root, file))

            # Restore each file
            for backup_file in backup_files:
                # Calculate destination path
                rel_path = os.path.relpath(backup_file, backup_dir)
                dest_path = os.path.join(".", rel_path)

                # Create destination directory
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Copy file
                shutil.copy2(backup_file, dest_path)

            # Reload data
            self.quiz_game.scores = self.quiz_game.load_scores()

            return True, "Backup restored successfully"
        except Exception as e:
            return False, f"Restore failed: {e}"

    def export_quiz(self, quiz_path, export_path=None):
        """Export a quiz to a specified location"""
        if not os.path.exists(quiz_path):
            return False, "Quiz file not found"

        if not export_path:
            quiz_name = os.path.basename(quiz_path).replace('.json', '')
            export_path = f"exports/{quiz_name}_export.json"

        try:
            # Load quiz to validate
            with open(quiz_path, 'r') as f:
                quiz_data = json.load(f)

            # Create export directory
            os.makedirs(os.path.dirname(export_path), exist_ok=True)

            # Save with pretty formatting
            with open(export_path, 'w') as f:
                json.dump(quiz_data, f, indent=2, ensure_ascii=False)

            return True, f"Quiz exported to {export_path}"
        except Exception as e:
            return False, f"Export failed: {e}"

    def import_quiz(self, import_path, target_dir="data/quizzes/custom"):
        """Import a quiz from external file"""
        if not os.path.exists(import_path):
            return False, "Import file not found"

        try:
            # Load and validate quiz structure
            with open(import_path, 'r') as f:
                quiz_data = json.load(f)

            # Validate required fields
            if "questions" not in quiz_data:
                return False, "Invalid quiz format: missing 'questions' field"

            if not isinstance(quiz_data["questions"], list):
                return False, "Invalid quiz format: 'questions' must be a list"

            # Validate each question
            for i, question in enumerate(quiz_data["questions"]):
                if "question" not in question:
                    return False, f"Question {i + 1}: missing 'question' field"
                if "options" not in question:
                    return False, f"Question {i + 1}: missing 'options' field"
                if "correct_answer" not in question:
                    return False, f"Question {i + 1}: missing 'correct_answer' field"

                # Ensure 4 options
                while len(question["options"]) < 4:
                    question["options"].append(f"Option {len(question['options']) + 1}")

            # Generate filename
            quiz_name = quiz_data.get("category", "imported_quiz")
            safe_name = "".join(c for c in quiz_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_').lower()

            filename = f"{safe_name}_imported.json"
            filepath = os.path.join(target_dir, filename)

            # Ensure target directory exists
            os.makedirs(target_dir, exist_ok=True)

            # Save imported quiz
            with open(filepath, 'w') as f:
                json.dump(quiz_data, f, indent=2)

            return True, f"Quiz imported successfully as {filename}"
        except json.JSONDecodeError:
            return False, "Invalid JSON file"
        except Exception as e:
            return False, f"Import failed: {e}"

    def get_system_stats(self):
        """Get comprehensive system statistics"""
        stats = {}

        # User stats
        stats["total_users"] = len(self.auth_system.users)
        stats["total_games_played"] = sum(
            user_data.get("games_played", 0)
            for user_data in self.auth_system.users.values()
        )

        # Score stats
        leaderboard = self.quiz_game.scores.get("leaderboard", [])
        stats["total_score_entries"] = len(leaderboard)
        stats["total_points_scored"] = sum(entry.get("score", 0) for entry in leaderboard)

        # Quiz stats
        quizzes = self.quiz_manager.get_available_quizzes()
        stats["total_quizzes"] = len(quizzes)
        stats["default_quizzes"] = sum(1 for q in quizzes if not q[2])
        stats["custom_quizzes"] = sum(1 for q in quizzes if q[2])

        # Calculate average scores per quiz
        quiz_stats = {}
        for entry in leaderboard:
            quiz_name = entry.get("quiz", "Unknown")
            if quiz_name not in quiz_stats:
                quiz_stats[quiz_name] = {"total_score": 0, "count": 0}
            quiz_stats[quiz_name]["total_score"] += entry.get("score", 0)
            quiz_stats[quiz_name]["count"] += 1

        stats["quiz_averages"] = {
            quiz: data["total_score"] / data["count"] if data["count"] > 0 else 0
            for quiz, data in quiz_stats.items()
        }

        # Top players
        user_stats = self.quiz_game.scores.get("user_stats", {})
        top_players = sorted(
            user_stats.items(),
            key=lambda x: x[1].get("total_score", 0),
            reverse=True
        )[:5]

        stats["top_players"] = [
            {"username": username, "score": data.get("total_score", 0)}
            for username, data in top_players
        ]

        return stats

    def cleanup_orphaned_scores(self):
        """Remove scores for users that no longer exist"""
        try:
            original_count = len(self.quiz_game.scores.get("leaderboard", []))

            # Filter leaderboard
            self.quiz_game.scores["leaderboard"] = [
                entry for entry in self.quiz_game.scores.get("leaderboard", [])
                if entry.get("username") in self.auth_system.users
            ]

            removed_count = original_count - len(self.quiz_game.scores["leaderboard"])

            # Recalculate stats
            self._recalculate_all_stats()

            self.quiz_game.save_scores()

            return True, f"Removed {removed_count} orphaned score entries"
        except Exception as e:
            return False, f"Cleanup failed: {e}"

    def _recalculate_all_stats(self):
        """Recalculate all user statistics"""
        # Reset user stats
        self.quiz_game.scores["user_stats"] = {}

        # Aggregate from leaderboard
        for entry in self.quiz_game.scores.get("leaderboard", []):
            username = entry.get("username")
            if not username:
                continue

            if username not in self.quiz_game.scores["user_stats"]:
                self.quiz_game.scores["user_stats"][username] = {
                    "total_games": 0,
                    "total_score": 0,
                    "average_score": 0
                }

            stats = self.quiz_game.scores["user_stats"][username]
            stats["total_games"] += 1
            stats["total_score"] += entry.get("score", 0)

        # Calculate averages
        for username, stats in self.quiz_game.scores["user_stats"].items():
            if stats["total_games"] > 0:
                stats["average_score"] = stats["total_score"] / stats["total_games"]

        # Update auth system
        for username in self.auth_system.users:
            if username in self.quiz_game.scores["user_stats"]:
                stats = self.quiz_game.scores["user_stats"][username]
                self.auth_system.users[username]["games_played"] = stats["total_games"]
                self.auth_system.users[username]["total_score"] = stats["total_score"]

        self.auth_system.save_users()