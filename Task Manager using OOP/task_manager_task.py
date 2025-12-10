# =====importing libraries===========
import os
from datetime import datetime, date
from tabulate import tabulate
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [task for task in task_data if task != ""]

task_list = []
for task in task_data:
    current_task = {}

    # Split by semicolon and manually add each component
    task_components = task.split(";")
    current_task['username'] = task_components[0]
    current_task['title'] = task_components[1]
    current_task['description'] = task_components[2]
    current_task['due_date'] = datetime.strptime(
        task_components[3], DATETIME_STRING_FORMAT)
    current_task['assigned_date'] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT)
    current_task['completed'] = task_components[5] == "Yes"

    task_list.append(current_task)

# ====Login Section====
# This code reads usernames and password from the user.txt file to
# allow a user to login.

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r', encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

while True:
    print("LOGIN")
    current_user = input("Username: ")
    current_pass = input("Password: ")
    if current_user not in username_password:
        print("User does not exist")
        continue
    if username_password[current_user] != current_pass:
        print("Wrong password")
        continue
    print("Login Successful!")
    break


# =====User-Defined functions========
def reg_user():
    '''Add a new user to the user.txt file'''
    # Request details of new user
    # checks to see if the username already exists and displaysd error
    # message until a unique username is created
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("Sorry that username already exists")
        else:
            break

    while True:
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            break
        # Otherwise you present a relevant message.
        else:
            print("Passwords do no match")

    with open("user.txt", "w", encoding="utf-8") as out_file:
        user_data = []
        for username, password in username_password.items():
            user_data.append(f"{username};{password}")
        out_file.write("\n".join(user_data))


def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following:
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and
    - the due date of the task.'''

    while True:
        # loops the user until an exisiting user is entered
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        # loops user to ensure correct date format
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Add the data to the file task.txt and
    # Include 'No' to indicate if the task is complete.
    current_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": current_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w", encoding="utf-8") as tf:
        task_list_to_write = []
        for i in task_list:
            str_attrs = [
                i['username'],
                i['title'],
                i['description'],
                i['due_date'].strftime(DATETIME_STRING_FORMAT),
                i['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if i['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        tf.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)'''
    for i in task_list:
        display = (
            f"Task: \t\t {i['title']}\n"
            f"Assigned to: \t {i['username']}\n"
            f"Date Assigned: \t " +
            f"{i['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Due Date: \t {i['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Task Description: \n {i['description']}\n"
        )
        print(display)


