from datetime import datetime, timedelta

class Habit:
    """
    Represents a single habit with its name, periodicity, creation date, and completions.
    """
    def __init__(self, name, periodicity, created_at=None, completions=None):
        """
        Initializes a new Habit instance.

        Args:
            name (str): The name of the habit.
            periodicity (str): The frequency, either 'daily' or 'weekly'.
            created_at (str, optional): ISO timestamp of creation. Defaults to now.
            completions (list, optional): List of ISO timestamp strings for completions.
        """
        self.name = name
        self.periodicity = periodicity
        # Use current time if created_at is not provided, storing it as an ISO string
        self.created_at = created_at or datetime.now().isoformat()
        # Initialize completions list, defaulting to an empty list
        self.completions = completions or []

    def complete(self):
        """
        Marks the habit as completed at the current time.
        Appends the current timestamp (as an ISO string) to the completions list.
        """
        timestamp = datetime.now().isoformat()
        self.completions.append(timestamp)

    def get_streak(self):
        """
        Calculates the current consecutive completion streak based on the habit's periodicity.

        Returns:
            int: The number of consecutive days or weeks the habit was completed.
        """
        if not self.completions:
            return 0  # A streak of 0 if there are no completions

        # Convert timestamp strings to datetime objects and sort them chronologically
        sorted_dates = sorted(datetime.fromisoformat(ts) for ts in self.completions)
        streak = 1  # The most recent completion always counts as a streak of 1

        # Iterate backwards from the second-to-last completion to find consecutive periods
        for i in range(len(sorted_dates) - 1, 0, -1):
            current_date = sorted_dates[i]
            previous_date = sorted_dates[i - 1]
            delta = current_date - previous_date

            # Check if the time difference is within the period for a daily or weekly habit
            if self.periodicity == 'daily' and delta <= timedelta(days=1.5):
                # A small buffer (0.5 days) is used to account for completions on the same day
                # or for slightly more than 24 hours between completions
                streak += 1
            elif self.periodicity == 'weekly' and delta <= timedelta(days=7.5):
                # A small buffer (0.5 weeks) is used for weekly streaks
                streak += 1
            else:
                break  # If the gap is too large, the streak is broken

        return streak
