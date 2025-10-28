# analytics.py

# This file contains functions for analyzing habit data, such as
# filtering habits and calculating streaks.

def get_all_habits(habits):
    """
    Retrieves the names of all habits.

    Args:
        habits (list): List of Habit objects.

    Returns:
        list: A list of habit names.
    """
    return [habit.name for habit in habits]

def filter_by_periodicity(habits, periodicity):
    """
    Filters habits by a given periodicity ('daily' or 'weekly').

    Args:
        habits (list): List of Habit objects.
        periodicity (str): The periodicity to filter by.

    Returns:
        list: A list of names of habits matching the given periodicity.
    """
    return [habit.name for habit in habits if habit.periodicity == periodicity]

def get_longest_streak_all(habits):
    """
    Finds the longest streak among all habits.

    Args:
        habits (list): List of Habit objects.

    Returns:
        int: The highest streak value among all habits, or 0 if no habits.
    """
    return max((habit.get_streak() for habit in habits), default=0)

def get_longest_streak_for(habits, habit_name):
    """
    Finds the current streak for a specific habit by name.

    Args:
        habits (list): List of Habit objects.
        habit_name (str): The name of the habit to check.

    Returns:
        int: The streak value of the specified habit, or 0 if not found.
    """
    for habit in habits:
        if habit.name == habit_name:
            return habit.get_streak()
    return 0  # Habit not found
