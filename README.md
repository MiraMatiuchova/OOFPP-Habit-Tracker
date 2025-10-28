# Habit Tracker App

This is a simple Python command-line habit tracking app. It allows users to:

- Create daily or weekly habits

- Complete habits

- Track streaks

- Analyze performance

- Save/load data using a SQLite database

# Requirements

Python 3.7+

pytest for running tests

# Installation

This command installs the libraries you need, like pytest.

pip install -r requirements.txt

# How to Run

IMPORTANT: Due to the modular structure of the app, you must execute the script from the main project folder to ensure all modules are found correctly.

1. Navigate to the project folder: (replace 'HabitTrackerApp' with the name of your downloaded folder, e.g., student ID folder)

  cd HabitTrackerApp

2. This command starts the application.

  python main.py

# Using the App

Once the app is running, just type the number for the action you want to take and press Enter. The menu options are straightforward, but here's a quick guide:

Add a habit: This is where you start! Give your habit a name and tell the app if it's daily or weekly.

Complete a habit: Use this to log a successful completion. Remember to type the exact name of the habit.

View habits: This shows you a list of all your habits and their current streaks. It's a great way to see your progress.

Analyze streaks: Options 6 and 7 let you check your longest streak overall or for a specific habit.

Save and exit: When you're done, use option 8 to save your data before you close the app.
