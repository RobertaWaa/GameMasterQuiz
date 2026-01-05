# GameMaster Quiz 🎮

A Python-based gaming quiz platform for video game enthusiasts.

## Features

- **User Authentication**: Secure login/registration with password hashing using SHA-256 with salt
- **Quiz Categories**: HISTORY, CHARACTERS, and MECHANICS gaming quizzes (5 questions each)
- **Custom Quizzes**: Create and play your own gaming quizzes
- **Dual Leaderboards**: Recent high scores and total score ranking system
- **Progress Tracking**: Save scores, game history, and global ranking
- **Modern GUI**: Beautiful pink-themed Tkinter interface
- **Local Data Storage**: All data saved in JSON files (no database required)

## Installation & Setup

### Requirements
- Python 3.6 or higher
- No additional packages required (uses standard library only)

### Running the Application
```bash
# Clone or download the project
# Navigate to GameMasterQuiz directory
python main.py
```
### First-time setup
The application automatically creates:
- Necessary directories (data/, data/quizzes/, data/quizzes/custom/)
- Default quiz files with gaming questions
- JSON files for user data and scores

## Project Architecture

##### GameMasterQuiz/
##### ├── main.py                 # Application entry point and main controller
##### ├── auth.py                 # User authentication with password hashing
##### ├── quiz_logic.py           # Core quiz logic, scoring, and leaderboards
##### ├── quiz_manager.py         # Quiz file management and custom quiz creation
##### ├── interface.py            # Tkinter GUI implementation with pink theme
##### ├── data/                   # Persistent data storage
##### │ ####  ├── users.json          # Encrypted user credentials and basic stats
##### │ ####  ├── scores.json         # Leaderboards and comprehensive user statistics
##### │ ####  └── quizzes/            # Quiz question repositories
##### │ ########      ├── history.json    # Gaming history questions
##### │ ########      ├── characters.json # Game character questions
##### │ ########      ├── mechanics.json  # Game mechanics questions
##### │ ########      └── custom/         # User-generated custom quizzes
##### └── README.md               # Project documentation

## Security Implementation

### Password Security
- SHA-256 Hashing: All passwords are hashed with salt before storage
- Salt Protection: Unique salt value prevents rainbow table attacks
- No Plain Text: Passwords are never stored in readable format

### Data Protection
- Input Validation: All user inputs are sanitized and validated
- File Integrity: JSON files include error handling and corruption checks
- Session Management: User sessions are properly handled and cleared on logout

## User Guide

### 1. Account Management
- Registration: Create a new account with username and password
- Login: Secure authentication to access your profile
- Statistics: View your games played, total score, and global rank

### 2. Playing Quizzes
- Default Categories: Choose from HISTORY, CHARACTERS, or MECHANICS
- Scoring System: 10 points per correct answer
- Progress Tracking: Real-time score display and question progress

### 3. Custom Quizzes
- Creation Tool: Intuitive interface to build custom quizzes
- Question Builder: Add multiple questions with 4 options each
- Answer Validation: Designate correct answers for each question
- Community Sharing: All users can play custom quizzes created by others

### 4. Leaderboards
- Recent Scores: Top individual quiz performances
- Total Ranking: Overall leaderboard based on cumulative scores
- Personal Stats: Your position in the global ranking system

## Technical Details

### Default Quiz Content
Each default category contains 5 challenging questions:
- HISTORY: Gaming milestones, consoles, and industry evolution
- CHARACTERS: Iconic video game characters and their origins
- MECHANICS: Game terminology, strategies, and design concepts

### Data Persistence
- JSON Storage: Lightweight file-based storage system
- Automatic Backup: Data preserved between sessions
- Error Recovery: Graceful handling of file corruption or missing data

### User Interface
- Theme: Pink color scheme (#ff69b4 primary, #fff0f5 background)
- Responsive Design: Adapts to different screen sizes
- Intuitive Navigation: Clear menu structure and back buttons

## Development Notes

### Design Principles
- Modular Architecture: Separated concerns for easy maintenance
- Error Handling: Comprehensive exception handling throughout
- Code Readability: Clear structure with comments and documentation

### Performance
- Lightweight: No external dependencies
- Fast Loading: Instant quiz loading and response times
- Memory Efficient: Minimal resource consumption

## Future Enhancements Roadmap

### Short-term (Next Version)
- Timer functionality for time-limited quizzes
- Difficulty levels (Easy, Medium, Hard)
- Achievement badges and rewards system

### Medium-term
- Multiplayer mode for head-to-head competition
- Quiz sharing via export/import files
- Additional quiz categories (eSports, Indie Games, Retro Gaming)

### Long-term Vision
- Online database for community quiz sharing
- Mobile application version
- Tournament mode with brackets and prizes

## Troubleshooting

### Common Issues
1. "Failed to load quiz" error: Delete and recreate data/quizzes/ directory
2. Login issues: Check data/users.json file integrity
3. GUI freezing: Ensure you have latest Python and Tkinter updates

### Data Recovery
- User data is stored in data/users.json
- Scores are in data/scores.json
- Quizzes are in data/quizzes/ directory
- Backup these files to preserve progress

## License & Credits

### License
This project is developed for educational purposes as part of a personal academic project.

### Technologies Used
- Python 3.x: Core programming language
- Tkinter: GUI framework
- JSON: Data serialization format
- Standard Library: No external dependencies

### Author
Developed as a personal project for academic purposes, demonstrating practical application of programming concepts including authentication systems, file handling, GUI development, and game logic implementation.