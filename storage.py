import sqlite3
import json
from habit import Habit

class StorageHandler:
    """
    Handles all database-related operations for the habit tracker.
    It connects to the SQLite database, creates the necessary tables,
    and provides methods for saving and loading habit data.
    """
    def __init__(self, db_name="habits.db"):
        """
        Initializes the database connection.
        - 'db_name' is the file name for the database.
        - 'self.conn' is the connection object to the database.
        - 'self.cursor' is used to execute SQL commands.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """
        Creates the 'habits' table in the database if it doesn't already exist.
        - 'id' is a unique key for each habit.
        - 'name' is the name of the habit, and it must be unique.
        - 'completions' is stored as a JSON string because SQLite doesn't
          have a native list type.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completions TEXT NOT NULL
            );
        """)
        self.conn.commit()  # Commits the table creation to the database

    def save(self, habits):
        """
        Saves all habits from the HabitManager to the database.
        It checks if a habit already exists by its name. If it does,
        it updates the record. If not, it inserts a new record.
        """
        for habit in habits:
            # Convert the list of completions to a JSON string for storage
            completions_json = json.dumps(habit.completions)

            # Check if the habit already exists in the database
            self.cursor.execute("SELECT id FROM habits WHERE name = ?", (habit.name,))
            existing_habit = self.cursor.fetchone()

            if existing_habit:
                # Update existing habit's completions and creation date
                self.cursor.execute("""
                    UPDATE habits SET completions = ?, created_at = ?
                    WHERE name = ?
                """, (completions_json, habit.created_at, habit.name))
            else:
                # Insert a new habit record into the table
                self.cursor.execute("""
                    INSERT INTO habits (name, periodicity, created_at, completions)
                    VALUES (?, ?, ?, ?)
                """, (habit.name, habit.periodicity, habit.created_at, completions_json))

        self.conn.commit()  # Save the changes to the database

    def load(self):
        """
        Loads all habits from the database and returns them as a list
        of Habit objects.
        """
        self.cursor.execute("SELECT name, periodicity, created_at, completions FROM habits")
        rows = self.cursor.fetchall()  # Fetches all rows from the query
        habits = []
        for row in rows:
            name, periodicity, created_at, completions_json = row
            # Convert the JSON string back into a Python list
            completions = json.loads(completions_json)
            # Create a new Habit object from the loaded data
            habits.append(Habit(name, periodicity, created_at=created_at, completions=completions))
        return habits

    def __del__(self):
        """
        Destructor to ensure the database connection is closed when the
        StorageHandler object is no longer in use. This prevents file locking issues.
        """
        self.conn.close()
