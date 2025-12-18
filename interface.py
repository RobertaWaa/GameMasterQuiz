"""
Graphical user interface for GameMaster Quiz
Built with tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from auth import UserAuth
from quiz_logic import QuizGame
from quiz_manager import QuizManager

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
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_scrollable_frame(self, parent):
        """Create a scrollable frame and return container, canvas, scrollable_frame"""
        # Create main container
        container = tk.Frame(parent, bg=self.bg_color)
        container.pack(fill="both", expand=True)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mouse wheel for Windows and Mac
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        return container, canvas, scrollable_frame
    
    def show_login_screen(self):
        """Display login/registration screen"""
        self.clear_window()
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎮 GameMaster Quiz 🎮", 
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
    
       # Create scrollable container
       container, canvas, scrollable_frame = self.create_scrollable_frame(self.root)
    
       # Create a frame to center content inside scrollable_frame
       center_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
       center_frame.pack(expand=True, fill="both")
    
       # Quiz categories frame - centered
       categories_frame = tk.Frame(center_frame, bg=self.bg_color)
       categories_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
       # Default categories
       categories = [
           ("HISTORY", "Test your knowledge of gaming history"),
           ("CHARACTERS", "How well do you know gaming characters?"),
           ("MECHANICS", "Test your knowledge of game mechanics")
       ]
    
       for i, (category, description) in enumerate(categories):
           # Create a container frame for each category to control width
           category_container = tk.Frame(categories_frame, bg=self.bg_color)
           category_container.pack(pady=15, padx=20, fill="x")
        
           # Center the category frame inside the container
           category_frame = tk.Frame(category_container, bg=self.bg_color, 
                                    highlightbackground=self.main_color, 
                                    highlightthickness=2)
           category_frame.pack()  # Default is center
        
           tk.Label(
               category_frame,
               text=category,
               font=("Arial", 16, "bold"),
               bg=self.bg_color,
               fg=self.main_color
           ).pack(pady=5)
        
           tk.Label(
               category_frame,
               text=description,
               font=("Arial", 12),
               bg=self.bg_color,
               fg=self.text_color,
               wraplength=400
           ).pack(pady=5)
        
           tk.Button(
               category_frame,
               text="Play",
               font=("Arial", 12),
               bg=self.main_color,
               fg="white",
               width=15,
               command=lambda cat=category: self.start_quiz(cat)
           ).pack(pady=10)
    
       # Custom quizzes section
       custom_quizzes = self.quiz_manager.get_available_quizzes()
       custom_quizzes = [q for q in custom_quizzes if q[2]]  # Only custom quizzes
    
       if custom_quizzes:
           tk.Label(
               center_frame,
               text="Custom Quizzes",
               font=("Arial", 18, "bold"),
               bg=self.bg_color,
               fg=self.main_color
           ).pack(pady=20)
        
           custom_frame = tk.Frame(center_frame, bg=self.bg_color)
           custom_frame.pack(pady=10)
        
           for quiz_name, _, _ in custom_quizzes:
               display_name = quiz_name.replace("_", " ").title()
               # Remove username prefix for display
               if "_" in display_name and display_name.startswith(self.current_user.title()):
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
       else:
           # Show message if no custom quizzes
           tk.Label(
               center_frame,
               text="No custom quizzes yet. Create your own!",
               font=("Arial", 12, "italic"),
               bg=self.bg_color,
               fg=self.text_color
           ).pack(pady=20)
    
       # Update canvas scroll region
       canvas.update_idletasks()
       canvas.config(scrollregion=canvas.bbox("all"))
    
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
        
        # Create scrollable container
        container, canvas, scrollable_frame = self.create_scrollable_frame(self.root)
        
        # Get current question
        question_data = self.quiz_game.get_current_question()
        
        if not question_data:
            self.show_quiz_results()
            return
        
        # Progress
        current, total = self.quiz_game.get_progress()
        progress_label = tk.Label(
            scrollable_frame,
            text=f"Question {current + 1} of {total}",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        progress_label.pack(pady=10)
        
        # Score
        score_label = tk.Label(
            scrollable_frame,
            text=f"Score: {self.quiz_game.score}",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        score_label.pack(pady=5)
        
        # Question
        question_label = tk.Label(
            scrollable_frame,
            text=question_data["question"],
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=600,
            justify="center"
        )
        question_label.pack(pady=30, padx=20)
        
        # Options frame
        options_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
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
            scrollable_frame,
            text="Quit Quiz",
            font=("Arial", 10),
            bg="#ffcccc",
            fg="red",
            command=self.show_main_menu
        )
        quit_btn.pack(pady=20)
        
        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
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
        
        # Create scrollable container
        container, canvas, scrollable_frame = self.create_scrollable_frame(self.root)
        
        # Title
        title_label = tk.Label(
            scrollable_frame, 
            text="Quiz Complete! 🎉", 
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.main_color
        )
        title_label.pack(pady=30)
        
        # Score
        score_label = tk.Label(
            scrollable_frame,
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
            scrollable_frame,
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
            scrollable_frame,
            text=message,
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=500
        )
        message_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
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
        
        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
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
        
        # Create scrollable container
        container, canvas, scrollable_frame = self.create_scrollable_frame(self.root)
        
        # Get leaderboard data based on type
        if lb_type == "recent":
            leaderboard = self.quiz_game.get_leaderboard(limit=50)  # Increased limit
            headers = ["Rank", "Username", "Score", "Quiz", "Date"]
        else:
            leaderboard = self.quiz_game.get_user_stats_leaderboard(limit=50)  # Increased limit
            headers = ["Rank", "Username", "Total Score", "Games Played", "Avg. Score"]
        
        if not leaderboard:
            no_data_label = tk.Label(
                scrollable_frame,
                text="No scores yet. Be the first to play!",
                font=("Arial", 16),
                bg=self.bg_color,
                fg=self.text_color
            )
            no_data_label.pack(pady=100)
            return
        
        # Create table frame
        table_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
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
                        scrollable_frame,
                        text=f"Your rank: #{user_rank} | Total Score: {user_stats.get('total_score', 0)} | Games: {user_stats.get('total_games', 0)}",
                        font=("Arial", 11, "bold"),
                        bg="#ffd9ec",
                        fg=self.main_color,
                        pady=10
                    )
                    user_info.pack(pady=10, fill="x")
        
        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
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
        
        # Create scrollable container
        container, canvas, scrollable_frame = self.create_scrollable_frame(self.root)
        
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
        
        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
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