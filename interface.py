"""
Graphical user interface for GameMaster Quiz
Built with tkinter
"""

import tkinter as tk
import json
import os
from tkinter import ttk, messagebox, simpledialog
from auth import UserAuth
from quiz_logic import QuizGame
from quiz_manager import QuizManager
from admin import AdminManager

class GameMasterApp:
    """Main application class for GameMaster Quiz"""

    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.title("GameMaster Quiz")
        self.root.geometry("800x600")

        # Set pink theme colors
        self.bg_color = "#fff0f5"  # Lavender blush
        self.main_color = "#ff69b4"  # Hot pink
        self.secondary_color = "#ffb6c1"  # Light pink
        self.text_color = "#4a4a4a"  # Dark gray

        # Configure root window
        self.root.configure(bg=self.bg_color)

        # Initialize components
        self.auth = UserAuth()
        self.quiz_manager = QuizManager()
        self.quiz_game = QuizGame(self.auth)  # Pass auth system to quiz game

        # Current user
        self.current_user = None

        # Start with login screen
        self.show_login_screen()
        self.admin_manager = AdminManager(self.quiz_game, self.auth, self.quiz_manager)

    def check_for_admin_combo(self, event=None):
        """Check for admin combination (type 'admin' in username field)"""
        current_text = self.username_entry.get().lower()

        # Show admin button if "admin" is typed in username field
        if "admin" in current_text and hasattr(self, 'admin_button'):
            self.admin_button.place(x=700, y=10)
        elif hasattr(self, 'admin_button'):
            self.admin_button.place_forget()

    def unlock_admin_panel(self):
        """Unlock and show admin panel"""
        # Clear the fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        # Hide admin button
        if hasattr(self, 'admin_button'):
            self.admin_button.place_forget()

        # Show admin panel
        self.show_admin_panel()

    def show_admin_panel(self):
        """Display admin panel"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="🔧 Admin Panel 🔧",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg="#800080"  # Purple color for admin
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back to Login",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_login_screen
        )
        back_btn.place(x=10, y=10)

        # Admin buttons frame
        admin_frame = tk.Frame(self.root, bg=self.bg_color)
        admin_frame.pack(pady=30)

        # Admin functions
        admin_functions = [
            ("📝 Manage Quizzes", self.manage_quizzes),
            ("📊 Reset All Scores", self.reset_all_scores),
            ("🔄 Reset Quiz Scores", self.reset_quiz_scores),
            ("💾 Backup & Restore", self.show_backup_restore),  # NEW
            ("👥 View All Users", self.view_all_users),
            ("📋 View Statistics", self.view_statistics)
        ]

        for i, (text, command) in enumerate(admin_functions):
            btn = tk.Button(
                admin_frame,
                text=text,
                font=("Arial", 14),
                bg="#800080" if i == 0 else "#9370DB",  # Purple colors
                fg="white",
                width=25,
                height=2,
                command=command
            )
            btn.pack(pady=10)

    def manage_quizzes(self):
        """Display quiz management interface"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="📝 Quiz Management",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#800080"
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back to Admin Panel",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_admin_panel
        )
        back_btn.place(x=10, y=10)

        # In manage_quizzes(), after the title but before the quiz list:

        # Warning label
        warning_label = tk.Label(
            self.root,
            text="⚠️  Caution: Deleting quizzes will remove them permanently!",
            font=("Arial", 10, "bold"),
            bg="#fffacd",  # Light yellow background
            fg="#b8860b",  # Dark goldenrod text
            relief="groove",
            bd=2
        )
        warning_label.pack(pady=10, padx=20, fill="x")

        # Get all quizzes
        quizzes = self.quiz_manager.get_available_quizzes()

        if not quizzes:
            tk.Label(
                self.root,
                text="No quizzes found.",
                font=("Arial", 14),
                bg=self.bg_color,
                fg=self.text_color
            ).pack(pady=100)
            return

        # Create frame for quiz list
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Canvas with scrollbar
        canvas = tk.Canvas(list_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display each quiz
        for quiz_name, filepath, is_custom in quizzes:
            quiz_frame = tk.Frame(
                scrollable_frame,
                bg="#f0e6ff",
                relief="groove",
                bd=2
            )
            quiz_frame.pack(pady=10, padx=10, fill="x")

            # Quiz info
            display_name = quiz_name.replace("_", " ").title()
            quiz_type = "Custom" if is_custom else "Default"

            # Load quiz data to show details
            try:
                with open(filepath, 'r') as f:
                    quiz_data = json.load(f)
                question_count = len(quiz_data.get("questions", []))
                description = quiz_data.get("description", "No description")
                created_by = quiz_data.get("created_by", "System")
            except:
                question_count = 0
                description = "Error loading quiz"
                created_by = "Unknown"

            # Quiz header
            header_frame = tk.Frame(quiz_frame, bg="#f0e6ff")
            header_frame.pack(fill="x", padx=10, pady=5)

            quiz_type = "Custom" if is_custom else "Default"
            type_color = "#9370DB" if is_custom else "#ff69b4"

            tk.Label(
                header_frame,
                text=f"{display_name} ({quiz_type})",
                font=("Arial", 14, "bold"),
                bg="#f0e6ff",
                fg=type_color
            ).pack(side="left")

            tk.Label(
                header_frame,
                text=f"Questions: {question_count}",
                font=("Arial", 10),
                bg="#f0e6ff",
                fg=self.text_color
            ).pack(side="right")

            # Quiz details
            tk.Label(
                quiz_frame,
                text=description,
                font=("Arial", 11),
                bg="#f0e6ff",
                fg=self.text_color,
                wraplength=500
            ).pack(padx=10, pady=2, anchor="w")

            if is_custom:
                tk.Label(
                    quiz_frame,
                    text=f"Created by: {created_by}",
                    font=("Arial", 10, "italic"),
                    bg="#f0e6ff",
                    fg="#666666"
                ).pack(padx=10, pady=2, anchor="w")

            # Action buttons
            action_frame = tk.Frame(quiz_frame, bg="#f0e6ff")
            action_frame.pack(pady=5)

            # Edit button
            tk.Button(
                action_frame,
                text="Edit",
                font=("Arial", 10),
                bg="#9370DB",
                fg="white",
                width=10,
                command=lambda qn=quiz_name, fp=filepath, ic=is_custom: self.edit_quiz(qn, fp, ic)
            ).pack(side="left", padx=5)

            # Delete button
            delete_bg = "#ff6666"  # Red for delete
            tk.Button(
                action_frame,
                text="Delete",
                font=("Arial", 10),
                bg=delete_bg,
                fg="white",
                width=10,
                command=lambda qn=quiz_name, fp=filepath, ic=is_custom: self.delete_quiz(qn, fp, ic)
            ).pack(side="left", padx=5)

            # Create new quiz button at the bottom
        create_frame = tk.Frame(self.root, bg=self.bg_color)
        create_frame.pack(pady=20)

        tk.Button(
            create_frame,
            text="+ Create New Default Quiz",
            font=("Arial", 12, "bold"),
            bg="#800080",
            fg="white",
            width=25,
            command=self.create_new_quiz
        ).pack(pady=10)

    def edit_quiz(self, quiz_name, filepath, is_custom):
        """Edit an existing quiz"""
        # Load quiz data
        try:
            with open(filepath, 'r') as f:
                quiz_data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load quiz: {e}")
            return

        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Quiz: {quiz_name}")
        edit_window.geometry("800x700")
        edit_window.configure(bg=self.bg_color)
        edit_window.transient(self.root)
        edit_window.grab_set()

        # Title
        tk.Label(
            edit_window,
            text=f"Editing: {quiz_name}",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#800080"
        ).pack(pady=20)

        # Main frame with scrollbar
        main_container = tk.Frame(edit_window, bg=self.bg_color)
        main_container.pack(pady=10, padx=20, fill="both", expand=True)

        canvas = tk.Canvas(main_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Quiz info
        info_frame = tk.Frame(scrollable_frame, bg=self.bg_color, relief="groove", bd=2)
        info_frame.pack(pady=10, fill="x", padx=10)

        tk.Label(
            info_frame,
            text="Quiz Information",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=5)

        # Category/Title
        tk.Label(
            info_frame,
            text="Quiz Title/Category:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w", padx=20, pady=2)

        title_var = tk.StringVar(value=quiz_data.get("category", ""))
        title_entry = tk.Entry(info_frame, font=("Arial", 11), width=40, textvariable=title_var)
        title_entry.pack(padx=20, pady=5, fill="x")

        # Description
        tk.Label(
            info_frame,
            text="Description:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w", padx=20, pady=2)

        desc_var = tk.StringVar(value=quiz_data.get("description", ""))
        desc_entry = tk.Entry(info_frame, font=("Arial", 11), width=40, textvariable=desc_var)
        desc_entry.pack(padx=20, pady=5, fill="x")

        # Questions section
        tk.Label(
            scrollable_frame,
            text="Questions",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=10)

        question_widgets = []

        def add_question_widget(question_data=None):
            """Add a question input widget"""
            q_frame = tk.Frame(scrollable_frame, bg="#f9f0ff", relief="groove", bd=1)
            q_frame.pack(pady=5, fill="x", padx=10)

            # Question number
            q_num = len(question_widgets) + 1
            tk.Label(
                q_frame,
                text=f"Question {q_num}:",
                font=("Arial", 10, "bold"),
                bg="#f9f0ff",
                fg=self.text_color
            ).pack(anchor="w", padx=10, pady=5)

            # Question text
            question_entry = tk.Entry(q_frame, font=("Arial", 11), width=50)
            question_entry.pack(padx=10, pady=2, fill="x")

            # Options frame
            options_frame = tk.Frame(q_frame, bg="#f9f0ff")
            options_frame.pack(pady=5, fill="x", padx=20)

            options = []
            for i in range(4):
                tk.Label(
                    options_frame,
                    text=f"Option {i + 1}:",
                    font=("Arial", 9),
                    bg="#f9f0ff",
                    fg=self.text_color
                ).grid(row=i, column=0, padx=5, pady=2, sticky="e")

                option_entry = tk.Entry(options_frame, font=("Arial", 10), width=30)
                option_entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
                options.append(option_entry)

            # Correct answer selection
            tk.Label(
                q_frame,
                text="Correct Answer:",
                font=("Arial", 9),
                bg="#f9f0ff",
                fg=self.text_color
            ).pack(anchor="w", padx=20, pady=2)

            correct_var = tk.IntVar(value=0)
            correct_frame = tk.Frame(q_frame, bg="#f9f0ff")
            correct_frame.pack(pady=2, padx=20)

            for i in range(4):
                tk.Radiobutton(
                    correct_frame,
                    text=f"Option {i + 1}",
                    variable=correct_var,
                    value=i,
                    bg="#f9f0ff",
                    fg=self.text_color,
                    selectcolor="#e6d9ff"
                ).grid(row=0, column=i, padx=8)

            # Remove button
            remove_btn = tk.Button(
                q_frame,
                text="Remove",
                font=("Arial", 8),
                bg="#ffcccc",
                fg="red",
                command=lambda f=q_frame: remove_question(f)
            )
            remove_btn.pack(anchor="e", padx=10, pady=5)

            # Populate with existing data if provided
            if question_data:
                question_entry.insert(0, question_data.get("question", ""))
                for i, option in enumerate(question_data.get("options", [])):
                    if i < 4:
                        options[i].insert(0, option)
                correct_var.set(question_data.get("correct_answer", 0))

            question_widgets.append({
                "frame": q_frame,
                "question": question_entry,
                "options": options,
                "correct": correct_var
            })

        def remove_question(frame):
            """Remove a question widget"""
            for i, q_data in enumerate(question_widgets):
                if q_data["frame"] == frame:
                    frame.destroy()
                    question_widgets.pop(i)
                    # Renumber remaining questions
                    for j, q_data in enumerate(question_widgets, 1):
                        q_data["frame"].winfo_children()[0].config(text=f"Question {j}:")
                    break

        # Add existing questions
        for question in quiz_data.get("questions", []):
            add_question_widget(question)

        # Buttons frame
        buttons_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        buttons_frame.pack(pady=20)

        # Add question button
        tk.Button(
            buttons_frame,
            text="+ Add Question",
            font=("Arial", 10),
            bg="#9370DB",
            fg="white",
            command=lambda: add_question_widget()
        ).pack(side="left", padx=5)

        # Save button
        def save_changes():
            """Save quiz changes"""
            # Collect data
            new_quiz_data = {
                "category": title_var.get(),
                "description": desc_var.get()
            }

            # Add created_by for custom quizzes
            if is_custom:
                new_quiz_data["created_by"] = quiz_data.get("created_by", "Admin")

            # Collect questions
            questions = []
            for q_data in question_widgets:
                question_text = q_data["question"].get().strip()
                if not question_text:
                    continue

                options = []
                for option_entry in q_data["options"]:
                    option_text = option_entry.get().strip()
                    if not option_text:
                        option_text = "Option"
                    options.append(option_text)

                # Ensure we have 4 options
                while len(options) < 4:
                    options.append(f"Option {len(options) + 1}")

                correct_answer = q_data["correct"].get()

                questions.append({
                    "question": question_text,
                    "options": options[:4],  # Ensure exactly 4 options
                    "correct_answer": min(correct_answer, 3)  # Ensure valid index
                })

            if not questions:
                messagebox.showerror("Error", "Quiz must have at least 1 question")
                return

            new_quiz_data["questions"] = questions

            # Save to file
            try:
                with open(filepath, 'w') as f:
                    json.dump(new_quiz_data, f, indent=2)

                messagebox.showinfo("Success", "Quiz saved successfully!")
                edit_window.destroy()
                self.manage_quizzes()  # Refresh the list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save quiz: {e}")

        tk.Button(
            buttons_frame,
            text="Save Changes",
            font=("Arial", 10, "bold"),
            bg="#800080",
            fg="white",
            command=save_changes
        ).pack(side="left", padx=5)

        # Cancel button
        tk.Button(
            buttons_frame,
            text="Cancel",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=edit_window.destroy
        ).pack(side="left", padx=5)

    def delete_quiz(self, quiz_name, filepath, is_custom):
        """Delete a quiz (both default and custom)"""

        # List of protected quizzes that cannot be deleted
        protected_quizzes = ["history", "characters", "mechanics"]

        # Check if this is a protected default quiz
        if not is_custom and quiz_name.lower() in protected_quizzes:
            messagebox.showwarning(
                "Protected Quiz",
                f"Cannot delete '{quiz_name}'!\n\n"
                "This is a core default quiz that is essential for the system.\n"
                "If you need to modify it, please use the 'Edit' feature instead."
            )
            return

        # Determine quiz type for message
        quiz_type = "custom" if is_custom else "default"
        display_name = quiz_name.replace("_", " ").title()

        # Special warning for default quizzes
        warning_msg = ""
        if not is_custom:
            warning_msg = "\n\n⚠️  WARNING: This is a default quiz!\nDeleting it will remove it from the system permanently."

        response = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{display_name}' ({quiz_type} quiz)?{warning_msg}\n\n"
            "This action cannot be undone!"
        )

        if response:
            try:
                # Delete the file
                os.remove(filepath)

                # Also delete from quiz_manager's cache if it exists
                if hasattr(self.quiz_manager, 'quizzes_cache'):
                    # Refresh the available quizzes cache
                    self.quiz_manager.get_available_quizzes = self.quiz_manager.get_available_quizzes.__func__

                # Show success message
                messagebox.showinfo("Success", f"Quiz '{display_name}' deleted successfully!")

                # Refresh the quiz management screen
                self.manage_quizzes()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete quiz: {e}")

    def create_new_quiz(self):
        """Create a new default quiz"""
        # Simple dialog for new quiz name
        quiz_name = simpledialog.askstring(
            "New Quiz",
            "Enter name for new quiz:",
            parent=self.root
        )

        if not quiz_name:
            return

        # Sanitize filename
        safe_name = "".join(c for c in quiz_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_').lower()

        # Save in DEFAULT quizzes directory
        filepath = f"data/quizzes/{safe_name}.json"

        # Check if already exists
        if os.path.exists(filepath):
            messagebox.showerror("Error", f"A quiz named '{quiz_name}' already exists!")
            return

        # Create empty quiz template
        new_quiz = {
            "category": quiz_name.upper(),
            "description": "New quiz created by admin",
            "questions": [
                {
                    "question": "Enter your first question here",
                    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "correct_answer": 0
                }
            ]
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(new_quiz, f, indent=2)

            # Now edit the new quiz (False = not custom)
            self.edit_quiz(safe_name, filepath, False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create quiz: {e}")

    def reset_all_scores(self):
        """Reset all scores and leaderboards"""
        response = messagebox.askyesno(
            "Confirm Reset",
            "⚠️  WARNING: This will reset ALL scores for ALL users!\n\n"
            "All leaderboards and user statistics will be cleared.\n"
            "This action cannot be undone!\n\n"
            "Are you sure you want to continue?"
        )

        if response:
            try:
                # Reset scores.json
                self.quiz_game.scores = {"leaderboard": [], "user_stats": {}}
                self.quiz_game.save_scores()

                # Reset user stats in auth system
                for username in self.auth.users:
                    self.auth.users[username]["games_played"] = 0
                    self.auth.users[username]["total_score"] = 0
                self.auth.save_users()

                messagebox.showinfo("Success", "All scores have been reset successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset scores: {e}")

    def reset_quiz_scores(self):
        """Reset scores for a specific quiz"""
        # Get list of all quizzes
        quizzes = self.quiz_manager.get_available_quizzes()

        if not quizzes:
            messagebox.showinfo("No Quizzes", "No quizzes found to reset.")
            return

        # Create selection dialog
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Quiz to Reset")
        select_window.geometry("500x400")
        select_window.configure(bg=self.bg_color)
        select_window.transient(self.root)
        select_window.grab_set()

        tk.Label(
            select_window,
            text="Select Quiz to Reset Scores",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg="#800080"
        ).pack(pady=20)

        # Listbox for quiz selection
        listbox_frame = tk.Frame(select_window, bg=self.bg_color)
        listbox_frame.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame)
        quiz_listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 11),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=quiz_listbox.yview)

        quiz_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add quizzes to listbox
        quiz_data = []
        for quiz_name, filepath, is_custom in quizzes:
            display_name = quiz_name.replace("_", " ").title()
            if is_custom:
                display_name += " (Custom)"
            quiz_listbox.insert(tk.END, display_name)
            quiz_data.append((quiz_name, filepath, is_custom))

        def perform_reset():
            """Reset scores for selected quiz"""
            selection = quiz_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a quiz.")
                return

            idx = selection[0]
            selected_quiz = quiz_data[idx]

            response = messagebox.askyesno(
                "Confirm Reset",
                f"Reset all scores for '{selected_quiz[0].replace('_', ' ').title()}'?\n\n"
                "This will remove all score entries for this quiz from the leaderboard."
            )

            if response:
                try:
                    # Filter out scores for this quiz
                    original_count = len(self.quiz_game.scores["leaderboard"])
                    self.quiz_game.scores["leaderboard"] = [
                        entry for entry in self.quiz_game.scores["leaderboard"]
                        if entry["quiz"] != selected_quiz[0]
                    ]
                    removed_count = original_count - len(self.quiz_game.scores["leaderboard"])

                    # Recalculate user stats
                    self.recalculate_user_stats()

                    self.quiz_game.save_scores()

                    messagebox.showinfo(
                        "Success",
                        f"Reset complete!\nRemoved {removed_count} score entries."
                    )
                    select_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to reset scores: {e}")

        # Buttons
        button_frame = tk.Frame(select_window, bg=self.bg_color)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Reset Selected Quiz",
            font=("Arial", 10, "bold"),
            bg="#800080",
            fg="white",
            command=perform_reset
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=select_window.destroy
        ).pack(side="left", padx=10)

    def recalculate_user_stats(self):
        """Recalculate all user stats after score changes"""
        # Reset user stats
        self.quiz_game.scores["user_stats"] = {}

        # Aggregate scores from leaderboard
        for entry in self.quiz_game.scores["leaderboard"]:
            username = entry["username"]
            score = entry["score"]

            if username not in self.quiz_game.scores["user_stats"]:
                self.quiz_game.scores["user_stats"][username] = {
                    "total_games": 0,
                    "total_score": 0,
                    "average_score": 0
                }

            stats = self.quiz_game.scores["user_stats"][username]
            stats["total_games"] += 1
            stats["total_score"] += score

        # Calculate averages
        for username, stats in self.quiz_game.scores["user_stats"].items():
            if stats["total_games"] > 0:
                stats["average_score"] = stats["total_score"] / stats["total_games"]

        # Update auth system
        for username in self.auth.users:
            if username in self.quiz_game.scores["user_stats"]:
                stats = self.quiz_game.scores["user_stats"][username]
                self.auth.users[username]["games_played"] = stats["total_games"]
                self.auth.users[username]["total_score"] = stats["total_score"]

        self.auth.save_users()

    def view_all_users(self):
        """Display all registered users"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="👥 All Registered Users",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#800080"
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back to Admin Panel",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_admin_panel
        )
        back_btn.place(x=10, y=10)

        if not self.auth.users:
            tk.Label(
                self.root,
                text="No users registered yet.",
                font=("Arial", 14),
                bg=self.bg_color,
                fg=self.text_color
            ).pack(pady=100)
            return

        # Create table
        table_frame = tk.Frame(self.root, bg=self.bg_color)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Headers
        headers = ["Username", "Games Played", "Total Score", "Joined"]

        for col, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                bg="#800080",
                fg="white",
                width=20,
                height=2
            ).grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

        # User rows
        for row, (username, user_data) in enumerate(self.auth.users.items(), start=1):
            # Get stats from scores if available
            user_stats = self.quiz_game.scores.get("user_stats", {}).get(username, {})

            # Username
            tk.Label(
                table_frame,
                text=username,
                font=("Arial", 11, "bold"),
                bg="#f0e6ff" if row % 2 == 0 else self.bg_color,
                fg=self.text_color,
                width=20,
                height=2
            ).grid(row=row, column=0, padx=2, pady=2, sticky="nsew")

            # Games Played
            tk.Label(
                table_frame,
                text=user_stats.get("total_games", user_data.get("games_played", 0)),
                font=("Arial", 11),
                bg="#f0e6ff" if row % 2 == 0 else self.bg_color,
                fg=self.text_color,
                width=20,
                height=2
            ).grid(row=row, column=1, padx=2, pady=2, sticky="nsew")

            # Total Score
            tk.Label(
                table_frame,
                text=user_stats.get("total_score", user_data.get("total_score", 0)),
                font=("Arial", 11),
                bg="#f0e6ff" if row % 2 == 0 else self.bg_color,
                fg=self.text_color,
                width=20,
                height=2
            ).grid(row=row, column=2, padx=2, pady=2, sticky="nsew")

            # Since we don't have join date, show games played from auth
            tk.Label(
                table_frame,
                text="Active User",
                font=("Arial", 10),
                bg="#f0e6ff" if row % 2 == 0 else self.bg_color,
                fg="#666666",
                width=20,
                height=2
            ).grid(row=row, column=3, padx=2, pady=2, sticky="nsew")

        # Configure grid weights
        for i in range(4):
            table_frame.columnconfigure(i, weight=1)

    def view_statistics(self):
        """Display system statistics"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="📊 System Statistics",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#800080"
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back to Admin Panel",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_admin_panel
        )
        back_btn.place(x=10, y=10)

        # Calculate statistics
        total_users = len(self.auth.users)
        total_quizzes = len(self.quiz_manager.get_available_quizzes())
        total_scores = len(self.quiz_game.scores.get("leaderboard", []))

        # Count custom vs default quizzes
        quizzes = self.quiz_manager.get_available_quizzes()
        custom_quizzes = sum(1 for q in quizzes if q[2])
        default_quizzes = total_quizzes - custom_quizzes

        # Get best player
        best_player, best_score = self.quiz_game.get_best_player()

        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#f0e6ff", relief="groove", bd=3)
        stats_frame.pack(pady=20, padx=40, fill="both", expand=True)

        stats_data = [
            ("Total Users:", str(total_users)),
            ("Total Quizzes:", str(total_quizzes)),
            ("  • Default Quizzes:", str(default_quizzes)),
            ("  • Custom Quizzes:", str(custom_quizzes)),
            ("Total Score Entries:", str(total_scores)),
            ("Best Player:", f"{best_player or 'None'} ({best_score or 0} points)"),
            ("Active Quizzes:", ", ".join(sorted(set([q[0] for q in quizzes])))),
            ("System Version:", "GameMaster Quiz v1.0"),
            ("Data Path:", "data/ directory")
        ]

        for i, (label, value) in enumerate(stats_data):
            label_frame = tk.Frame(stats_frame, bg="#f0e6ff")
            label_frame.pack(pady=8, fill="x", padx=20)

            tk.Label(
                label_frame,
                text=label,
                font=("Arial", 12, "bold"),
                bg="#f0e6ff",
                fg="#4B0082",
                width=20,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                label_frame,
                text=value,
                font=("Arial", 12),
                bg="#f0e6ff",
                fg=self.text_color,
                wraplength=400,
                justify="left"
            ).pack(side="left", padx=10)

    def run(self):
        """Run the application"""
        self.root.mainloop()

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Display login/registration screen"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="🎮 Game Master Quiz 🎮",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=30)

        subtitle_label = tk.Label(
            self.root,
            text="Test Your Gaming Knowledge!",
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle_label.pack(pady=5)

        # Login frame
        login_frame = tk.Frame(self.root, bg=self.bg_color)
        login_frame.pack(pady=20)

        # Username
        tk.Label(
            login_frame,
            text="Username:",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        ).grid(row=0, column=0, padx=5, pady=10, sticky="e")

        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25)
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)

        # Password
        tk.Label(
            login_frame,
            text="Password:",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        ).grid(row=1, column=0, padx=5, pady=10, sticky="e")

        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)

        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=20)

        # Login button
        login_btn = tk.Button(
            buttons_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg=self.main_color,
            fg="white",
            width=15,
            command=self.login
        )
        login_btn.grid(row=0, column=0, padx=10)

        # Register button
        register_btn = tk.Button(
            buttons_frame,
            text="Register",
            font=("Arial", 12),
            bg=self.secondary_color,
            fg=self.text_color,
            width=15,
            command=self.register
        )
        register_btn.grid(row=0, column=1, padx=10)

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())

        # Admin button (hidden by default)
        self.admin_button = tk.Button(
            self.root,
            text="🔧 ADMIN",
            font=("Arial", 8, "bold"),
            bg="#800080",
            fg="white",
            command=self.unlock_admin_panel
        )
        self.admin_button.place(x=700, y=10)
        self.admin_button.place_forget()  # Hide initially

        # Bind key events for admin detection
        self.username_entry.bind('<KeyRelease>', self.check_for_admin_combo)

    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        success, message = self.auth.login(username, password)

        if success:
            self.current_user = username
            self.quiz_game.current_user = username
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", message)

    def register(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        success, message = self.auth.register(username, password)

        if success:
            messagebox.showinfo("Success", message)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Registration Failed", message)

    def show_main_menu(self):
        """Display the main menu after login"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text=f"Welcome, {self.current_user}! 🎮",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=20)

        # User stats
        stats = self.quiz_game.scores.get("user_stats", {}).get(self.current_user, {})

        if stats:
            # Get user rank
            user_rank = self.quiz_game.get_user_rank(self.current_user)
            rank_text = f"Global Rank: #{user_rank}" if user_rank else ""

            stats_text = f"Games Played: {stats.get('total_games', 0)} | Total Score: {stats.get('total_score', 0)} | {rank_text}"
            stats_label = tk.Label(
                self.root,
                text=stats_text,
                font=("Arial", 12),
                bg=self.bg_color,
                fg=self.text_color
            )
            stats_label.pack(pady=10)

        # Menu buttons
        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.pack(pady=30)

        buttons = [
            ("Play Quiz", self.show_quiz_selection),
            ("Leaderboard", self.show_leaderboard_selection),
            ("Diploma", self.show_diploma_screen),  # NEW: Added Diploma button
            ("Create Custom Quiz", self.show_custom_quiz_creator),
            ("Logout", self.logout)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                menu_frame,
                text=text,
                font=("Arial", 14),
                bg=self.main_color if i == 0 else self.secondary_color,
                fg="white",
                width=25,
                height=2,
                command=command
            )
            btn.pack(pady=10)

    def show_leaderboard_selection(self):
        """Display leaderboard type selection"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="Leaderboards",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_main_menu
        )
        back_btn.place(x=10, y=10)

        # Leaderboard buttons frame
        lb_frame = tk.Frame(self.root, bg=self.bg_color)
        lb_frame.pack(pady=40)

        # Recent Scores button
        recent_btn = tk.Button(
            lb_frame,
            text="Recent High Scores",
            font=("Arial", 14),
            bg=self.main_color,
            fg="white",
            width=30,
            height=3,
            command=lambda: self.show_leaderboard("recent")
        )
        recent_btn.pack(pady=15)

        # Total Score Leaderboard button
        total_btn = tk.Button(
            lb_frame,
            text="Total Score Leaderboard",
            font=("Arial", 14),
            bg=self.main_color,
            fg="white",
            width=30,
            height=3,
            command=lambda: self.show_leaderboard("total")
        )
        total_btn.pack(pady=15)

    def show_quiz_selection(self):
        """Display quiz category selection"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="Select Quiz Category",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_main_menu
        )
        back_btn.place(x=10, y=10)

        # Get ALL quizzes
        all_quizzes = self.quiz_manager.get_available_quizzes()

        # Separate quizzes
        default_quizzes = [q for q in all_quizzes if not q[2]]  # Non-custom
        custom_quizzes = [q for q in all_quizzes if q[2]]  # Custom

        # Create main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # ========== DEFAULT QUIZZES SECTION ==========
        if default_quizzes:
            # Label for default quizzes
            tk.Label(
                main_container,
                text="Available Quizzes",
                font=("Arial", 18, "bold"),
                bg=self.bg_color,
                fg=self.main_color
            ).pack(pady=(0, 15))

            # Create a frame to hold the scrollable area
            scroll_container = tk.Frame(main_container, bg=self.bg_color)
            scroll_container.pack(fill="both", expand=True)

            # Create canvas and scrollbar
            canvas = tk.Canvas(scroll_container, bg=self.bg_color, highlightthickness=0)
            scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)

            # Frame inside canvas for quizzes (this will be centered)
            scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

            # Configure scrolling
            def configure_scroll(event=None):
                canvas.configure(scrollregion=canvas.bbox("all"))

            scrollable_frame.bind("<Configure>", configure_scroll)

            # Add scrollable frame to canvas (centered)
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

            def center_frame(event=None):
                """Center the scrollable frame horizontally"""
                canvas_width = canvas.winfo_width()
                # Update the window width to match canvas
                canvas.itemconfig(canvas_window, width=canvas_width)
                # Center the frame
                frame_width = scrollable_frame.winfo_reqwidth()
                x_position = max(0, (canvas_width - frame_width) // 2)
                canvas.coords(canvas_window, x_position, 0)

            canvas.bind("<Configure>", center_frame)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # ========== DISPLAY DEFAULT QUIZZES AS CENTERED RECTANGLES ==========
            for quiz_name, filepath, is_custom in default_quizzes:
                # Load quiz to get description
                try:
                    with open(filepath, 'r') as f:
                        quiz_data = json.load(f)
                    description = quiz_data.get("description", "Test your knowledge")
                    display_name = quiz_data.get("category", quiz_name.replace("_", " ").title())
                except:
                    description = "Quiz description"
                    display_name = quiz_name.replace("_", " ").title()

                # QUIZ FRAME - FIXED SIZE RECTANGLE (like original)
                category_frame = tk.Frame(
                    scrollable_frame,
                    bg=self.bg_color,
                    highlightbackground=self.main_color,
                    highlightthickness=2,
                    width=500,  # FIXED WIDTH
                    height=180  # FIXED HEIGHT
                )
                category_frame.pack(pady=10)
                category_frame.pack_propagate(False)  # PREVENT FRAME FROM SHRINKING TO FIT CONTENT

                # Inner frame for content with proper padding
                content_frame = tk.Frame(category_frame, bg=self.bg_color)
                content_frame.place(relx=0.5, rely=0.5, anchor="center")  # CENTER CONTENT INSIDE FRAME

                # Quiz title
                tk.Label(
                    content_frame,
                    text=display_name,
                    font=("Arial", 16, "bold"),
                    bg=self.bg_color,
                    fg=self.main_color
                ).pack(pady=5)

                # Quiz description
                desc_label = tk.Label(
                    content_frame,
                    text=description,
                    font=("Arial", 12),
                    bg=self.bg_color,
                    fg=self.text_color,
                    wraplength=450,  # Slightly less than frame width
                    justify="center"
                )
                desc_label.pack(pady=5)

                # Play button
                tk.Button(
                    content_frame,
                    text="Play",
                    font=("Arial", 12),
                    bg=self.main_color,
                    fg="white",
                    width=15,
                    command=lambda q=quiz_name: self.start_quiz(q)
                ).pack(pady=10)
        else:
            # No default quizzes message
            tk.Label(
                main_container,
                text="No quizzes available yet.",
                font=("Arial", 14, "italic"),
                bg=self.bg_color,
                fg=self.text_color
            ).pack(pady=50)

        # ========== CUSTOM QUIZZES SECTION ==========
        if custom_quizzes:
            # Separator line
            separator = tk.Frame(main_container, height=2, bg=self.main_color)
            separator.pack(fill="x", pady=20)

            # Label for custom quizzes
            tk.Label(
                main_container,
                text="Custom Quizzes",
                font=("Arial", 18, "bold"),
                bg=self.bg_color,
                fg=self.main_color
            ).pack(pady=(0, 15))

            # Display custom quizzes
            custom_frame = tk.Frame(main_container, bg=self.bg_color)
            custom_frame.pack()

            for quiz_name, _, _ in custom_quizzes:
                display_name = quiz_name.replace("_", " ").title()
                # Remove username prefix for display
                if "_" in display_name and self.current_user and display_name.startswith(self.current_user.title()):
                    display_name = display_name[len(self.current_user) + 1:] + " (Custom)"

                btn = tk.Button(
                    custom_frame,
                    text=display_name,
                    font=("Arial", 12),
                    bg=self.secondary_color,
                    fg=self.text_color,
                    width=30,
                    command=lambda q=quiz_name: self.start_quiz("custom", q)
                )
                btn.pack(pady=5)

    def start_quiz(self, category, custom_quiz=None):
        """Start a quiz"""
        success = self.quiz_game.load_quiz(category, custom_quiz)

        if not success:
            messagebox.showerror("Error", f"Failed to load quiz. The quiz file may be empty or corrupted.\n\nCategory: {category}\nCustom: {custom_quiz}")
            return

        self.show_quiz_question()

    def show_quiz_question(self):
        """Display the current quiz question"""
        self.clear_window()

        # Get current question
        question_data = self.quiz_game.get_current_question()

        if not question_data:
            self.show_quiz_results()
            return

        # Progress
        current, total = self.quiz_game.get_progress()
        progress_label = tk.Label(
            self.root,
            text=f"Question {current + 1} of {total}",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        progress_label.pack(pady=10)

        # Score
        score_label = tk.Label(
            self.root,
            text=f"Score: {self.quiz_game.score}",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        score_label.pack(pady=5)

        # Question
        question_label = tk.Label(
            self.root,
            text=question_data["question"],
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=600,
            justify="center"
        )
        question_label.pack(pady=30, padx=20)

        # Options frame
        options_frame = tk.Frame(self.root, bg=self.bg_color)
        options_frame.pack(pady=20)

        # Create option buttons
        for i, option in enumerate(question_data["options"]):
            btn = tk.Button(
                options_frame,
                text=option,
                font=("Arial", 14),
                bg=self.secondary_color,
                fg=self.text_color,
                width=40,
                height=2,
                wraplength=500,
                command=lambda idx=i: self.submit_answer(idx)
            )
            btn.pack(pady=10)

        # Quit button
        quit_btn = tk.Button(
            self.root,
            text="Quit Quiz",
            font=("Arial", 10),
            bg="#ffcccc",
            fg="red",
            command=self.show_main_menu
        )
        quit_btn.pack(pady=20)

    def submit_answer(self, answer_index):
        """Submit answer and show feedback"""
        is_correct, correct_answer = self.quiz_game.submit_answer(answer_index)

        # Get the correct answer text
        question_data = self.quiz_game.current_questions[self.quiz_game.current_question_index - 1]
        correct_answer_text = question_data["options"][correct_answer]

        # Show feedback
        if is_correct:
            messagebox.showinfo("Correct!", "Well done! +10 points")
        else:
            messagebox.showinfo("Incorrect", f"The correct answer was: {correct_answer_text}")

        # Move to next question or show results
        if self.quiz_game.is_quiz_complete():
            self.show_quiz_results()
        else:
            self.show_quiz_question()

    def show_quiz_results(self):
        """Display quiz results"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="Quiz Complete! 🎉",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=30)

        # Score
        score_label = tk.Label(
            self.root,
            text=f"Your Score: {self.quiz_game.score}",
            font=("Arial", 36, "bold"),
            bg=self.bg_color,
            fg="#4CAF50"  # Green for score
        )
        score_label.pack(pady=20)

        # Get updated stats
        stats = self.quiz_game.scores.get("user_stats", {}).get(self.current_user, {})
        user_rank = self.quiz_game.get_user_rank(self.current_user)

        # Stats info
        stats_text = f"Games Played: {stats.get('total_games', 0)} | Total Score: {stats.get('total_score', 0)}"
        if user_rank:
            stats_text += f" | Global Rank: #{user_rank}"

        stats_label = tk.Label(
            self.root,
            text=stats_text,
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        stats_label.pack(pady=10)

        # Message based on score
        total_questions = len(self.quiz_game.current_questions)
        max_score = total_questions * 10
        percentage = (self.quiz_game.score / max_score) * 100 if max_score > 0 else 0

        if percentage >= 80:
            message = "Excellent! You're a true gaming master! 🏆"
        elif percentage >= 60:
            message = "Great job! You know your games well! 👍"
        elif percentage >= 40:
            message = "Good effort! Keep practicing! 💪"
        else:
            message = "Keep playing to improve your knowledge! 🎮"

        message_label = tk.Label(
            self.root,
            text=message,
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=500
        )
        message_label.pack(pady=20)

        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=30)

        # Play again button
        play_again_btn = tk.Button(
            buttons_frame,
            text="Play Again",
            font=("Arial", 12, "bold"),
            bg=self.main_color,
            fg="white",
            width=15,
            command=self.show_quiz_selection
        )
        play_again_btn.grid(row=0, column=0, padx=10)

        # Main menu button
        menu_btn = tk.Button(
            buttons_frame,
            text="Main Menu",
            font=("Arial", 12),
            bg=self.secondary_color,
            fg=self.text_color,
            width=15,
            command=self.show_main_menu
        )
        menu_btn.grid(row=0, column=1, padx=10)

    def show_leaderboard(self, lb_type="recent"):
        """Display the leaderboard"""
        self.clear_window()

        # Title based on type
        if lb_type == "recent":
            title_text = "🏆 Recent High Scores 🏆"
        else:
            title_text = "🏆 Total Score Leaderboard 🏆"

        title_label = tk.Label(
            self.root,
            text=title_text,
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back to Leaderboards",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_leaderboard_selection
        )
        back_btn.place(x=10, y=10)

        # Get leaderboard data based on type
        if lb_type == "recent":
            leaderboard = self.quiz_game.get_leaderboard(limit=20)
            headers = ["Rank", "Username", "Score", "Quiz", "Date"]
        else:
            leaderboard = self.quiz_game.get_user_stats_leaderboard(limit=20)
            headers = ["Rank", "Username", "Total Score", "Games Played", "Avg. Score"]

        if not leaderboard:
            no_data_label = tk.Label(
                self.root,
                text="No scores yet. Be the first to play!",
                font=("Arial", 16),
                bg=self.bg_color,
                fg=self.text_color
            )
            no_data_label.pack(pady=100)
            return

        # Create table frame
        table_frame = tk.Frame(self.root, bg=self.bg_color)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Table headers
        for col, header in enumerate(headers):
            header_label = tk.Label(
                table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                bg=self.main_color,
                fg="white",
                width=15 if col != 3 else 20,
                height=2
            )
            header_label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

        # Table rows
        for row, entry in enumerate(leaderboard, start=1):
            # Rank
            rank_label = tk.Label(
                table_frame,
                text=f"#{row}",
                font=("Arial", 12, "bold"),
                bg=self.secondary_color if row % 2 == 0 else self.bg_color,
                fg=self.main_color if row <= 3 else self.text_color,
                width=15,
                height=2
            )
            rank_label.grid(row=row, column=0, padx=2, pady=2, sticky="nsew")

            # Username (highlight current user)
            is_current_user = entry["username"] == self.current_user
            username_bg = "#ffd9ec" if is_current_user else (self.secondary_color if row % 2 == 0 else self.bg_color)
            username_fg = self.main_color if is_current_user else self.text_color

            username_label = tk.Label(
                table_frame,
                text=entry["username"],
                font=("Arial", 12, "bold" if is_current_user else "normal"),
                bg=username_bg,
                fg=username_fg,
                width=15,
                height=2
            )
            username_label.grid(row=row, column=1, padx=2, pady=2, sticky="nsew")

            # Score or Total Score
            if lb_type == "recent":
                score_text = entry["score"]
            else:
                score_text = entry["total_score"]

            score_label = tk.Label(
                table_frame,
                text=score_text,
                font=("Arial", 12, "bold"),
                bg=self.secondary_color if row % 2 == 0 else self.bg_color,
                fg=self.text_color,
                width=15,
                height=2
            )
            score_label.grid(row=row, column=2, padx=2, pady=2, sticky="nsew")

            # Third column (Quiz/Date or Games Played)
            if lb_type == "recent":
                col3_text = entry["quiz"]
                col3_width = 20
            else:
                col3_text = entry["total_games"]
                col3_width = 15

            col3_label = tk.Label(
                table_frame,
                text=col3_text,
                font=("Arial", 10 if lb_type == "recent" else 12),
                bg=self.secondary_color if row % 2 == 0 else self.bg_color,
                fg=self.text_color,
                width=col3_width,
                height=2,
                wraplength=150 if lb_type == "recent" else None
            )
            col3_label.grid(row=row, column=3, padx=2, pady=2, sticky="nsew")

            # Fourth column (Date or Avg. Score)
            if lb_type == "recent":
                col4_text = entry["date"]
            else:
                col4_text = f"{entry['average_score']:.1f}"

            col4_label = tk.Label(
                table_frame,
                text=col4_text,
                font=("Arial", 10),
                bg=self.secondary_color if row % 2 == 0 else self.bg_color,
                fg=self.text_color,
                width=15,
                height=2
            )
            col4_label.grid(row=row, column=4, padx=2, pady=2, sticky="nsew")

        # Configure grid weights
        for i in range(len(headers)):
            table_frame.columnconfigure(i, weight=1)

        # Add current user info if not in top 20
        if lb_type == "total":
            user_rank = self.quiz_game.get_user_rank(self.current_user)
            if user_rank and user_rank > 20:
                user_stats = self.quiz_game.scores.get("user_stats", {}).get(self.current_user, {})
                if user_stats:
                    user_info = tk.Label(
                        self.root,
                        text=f"Your rank: #{user_rank} | Total Score: {user_stats.get('total_score', 0)} | Games: {user_stats.get('total_games', 0)}",
                        font=("Arial", 11, "bold"),
                        bg="#ffd9ec",
                        fg=self.main_color,
                        pady=10
                    )
                    user_info.pack(pady=10, fill="x")

    def show_custom_quiz_creator(self):
        """Display custom quiz creator"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="Create Custom Quiz",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_main_menu
        )
        back_btn.place(x=10, y=10)

        # Instructions
        instructions = tk.Label(
            self.root,
            text="Create your own gaming quiz! Add questions with 4 options each.\nAfter creating, it will appear in the 'Custom Quizzes' section.",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=600
        )
        instructions.pack(pady=10)

        # Main frame with scrollbar
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Create a canvas with scrollbar
        canvas = tk.Canvas(main_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Quiz name
        tk.Label(
            scrollable_frame,
            text="Quiz Name:",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w", pady=5)

        self.quiz_name_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=40)
        self.quiz_name_entry.pack(pady=5, fill="x")

        # Questions list frame
        self.questions_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        self.questions_frame.pack(pady=20, fill="both", expand=True)

        # List to store question entries
        self.question_widgets = []

        # Add first question
        self.add_question_widget()

        # Buttons frame
        buttons_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        buttons_frame.pack(pady=20)

        # Add question button
        add_btn = tk.Button(
            buttons_frame,
            text="+ Add Another Question",
            font=("Arial", 12),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.add_question_widget
        )
        add_btn.grid(row=0, column=0, padx=10)

        # Create quiz button
        create_btn = tk.Button(
            buttons_frame,
            text="Create Quiz",
            font=("Arial", 12, "bold"),
            bg=self.main_color,
            fg="white",
            command=self.create_custom_quiz
        )
        create_btn.grid(row=0, column=1, padx=10)

    def add_question_widget(self):
        """Add a question input widget"""
        question_num = len(self.question_widgets) + 1

        # Question frame
        q_frame = tk.Frame(self.questions_frame, bg=self.bg_color, relief="groove", bd=2)
        q_frame.pack(pady=10, fill="x", padx=5)

        # Question number
        tk.Label(
            q_frame,
            text=f"Question {question_num}:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        ).pack(anchor="w", pady=5)

        # Question text
        question_entry = tk.Entry(q_frame, font=("Arial", 12), width=50)
        question_entry.pack(pady=5, fill="x", padx=10)

        # Options frame
        options_frame = tk.Frame(q_frame, bg=self.bg_color)
        options_frame.pack(pady=10, fill="x", padx=20)

        options = []
        for i in range(4):
            tk.Label(
                options_frame,
                text=f"Option {i+1}:",
                font=("Arial", 10),
                bg=self.bg_color,
                fg=self.text_color
            ).grid(row=i, column=0, padx=5, pady=3, sticky="e")

            option_entry = tk.Entry(options_frame, font=("Arial", 11), width=30)
            option_entry.grid(row=i, column=1, padx=5, pady=3, sticky="w")
            options.append(option_entry)

        # Correct answer selection
        tk.Label(
            q_frame,
            text="Correct Answer:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w", padx=20, pady=5)

        correct_var = tk.IntVar(value=0)
        correct_frame = tk.Frame(q_frame, bg=self.bg_color)
        correct_frame.pack(pady=5, padx=20)

        for i in range(4):
            rb = tk.Radiobutton(
                correct_frame,
                text=f"Option {i+1}",
                variable=correct_var,
                value=i,
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor=self.secondary_color
            )
            rb.grid(row=0, column=i, padx=10)

        # Store widget references
        self.question_widgets.append({
            "frame": q_frame,
            "question": question_entry,
            "options": options,
            "correct": correct_var
        })

    def create_custom_quiz(self):
        """Create the custom quiz from user input"""
        quiz_name = self.quiz_name_entry.get().strip()

        if not quiz_name:
            messagebox.showerror("Error", "Please enter a quiz name")
            return

        # Collect questions
        questions = []
        for i, q_data in enumerate(self.question_widgets):
            question_text = q_data["question"].get().strip()

            # Check if question is empty
            if not question_text:
                continue

            options = []
            for j, option_entry in enumerate(q_data["options"]):
                option_text = option_entry.get().strip()
                if not option_text:
                    option_text = f"Option {j+1}"
                options.append(option_text)

            correct_answer = q_data["correct"].get()

            # Make sure we have at least 2 non-empty options
            non_empty_options = [opt for opt in options if opt.strip()]
            if len(non_empty_options) < 2:
                messagebox.showerror("Error", f"Question {i+1} needs at least 2 non-empty options")
                return

            questions.append({
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer
            })

        if len(questions) < 1:
            messagebox.showerror("Error", "You need at least 1 question")
            return

        # Create the quiz
        filename = self.quiz_manager.create_custom_quiz(
            self.current_user,
            quiz_name,
            questions
        )

        messagebox.showinfo("Success", f"Quiz '{quiz_name}' created successfully!\n\nIt will now appear in the 'Custom Quizzes' section when you select 'Play Quiz'.")
        self.show_main_menu()

    def logout(self):
        """Logout the current user"""
        self.current_user = None
        self.quiz_game.current_user = None
        self.show_login_screen()


    def show_diploma_screen(self):
        """Display the diploma screen"""
        self.clear_window()

        # Get best player info
        best_username, best_score = self.quiz_game.get_best_player()
        user_score, user_rank = self.quiz_game.get_user_score_and_rank(self.current_user)
        score_difference = self.quiz_game.get_score_difference(self.current_user)

        # Check if current user is the best
        is_best_player = (self.current_user == best_username)

        # Title
        title_label = tk.Label(
            self.root,
            text="🏆 Hall of Fame 🏆",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_main_menu
        )
        back_btn.place(x=10, y=10)

        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=30, padx=20, fill="both", expand=True)

        if is_best_player:
            # Show diploma for best player
            self.show_victory_diploma(content_frame, user_score, user_rank)
        else:
            # Show encouragement message
            self.show_encouragement_message(content_frame, best_username, best_score,
                                          user_score, user_rank, score_difference)

        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=20)

        # Play Quiz button to improve score
        play_btn = tk.Button(
            buttons_frame,
            text="Play Quiz to Improve Score",
            font=("Arial", 12, "bold"),
            bg=self.main_color,
            fg="white",
            width=25,
            command=self.show_quiz_selection
        )
        play_btn.pack(pady=5)

        # Leaderboard button
        leaderboard_btn = tk.Button(
            buttons_frame,
            text="View Leaderboard",
            font=("Arial", 12),
            bg=self.secondary_color,
            fg=self.text_color,
            width=25,
            command=self.show_leaderboard_selection
        )
        leaderboard_btn.pack(pady=5)

    def show_victory_diploma(self, parent_frame, user_score, user_rank):
        """Display victory diploma for the best player"""
        # Decorative frame for diploma
        diploma_frame = tk.Frame(
            parent_frame,
            bg="gold",
            highlightbackground="orange",
            highlightthickness=5,
            relief="ridge"
        )
        diploma_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Inner frame
        inner_frame = tk.Frame(diploma_frame, bg="ivory")
        inner_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Diploma title
        tk.Label(
            inner_frame,
            text="OFFICIAL DIPLOMA",
            font=("Times New Roman", 36, "bold"),
            bg="ivory",
            fg="darkred"
        ).pack(pady=20)

        # Decorative line
        tk.Frame(inner_frame, bg="gold", height=3).pack(fill="x", padx=50, pady=10)

        # Awarded to text
        tk.Label(
            inner_frame,
            text="Awarded to",
            font=("Times New Roman", 20),
            bg="ivory",
            fg="black"
        ).pack(pady=10)

        # Username (in fancy font)
        tk.Label(
            inner_frame,
            text=self.current_user,
            font=("Brush Script MT", 48),
            bg="ivory",
            fg="purple"
        ).pack(pady=20)

        # Achievement text
        tk.Label(
            inner_frame,
            text="For achieving the highest total score in",
            font=("Times New Roman", 18),
            bg="ivory",
            fg="black"
        ).pack(pady=10)

        tk.Label(
            inner_frame,
            text="Game Master Quiz",
            font=("Times New Roman", 22, "bold"),
            bg="ivory",
            fg="darkblue"
        ).pack(pady=10)

        # Score info
        tk.Label(
            inner_frame,
            text=f"Total Score: {user_score:,} points",
            font=("Arial", 16, "bold"),
            bg="ivory",
            fg="darkgreen"
        ).pack(pady=15)

        tk.Label(
            inner_frame,
            text=f"Global Rank: #{user_rank}",
            font=("Arial", 14),
            bg="ivory",
            fg="darkblue"
        ).pack(pady=5)

        # Decorative element
        tk.Label(
            inner_frame,
            text="🏆 CHAMPION 🏆",
            font=("Arial", 24, "bold"),
            bg="ivory",
            fg="orange"
        ).pack(pady=30)

        # Date
        from datetime import datetime
        current_date = datetime.now().strftime("%B %d, %Y")
        tk.Label(
            inner_frame,
            text=f"Awarded on {current_date}",
            font=("Times New Roman", 14, "italic"),
            bg="ivory",
            fg="gray"
        ).pack(pady=10)

        # Congratulatory message
        tk.Label(
            inner_frame,
            text="Congratulations! You are the ultimate gaming quiz master!",
            font=("Arial", 12),
            bg="ivory",
            fg="darkgreen",
            wraplength=500
        ).pack(pady=20)

    def show_encouragement_message(self, parent_frame, best_username, best_score,
                                 user_score, user_rank, score_difference):
        """Display encouragement message for non-best players"""
        # Current stats frame
        stats_frame = tk.Frame(parent_frame, bg=self.bg_color, relief="groove", bd=2)
        stats_frame.pack(pady=20, padx=20, fill="x")

        tk.Label(
            stats_frame,
            text="Your Current Stats",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        ).pack(pady=10)

        # User stats
        stats_text = f"Total Score: {user_score:,} points\n"
        stats_text += f"Global Rank: #{user_rank}\n"
        if best_username:
            stats_text += f"Best Player: {best_username} ({best_score:,} points)"

        tk.Label(
            stats_frame,
            text=stats_text,
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color,
            justify="center"
        ).pack(pady=15, padx=20)

        # Encouragement frame
        encouragement_frame = tk.Frame(parent_frame, bg="#e6f7ff", relief="raised", bd=3)
        encouragement_frame.pack(pady=30, padx=20, fill="both", expand=True)

        # Crown icon for best player
        tk.Label(
            encouragement_frame,
            text="👑",
            font=("Arial", 48),
            bg="#e6f7ff",
            fg="gold"
        ).pack(pady=10)

        # Message
        message = "Keep Playing to Earn the Champion Diploma!\n\n"

        if score_difference > 0:
            message += f"You need {score_difference:,} more points\n"
            message += f"to beat {best_username} and become the champion!\n\n"

        message += "Every quiz you play brings you closer to victory.\n"
        message += "Test your gaming knowledge and claim the throne!"

        tk.Label(
            encouragement_frame,
            text=message,
            font=("Arial", 14),
            bg="#e6f7ff",
            fg="darkblue",
            justify="center",
            wraplength=500
        ).pack(pady=20, padx=30)

        # Motivational quote
        quotes = [
            "The master has failed more times than the beginner has even tried.",
            "Every expert was once a beginner.",
            "Champions keep playing until they get it right.",
            "The only way to become better is to keep playing!",
            "Greatness comes from consistent effort."
        ]

        import random
        quote = random.choice(quotes)

        tk.Label(
            encouragement_frame,
            text=f'"{quote}"',
            font=("Arial", 12, "italic"),
            bg="#e6f7ff",
            fg="darkgreen",
            wraplength=450
        ).pack(pady=20)

    # Add these methods to the GameMasterApp class after all the other methods

    def export_data(self):
        """Export data for backup"""
        export_window = tk.Toplevel(self.root)
        export_window.title("Export Data")
        export_window.geometry("400x200")
        export_window.configure(bg=self.bg_color)
        export_window.transient(self.root)
        export_window.grab_set()

        tk.Label(
            export_window,
            text="Export Data",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg="#800080"
        ).pack(pady=20)

        tk.Label(
            export_window,
            text="Backup Name (optional):",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=5)

        backup_name_entry = tk.Entry(export_window, font=("Arial", 11), width=30)
        backup_name_entry.pack(pady=5)

        def perform_export():
            backup_name = backup_name_entry.get().strip()
            if not backup_name:
                backup_name = None

            # Create backup
            success, message = self.admin_manager.backup_data(backup_name)

            if success:
                messagebox.showinfo("Export Successful", message)
            else:
                messagebox.showerror("Export Failed", message)

            export_window.destroy()

        button_frame = tk.Frame(export_window, bg=self.bg_color)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Export",
            font=("Arial", 10, "bold"),
            bg="#800080",
            fg="white",
            command=perform_export
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=export_window.destroy
        ).pack(side="left", padx=10)

    def cleanup_data(self):
        """Clean up orphaned data"""
        response = messagebox.askyesno(
            "Cleanup Data",
            "This will remove all score entries for users that no longer exist.\n\n"
            "This operation helps keep the database clean.\n"
            "Continue?"
        )

        if response:
            success, message = self.admin_manager.cleanup_orphaned_scores()

            if success:
                messagebox.showinfo("Cleanup Complete", message)
            else:
                messagebox.showerror("Cleanup Failed", message)

    def show_backup_restore(self):
        """Show backup/restore interface"""
        self.clear_window()

        # Title
        title_label = tk.Label(
            self.root,
            text="💾 Backup & Restore",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#800080"
        )
        title_label.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back to Admin Panel",
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            command=self.show_admin_panel
        )
        back_btn.place(x=10, y=10)

        # Instructions
        tk.Label(
            self.root,
            text="Manage system backups and data recovery",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=600
        ).pack(pady=10)

        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=40)

        backup_btn = tk.Button(
            buttons_frame,
            text="Create Backup",
            font=("Arial", 14),
            bg="#800080",
            fg="white",
            width=25,
            height=2,
            command=self.export_data
        )
        backup_btn.pack(pady=15)

        cleanup_btn = tk.Button(
            buttons_frame,
            text="Cleanup Orphaned Data",
            font=("Arial", 14),
            bg="#9370DB",
            fg="white",
            width=25,
            height=2,
            command=self.cleanup_data
        )
        cleanup_btn.pack(pady=15)