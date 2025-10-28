# Import necessary classes and modules
from habit import Habit
from habit_manager import HabitManager
from storage import StorageHandler
import analytics

# Function to display the menu to the user
def menu():
    """
    Presents the user with a list of available actions for the habit tracker.
    """
    print("\nHabit Tracker")
    print("1. Add Habit")                          # Option to add a new habit
    print("2. Delete Habit")                       # Option to delete an existing habit
    print("3. Complete Habit")                     # Option to mark a habit as completed
    print("4. View All Habits")                    # Show all current habits
    print("5. Filter Habits")                      # Show habits filtered by periodicity
    print("6. Longest Streak")                     # Show the longest streak across all habits
    print("7. Longest Streak for a Habit")         # Show the streak of a specific habit
    print("8. Save & Exit")                        # Save habits and exit the app

# Main function that runs the habit tracker loop
def run():
    """
    The main loop of the application. It initializes the HabitManager and
    StorageHandler, loads existing habits, and presents the menu to the user.
    """
    manager = HabitManager()                       # Create a new HabitManager instance
    storage = StorageHandler()                     # Create a new StorageHandler instance
    manager.habits = storage.load()                # Load saved habits from the database

    # If no habits were loaded from the database, add the predefined ones.
    if not manager.habits:
        print("No habits found. Adding predefined habits...")
        manager.add_habit("Read Book", "daily")
        manager.add_habit("Exercise", "daily")
        manager.add_habit("Drink Water", "daily")
        manager.add_habit("Meditate", "weekly")
        manager.add_habit("Call Family", "weekly")

    # Infinite loop to keep the menu running until the user chooses to exit
    while True:
        menu()                                     # Display menu options
        choice = input("Choose an option: ")       # Get user choice

        if choice == "1":
            # Add a new habit
            name = input("Habit name: ")
            period = input("Periodicity (daily/weekly): ")
            manager.add_habit(name, period)
            print(f"Habit '{name}' added.")

        elif choice == "2":
            # Delete an existing habit
            name = input("Habit to delete: ")
            manager.delete_habit(name)
            print(f"Habit '{name}' deleted.")

        elif choice == "3":
            # Mark a habit as completed
            name = input("Habit to complete: ")
            if manager.complete_habit(name):
                print("Completed.")                # Confirm completion
            else:
                print("Habit not found.")          # Show error if habit doesn't exist

        elif choice == "4":
            # View all current habits with their streaks
            print("\n--- Your Habits ---")
            for habit in manager.habits:
                print(f"{habit.name} ({habit.periodicity}) - Streak: {habit.get_streak()}")

        elif choice == "5":
            # Filter habits by periodicity (daily/weekly)
            period = input("Filter by (daily/weekly): ")
            filtered = analytics.filter_by_periodicity(manager.habits, period)
            print(f"\n--- {period.capitalize()} Habits ---")
            print(filtered)

        elif choice == "6":
            # Show the longest streak among all habits
            longest_streak = analytics.get_longest_streak_all(manager.habits)
            print("Longest streak overall:", longest_streak)

        elif choice == "7":
            # Show the longest streak for a specific habit
            name = input("Enter habit name: ")
            streak = analytics.get_longest_streak_for(manager.habits, name)
            print("Streak for", name, ":", streak)

        elif choice == "8":
            # Save all habits to the database and exit the program
            storage.save(manager.habits)
            print("Data saved. Exiting...")
            break

        else:
            print("Invalid option.")               # Handle invalid input

# Run the main function when the script is executed directly
if __name__ == "__main__":
    run()
