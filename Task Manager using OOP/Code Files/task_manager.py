"""
This is a module docstring. A module docstring is used to provide a
clear and concise description of the module's purpose, functionality,
and usage.

● Use the following username and password to access the admin rights 

    username: admin
    password: password

● Ensure you open the whole folder for this task in VS Code otherwise
the program will look in your root directory for the text files.

NOTE: After refactoring this module, refactor this docstring to properly
      reflect the purpose of this module.

NOTE: After refactoring this module, refactor all comments to properly
      reflect the purpose of the code they describe.

"""

#=====importing libraries===========
import os
from datetime import datetime, date

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
    current_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    current_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    current_task['completed'] = task_components[5] == "Yes"

    task_list.append(current_task)


#====Login Section====
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

#====Main Menu Section====
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
                 "e - Exit\n"
                 ": ").lower()

    # Add a new user to the user.txt file
    if menu == 'r':
        # Request details of new user
        new_username = input("New Username: ")
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w", encoding="utf-8") as out_file:
                user_data = []
                for username, password in username_password.items():
                    user_data.append(f"{username};{password}")
                out_file.write("\n".join(user_data))

        # Otherwise you present a relevant message.
        else:
            print("Passwords do no match")

    # Allow a user to add a new task to task.txt file
    # Prompt a user for the following:
    # - A username of the person whom the task is assigned to,
    # - A title of a task,
    # - A description of the task and
    # - the due date of the task.
    elif menu == 'a':
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password:
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")

        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
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
        with open("tasks.txt", "w", encoding="utf-8") as task_file:
            task_list_to_write = []
            for task in task_list:
                str_attrs = [
                    task['username'],
                    task['title'],
                    task['description'],
                    task['due_date'].strftime(DATETIME_STRING_FORMAT),
                    task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if task['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

    # Reads the task from task.txt file and prints to the console in the
    # format of Output 2 presented in the task pdf (i.e. includes spacing
    # and labelling)
    elif menu == 'va':
        for task in task_list:
            display = (
                f"Task: \t\t {task['title']}\n"
                f"Assigned to: \t {task['username']}\n"
                f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                f"Task Description: \n {task['description']}\n"
            )
            print(display)

    # Reads the task from task.txt file and prints to the console in the
    # format of Output 2 presented in the task pdf (i.e. includes spacing
    # and labelling)
    elif menu == 'vm':
        for task in task_list:
            if task['username'] == current_user:
                display = (
                    f"Task: \t\t {task['title']}\n"
                    f"Assigned to: \t {task['username']}\n"
                    f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    f"Task Description: \n {task['description']}\n"
                )
                print(display)

    # If the user is an admin they can display statistics about number of users
    # and tasks.
    elif menu == 'ds' and current_user == 'admin':
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

    elif menu == 'e':
        print('Goodbye!!!')
        break

    else:
        print("You have made a wrong choice, Please Try again")
