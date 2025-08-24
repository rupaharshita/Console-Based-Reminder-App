# personal to-do (reminder) 
import os
from datetime import datetime
from win11toast import toast

class Reminder:
    # to initialize reminder object
    def __init__(self, title, start_time, end_time, priority):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority
        self.task_completed = False

    # string representation of reminder (special methods in python)
    def __str__(self):
        task_status = "Done" if self.task_completed else "Not Done"
        return f"""
        Task -> {self.title}
        From Date -> {self.start_time} 
        To Date -> {self.end_time} 
        Priority -> {self.priority} 
        Task Status -> {task_status}"""

    # converts the object into a dictionary making it easier to store in a file
    def to_dict(self):
        return {
            "title": self.title,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M"),
            "priority": self.priority,
            "task_completed": self.task_completed,
        }
    # static method decorator
    @staticmethod
    # takes the dictionary from of data from file and converts it into reminder object
    def from_dict(data):
        start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M")
        return Reminder(data["title"], start_time, end_time, data["priority"])


# a class to handle reminders
class ReminderManager:
    FILE_PATH = "reminders.txt"

    # to load all reminders from file
    def __init__(self):
        self.reminders = self.load_reminders()

    # method to add reminder
    def add_reminder(self, title, start_time, end_time, priority):
        new_reminder = Reminder(title, start_time, end_time, priority)
        # does your reminder coincide with other?
        conflicts = self.check_conflicts(new_reminder)
        if conflicts:
            print("You have this Reminder conflicting other reminders below: ")
            for counter, conflict in enumerate(conflicts, start=1):
                print(f" {counter} - {conflict}")
            confirm = input("Do you still want to add this reminder? (yes/no): ")
            if confirm.lower() != "yes":
                return 
        # upon user's decision we add the reminder
        self.reminders.append(new_reminder)
        self.save_reminders()
        # print("Reminder added successfully.")
        return str(new_reminder)

    # a method to check if the date, time and title of existing reminders coincide with the new reminder
    def check_conflicts(self, new_reminder):
        conflicts = []
        for reminder in self.reminders:
            if (
                new_reminder.start_time <= reminder.end_time
                and new_reminder.end_time >= reminder.start_time
            ):
                conflicts.append(reminder)
            if (
                new_reminder.start_time == reminder.start_time
                or new_reminder.end_time == reminder.end_time
            ):
                conflicts.append(reminder)
            if new_reminder.title == reminder.title:
                conflicts.append(reminder)
        return conflicts

    # method to display reminders
    def display_reminders(self):
     if not self.reminders:
        print("No existing reminders.")
     else:
        print("All reminders:")
        for i, reminder in enumerate(self.reminders):
            print(f"{i + 1} -> {reminder}")
    # to delete a reminder
    def delete_reminder(self, index):
        if 0 <= index < len(self.reminders):
            removed = str(self.reminders.pop(index))
            self.save_reminders()
            return removed
        else:
            print("Invalid index. Please try again.")
    # to update if a task is done
    def update_reminders(self, index):
        if 0 <= index < len(self.reminders):
            self.reminders[index].task_completed = True
            updated = str(self.reminders[index])
            self.save_reminders()
            return updated
        else:
            print("Invalid index. Please try again.")

    # a method to load reminders from the file
    def load_reminders(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            reminders = []
            for line in file:
                data = eval(line.strip())
                reminders.append(Reminder.from_dict(data))
            return reminders

    # write the reminders into the file
    def save_reminders(self):
        with open(self.FILE_PATH, "w") as file:
            for reminder in self.reminders:
                file.write(str(reminder.to_dict()) + "\n")


# in case our user enters wrong formats of date and time
def get_datetime_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'.")
            print("For Example :  2024-06-12 01:30 ")


# display menu
def display_menu():
    print("\nTo-Do ")
    print("1. Add task")
    print("2. View tasks")
    print("3. Delete task")
    print("4. Mark Task as completed")
    print("5. Save and Exit")

    choice = input("Choose an option: ")
    return choice


# main section
def main():
    manager = ReminderManager()

    while True:
        choice = display_menu()

        if choice == "1":
            print("\n Please Add a new reminder")
            title = input("Enter title: ")
            start_time = get_datetime_input("Enter start time (YYYY-MM-DD HH:MM): ")
            end_time = get_datetime_input("Enter end time (YYYY-MM-DD HH:MM): ")
            priority = int(input("Enter priority (1-5): "))
            ret = manager.add_reminder(title, start_time, end_time, priority)
            if ret: 
                toast(
                    "Task updated successfully",
                    ret,
                    duration="short",
                    button="Dismiss",
                )
        elif choice == "2":
            manager.display_reminders()
        elif choice == "3":
            print("\n Select a reminder to Delete")
            manager.display_reminders()
            index = int(input("Enter the index of the reminder to delete: ")) - 1
            ret = manager.delete_reminder(index)
            toast(
                "Task deleted successfully",
                ret,
                duration="short",
                button="Dismiss",
             )
        elif choice == "4":
            print("\n Select a reminder to update")
            manager.display_reminders()
            index = (
                int(input("Enter the index of the reminder to mark as completed: ")) - 1
            )
            ret = manager.update_reminders(index)
            toast(
                "Task Updated successfully",
                ret,
                duration="short",
                button="Dismiss",
            )
        elif choice == "5":
            print("Saving and exiting...")
            manager.save_reminders()
            toast(
                "Task saved successfully",
                "Good Job",
                button="Dismiss",
            )
            break
        else:
            print("Invalid choice. Please try again.")

# call main 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        toast(
            "TO-DO Closed Successfully",
            duration="short",
            button="Dismiss",
        )
