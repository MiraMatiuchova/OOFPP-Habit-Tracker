import pytest
import os
import sqlite3
from datetime import datetime, timedelta

# Import all classes and functions from your project files
from habit import Habit
from habit_manager import HabitManager
from storage import StorageHandler
import analytics
import main  # Import the main module to test the CLI


# --- Habit Class Tests ---
# This section tests the fundamental logic of a single habit object.
def test_habit_creation():
    """Verify a habit is created with the correct properties."""
    habit = Habit("Read Book", "daily")
    assert habit.name == "Read Book"
    assert habit.periodicity == "daily"
    assert not habit.completions


def test_habit_completion():
    """Ensure a habit can be marked as completed."""
    habit = Habit("Read Book", "daily")
    habit.complete()
    assert len(habit.completions) == 1


def test_daily_streak_calculation():
    """Verify that the daily streak is calculated correctly."""
    # Create a habit with consecutive completions
    habit = Habit("Exercise", "daily")
    now = datetime.now()
    habit.completions = [
        (now - timedelta(days=2)).isoformat(),
        (now - timedelta(days=1)).isoformat(),
        now.isoformat()
    ]
    assert habit.get_streak() == 3


def test_weekly_streak_calculation():
    """Verify that the weekly streak is calculated correctly."""
    # Create a habit with consecutive weekly completions
    habit = Habit("Meditate", "weekly")
    now = datetime.now()
    habit.completions = [
        (now - timedelta(weeks=2)).isoformat(),
        (now - timedelta(weeks=1)).isoformat(),
        now.isoformat()
    ]
    assert habit.get_streak() == 3


# --- HabitManager Class Tests ---
# This section tests the logic for managing a collection of habits.
def test_add_habit():
    """Ensure a new habit can be added to the manager."""
    manager = HabitManager()
    manager.add_habit("Write Code", "daily")
    assert len(manager.habits) == 1
    assert manager.habits[0].name == "Write Code"


def test_delete_habit():
    """Ensure an existing habit can be deleted."""
    manager = HabitManager()
    manager.add_habit("Write Code", "daily")
    manager.delete_habit("Write Code")
    assert len(manager.habits) == 0


# --- Analytics Module Tests ---
# This section tests the functions for filtering and analyzing habits.
def test_get_all_habits():
    """Verify the function returns all habit names."""
    manager = HabitManager()
    manager.add_habit("Habit A", "daily")
    manager.add_habit("Habit B", "weekly")
    all_habits = analytics.get_all_habits(manager.habits)
    assert all_habits == ["Habit A", "Habit B"]


def test_filter_by_periodicity():
    """Verify the function can correctly filter habits by their periodicity."""
    manager = HabitManager()
    manager.add_habit("Daily Habit", "daily")
    manager.add_habit("Weekly Habit", "weekly")
    daily_habits = analytics.filter_by_periodicity(manager.habits, "daily")
    assert daily_habits == ["Daily Habit"]


def test_get_longest_streak_overall():
    """Verify the function finds the longest streak among all habits."""
    habit1 = Habit("Daily", "daily")
    habit1.completions = [datetime.now().isoformat(), (datetime.now() - timedelta(days=1)).isoformat()]
    habit2 = Habit("Weekly", "weekly")
    habit2.completions = [datetime.now().isoformat()]

    longest = analytics.get_longest_streak_all([habit1, habit2])
    assert longest == 2


# --- StorageHandler (Database) Tests ---
# This section tests the save and load functionality with a temporary database.

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to create a temporary database file for each test,
    ensuring tests are isolated and don't affect each other.
    """
    db_file = "test_habits.db"
    if os.path.exists(db_file):
        os.remove(db_file)
    yield db_file
    if os.path.exists(db_file):
        os.remove(db_file)


def test_save_and_load_habits(db_session):
    """
    Test saving a list of habits and then loading them back,
    verifying that the data is preserved correctly.
    """
    # Create and save two habits to the temporary database
    storage_handler = StorageHandler(db_name=db_session)
    habits_to_save = [
        Habit("Test Habit 1", "daily"),
        Habit("Test Habit 2", "weekly")
    ]
    habits_to_save[0].complete()
    storage_handler.save(habits_to_save)

    # Load the habits back from the database
    loaded_habits = storage_handler.load()
    assert len(loaded_habits) == 2

    # Verify that the loaded data matches the original data
    loaded_habit_1 = loaded_habits[0]
    assert loaded_habit_1.name == "Test Habit 1"
    assert loaded_habit_1.periodicity == "daily"
    assert len(loaded_habit_1.completions) == 1


def test_update_existing_habit(db_session):
    """
    Test that the save method correctly updates an existing habit
    instead of creating a duplicate.
    """
    # Save a habit initially
    storage_handler = StorageHandler(db_name=db_session)
    habit = Habit("Update Me", "daily")
    storage_handler.save([habit])

    # Complete the habit and save again
    habit.complete()
    storage_handler.save([habit])

    # Load the habits and verify the completion was added to the existing record
    loaded_habits = storage_handler.load()
    assert len(loaded_habits) == 1
    assert len(loaded_habits[0].completions) == 1


# --- Command-Line Interface (CLI) Test ---
# This section tests the main loop by simulating user input and capturing output.
def test_cli_add_and_view_habit(monkeypatch, capsys, db_session):
    """
    Simulate a user adding a habit and then viewing it, checking for correct output.
    This test uses a mock database to ensure it's isolated.
    """
    # Create a clean database for this test
    storage_handler = StorageHandler(db_name=db_session)
    storage_handler.conn.close()

    # Simulate user input for adding a habit and viewing all habits, then exiting
    inputs = iter(['1', 'Run every day', 'daily', '4', '8'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Redirect the main loop's storage to use our test database
    main.StorageHandler = lambda: StorageHandler(db_name=db_session)

    # Run the main application
    main.run()

    # Capture the output printed to the console
    captured = capsys.readouterr()

    # Verify that the expected output is present
    assert "Habit 'Run every day' added." in captured.out
    assert "Run every day (daily) - Streak: 0" in captured.out
    assert "Data saved. Exiting..." in captured.out
