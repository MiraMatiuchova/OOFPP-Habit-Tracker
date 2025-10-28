from habit import Habit

class HabitManager:
    def __init__(self):
        """
        Initializes a new HabitManager with an empty list of habits.
        """
        self.habits = []  # List to store Habit objects

    def add_habit(self, name, periodicity):
        """
        Adds a new habit to the manager.

        Args:
            name (str): Name of the habit (e.g., 'Read Book').
            periodicity (str): Frequency of the habit, either 'daily' or 'weekly'.
        """
        self.habits.append(Habit(name, periodicity))

    def delete_habit(self, name):
        """
        Deletes a habit by name.

        Args:
            name (str): Name of the habit to delete.
        """
        # Create a new list with all habits except the one to delete
        self.habits = [h for h in self.habits if h.name != name]

    def complete_habit(self, name):
        """
        Marks the specified habit as completed (adds a timestamp).

        Args:
            name (str): Name of the habit to complete.

        Returns:
            bool: True if the habit was found and completed, False otherwise.
        """
        for habit in self.habits:
            if habit.name == name:
                habit.complete()
                return True  # Habit found and completed
        return False  # Habit not found

    def get_habit(self, name):
        """
        Retrieves a habit by name.

        Args:
            name (str): Name of the habit to retrieve.

        Returns:
            Habit or None: The matching Habit object, or None if not found.
        """
        for habit in self.habits:
            if habit.name == name:
                return habit
        return None  # Habit not found