def task_edit(task_index):
    """This function recusivly calls itself to allow the user to make
    multiple adjustments to the user and sue date values in each object.
    The user then has the choice to exit after each change or call the
    function again to change something different"""

    task_to_edit = task_list[task_index]

    print(f"\nEditing task: {task_to_edit['title']}")
    if task_to_edit["completed"]:
        print("This task is already marked as complete and cannot be edited.")
        return

    while True:
        print("\nWhat would you like to edit?")
        print("1 - Change assigned user")
        print("2 - Change due date")
        print("3 - Mark task as complete")
        print("4 - No edits / return to menu")
        choice = input("Enter option number: ")

        if choice == "1":
            while True:
                new_user = input("Enter new username: ")
                if new_user not in username_password:
                    print(
                        "User does not exist. Please enter a valid username.")
                else:
                    task["username"] = new_user
                    print("Username updated successfully.")
                    break

        elif choice == "2":
            while True:
                new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                try:
                    task["due_date"] = datetime.strptime(
                        new_due_date, DATETIME_STRING_FORMAT)
                    print("Due date updated successfully.")
                    break
                except ValueError:
                    print("Invalid date format. Please try again.")

        elif choice == "3":
            if task["completed"]:
                print("Task is already marked complete.")
            else:
                confirm = input("Mark as complete? (yes/no): ").lower()
                if confirm == "yes":
                    task["completed"] = True
                    print("Task marked as complete.")

        elif choice == "4":
            print("No further edits made.")
            break

        else:
            print("Invalid choice. Please try again.")

        # Ask if user wants to make more edits to the same task
        more = input("Would you like to make another edit to this task?\
                     (yes/no): ").lower()
        if more != "yes":
            break

    # Save all changes to file
    with open("tasks.txt", "w", encoding="utf-8") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t["completed"] else "No",
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling), but usees the current user to only display tasks
    assigned to the current user'''
    i = 1
    display = []
    for x in task_list:
        if x['username'] == current_user:
            display.append([i, x['title'], x['username'],
                            x['assigned_date'],
                            x['due_date'], x['description']])
            i += 1
    print(tabulate(display, headers=['Task number', 'Task Title', 'User',
                                     'Date Assigned',
                                     'Date Due', 'Task Description'],
                   tablefmt='github'))

    update_choice = int(input("Enter task number to edit, or -1 to return: "))

    if update_choice == -1:
        return

# Convert to zero-based index
    if 1 <= update_choice <= len(display):
        task_index = update_choice - 1
        # Find the corresponding task in task_list
        user_tasks = [t for t in task_list if t['username'] == current_user]
        task_to_edit = user_tasks[task_index]
        real_index = task_list.index(task_to_edit)
        task_edit(real_index)
    else:
        print("Invalid task number. Please try again.")


def show_stats():
    '''allows the admin to check the statistics'''
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t["completed"])
    uncompleted_tasks = total_tasks - completed_tasks

    today = date.today()
    overdue_tasks = sum(
        1 for t in task_list if not t["completed"] and t["due_date"].date()
        < today
    )

    percent_incomplete = (
        uncompleted_tasks / total_tasks * 100) if total_tasks else 0
    percent_overdue = (overdue_tasks / total_tasks * 100) if total_tasks else 0

    print("===== TASK OVERVIEW =====")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Uncompleted tasks: {uncompleted_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")
    print(f"Percentage incomplete: {percent_incomplete:.2f}%")
    print(f"Percentage overdue: {percent_overdue:.2f}%\n")

    # === USER OVERVIEW ===
    total_users = len(username_password.keys())

    print("===== USER OVERVIEW =====")
    print(f"Total users: {total_users}")
    print(f"Total tasks: {total_tasks}")

    # Avoid division by zero if there are no tasks
    if total_tasks == 0:
        print("No tasks have been created yet.\n")
        return

    for x in username_password.keys():
        user_tasks = [t for t in task_list if t["username"] == x]
        num_user_tasks = len(user_tasks)

    if num_user_tasks == 0:
        percent_of_total = 0
        percent_completed = 0
        percent_incomplete = 0
        percent_overdue_user = 0
    else:
        percent_of_total = (num_user_tasks / total_tasks) * 100
        completed_user_tasks = sum(1 for t in user_tasks if t["completed"])
        incomplete_user_tasks = num_user_tasks - completed_user_tasks
        overdue_user_tasks = sum(
            1
            for t in user_tasks
            if not t["completed"] and t["due_date"].date() < today
        )

        percent_completed = (completed_user_tasks / num_user_tasks) * 100
        percent_incomplete = (incomplete_user_tasks / num_user_tasks) * 100
        percent_overdue_user = (overdue_user_tasks / num_user_tasks) * 100

    print(f"  User: {x}")
    print(f"  Total tasks assigned: {num_user_tasks}")
    print(f"  % of all tasks assigned: {percent_of_total:.2f}%")
    print(f"  % completed: {percent_completed:.2f}%")
    print(f"  % incomplete: {percent_incomplete:.2f}%")
    print(f"  % overdue: {percent_overdue_user:.2f}%")


def generate_reports():
    """Generates task_overview.txt and user_overview.txt reports."""

    # === TASK OVERVIEW ===
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t["completed"])
    uncompleted_tasks = total_tasks - completed_tasks

    today = date.today()
    overdue_tasks = sum(
        1 for t in task_list if not t["completed"] and t["due_date"].date() < today
    )

    percent_incomplete = (
        uncompleted_tasks / total_tasks * 100) if total_tasks else 0
    percent_overdue = (overdue_tasks / total_tasks * 100) if total_tasks else 0

    # Write task_overview.txt
    with open("task_overview.txt", "w", encoding="utf-8") as f:
        f.write("===== TASK OVERVIEW =====\n")
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed tasks: {completed_tasks}\n")
        f.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        f.write(f"Overdue tasks: {overdue_tasks}\n")
        f.write(f"Percentage incomplete: {percent_incomplete:.2f}%\n")
        f.write(f"Percentage overdue: {percent_overdue:.2f}%\n")

    # === USER OVERVIEW ===
    total_users = len(username_password.keys())

    with open("user_overview.txt", "w", encoding="utf-8") as f:
        f.write("===== USER OVERVIEW =====\n")
        f.write(f"Total users: {total_users}\n")
        f.write(f"Total tasks: {total_tasks}\n\n")

        # Avoid division by zero if there are no tasks
        if total_tasks == 0:
            f.write("No tasks have been created yet.\n")
            return

        for x in username_password.keys():
            user_tasks = [t for t in task_list if t["username"] == x]
            num_user_tasks = len(user_tasks)

            if num_user_tasks == 0:
                percent_of_total = 0
                percent_completed = 0
                percent_incomplete = 0
                percent_overdue_user = 0
            else:
                percent_of_total = (num_user_tasks / total_tasks) * 100
                completed_user_tasks = sum(1 for t in user_tasks if t[
                    "completed"])
                incomplete_user_tasks = num_user_tasks - completed_user_tasks
                overdue_user_tasks = sum(
                    1
                    for t in user_tasks
                    if not t["completed"] and t["due_date"].date() < today
                )

                percent_completed = (
                    completed_user_tasks / num_user_tasks) * 100
                percent_incomplete = (
                    incomplete_user_tasks / num_user_tasks) * 100
                percent_overdue_user = (
                    overdue_user_tasks / num_user_tasks) * 100

            f.write(f"  User: {user}\n")
            f.write(f"  Total tasks assigned: {num_user_tasks}\n")
            f.write(f"  % of all tasks assigned: {percent_of_total:.2f}%\n")
            f.write(f"  % completed: {percent_completed:.2f}%\n")
            f.write(f"  % incomplete: {percent_incomplete:.2f}%\n")
            f.write(f"  % overdue: {percent_overdue_user:.2f}%\n\n")

    print("Reports generated: task_overview.txt and user_overview.txt\
          created successfully.")


# ====Main Menu Section====
while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input("Select one of the following Options below:\n"
                 "r - Registering a user\n"
                 "a - Adding a task\n"
                 "va - View all tasks\n"
                 "vm - View my task\n"
                 "ds - Display statistics\n"
                 "gr - Generate reports\n"
                 "e - Exit\n"
                 ": ").lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'ds' and current_user == 'admin':
        show_stats()
    elif menu == 'gr' and current_user == 'admin':
        generate_reports()
    elif menu == 'e':
        print("goodbye!")
        break
    else:
        print("You have made a wrong choice, please try again")
