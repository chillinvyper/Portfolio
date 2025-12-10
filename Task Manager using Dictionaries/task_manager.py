# ===== Importing external modules ===========
'''This is the section where you will import modules'''
import sys
import os.path
from datetime import datetime
from datetime import date
from tabulate import tabulate


class Task:
    """This is a class for the tasks that are being imported to allow for
    specific handeling and self-referencing when doing searches, additions,
    presentation and deletion"""
    def __init__(
            self, user, title, description, date_assign, date_due, completed
            ):
        self.user = user
        self.title = title
        self.description = description
        self.date_assign = date_assign
        self.date_due = date_due
        self.completed = completed

    def task_complete(self):
        """Changes the completed value to 'Yes' to show the task complete"""
        return self.completed == "Yes"

    def get_user(self):
        """Returns the value of user in the object"""
        return self.user

    def get_title(self):
        """Returns the value of title in the object"""
        return self.title

    def get_description(self):
        """Returns the value of description in the object"""
        return self.description

    def get_date_assign(self):
        """Returns the value of date assigned in the object"""
        return self.date_assign

    def get_date_due(self):
        """Returns the value of date due in the object"""
        return self.date_due

    def get_status(self):
        """Returns the value of completed status in the object"""
        return self.completed


def reg_user(users):
    """This function checks whether the entered new username already exists
    before taking the new password and confirm password and making sure
    they are the same"""
    users = get_user_list()
    new_username = input("Please enter the new username to be added: ")
    if new_username in users:
        print("This username already exists. Please try again.")
    else:
        new_password = input("Enter password: ")
        confirm_password = input("Please confirm password: ")
        while True:
            if new_password == confirm_password:
                with open("user.txt", "a+", encoding="utf-8") as file:
                    file.write(f"\n{new_username}, {new_password}")
                print("New user added")
                break
            print("These passwords do not match please try again")
            new_password = input("Enter password: ")
            confirm_password = input("Please confirm password: ")


def sequentrial_search(target, items):
    """A simple search algorthm that itereates through a list to find a
    certain value and returns the index if found or None if not"""
    for index in range(len(items)):
        if items[index] == target:
            return index
    return None


def user_login():
    """uses 2 list to take usernames and passwords from user.txt and check
them against the user input, then searches to see if they exists and
the password is the right one for that index, if not an error is
raised otherwise a success message is displayed and the user continues
to the main menu"""
    usernames = []
    passwords = []
    with open("user.txt", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.split(',')
            usernames.append(line[0])
            passwords.append(line[1])
    while True:
        username_attempt = input("Please enter username ")
        password_attempt = input("Please enter your password ")
        index = sequentrial_search(username_attempt, usernames)
        if index is None:
            print("Incorrect username or password")
        elif index is not None and password_attempt != passwords[index]:
            print("Incorrect username or password")
        else:
            print("Log in Successful")
            return username_attempt


def new_task(users):
    """This function checks if the input user exists, before taking
    further details of the task. When the due date is entered, there is
    a check foir the format, then sets the task done status to No. Finally
    it adds all the information gathered into the tasks.txt file"""
    date_format = "%d-%m-%Y"
    task_user = input("Which user is this task for? ")
    users = get_user_list()
    if task_user not in users:
        print("Sorry that user doesnt exist please try again")
    else:
        task_title = input("What is the title of this task? ")
        task_description = input("Enter a short task description ")
        while True:
            task_due = input(
                "When is the task due for? Please use DD-MM-YYYY format ")
            try:
                task_due_format = datetime.strptime(
                    task_due, date_format)
                task_due = task_due_format.strftime('%d-%b-%Y')
                task_due = task_due.replace("-", " ")
                task_set = datetime.now()
                task_set = task_set.strftime('%d-%b-%Y')
                task_set = task_set.replace("-", " ")
                break
            except ValueError:
                print("The date input is incorrect, Please try again")
        task_done = "no"
        with open("Tasks.txt", "a+", encoding="utf-8") as file:
            file.write(f"\n{task_user}, {task_title}, {task_description}, "
                       + f"{task_set}, {task_due}, {task_done}")
        print("New task added to file")


def read_tasks():
    """This function opens the tasks.txt file and reads each of the tasks
    and converts them into a list of Task objects"""
    task_list = []
    with open("Tasks.txt", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(",")
            task_list.append(
                Task(line[0], line[1], line[2], line[3], line[4], line[5])
                )
    return task_list


def view_all():
    """This function reads in all the tasks from tasks.txt, formats them
    and creates a list, by converting all the data into objects, then adds
    each part to a table to make display more user friendly"""
    task_list = []
    j = 1
    with open("Tasks.txt", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(",")
            task_list.append(
                Task(line[0], line[1], line[2], line[3], line[4], line[5])
                )
        table = []
        for i in task_list:
            table.append([j, i.get_user(), i.get_title(),
                         i.get_date_assign(), i.get_date_due(),
                         i.get_status()])
            j += 1
        print(tabulate(table, headers=["Task number", "Assigned User", "Title",
                                       "Date Assigned",
                                       "Date Due", "Task Completed?"],
                       tablefmt="github"))

    return task_list


def view_my_tasks(user):
    """This function checks the assigned user of each task against the
    user currently logged in, then returns a table populated with each
    task that is assigned to that user"""
    table = []
    counter_list = []
    j = 1
    task_list = read_tasks()
    for i in task_list:
        if i.get_user() == user:
            table.append([j, i.get_title(),
                          i.get_date_assign(), i.get_date_due(),
                          i.get_status()])
            counter_list.append(j)
            j += 1
        else:
            continue
    print(tabulate(table, headers=["Task number", "Title",
                                   "Date Assigned",
                                   "Date Due", "Task Completed?"],
                   tablefmt="github"))
    while True:
        try:
            print("Do you need to edit any tasks?")
            edit_choice = input("Enter Y or N ")
            edit_choice = edit_choice.lower()
            if edit_choice == 'n':
                break
            if edit_choice == 'y':
                task_edit(task_list)
        except ValueError:
            print("Thats not a valid input, please try again")


def task_edit(tasks):
    """This function recusivly calls itself to allow the user to make
    multiple adjustments to the user and sue date values in each object.
    The user then has the choice to exit after each change or call the
    function again to change something different"""
    count_choice = int(input("Which task to do you need to edit? "))
    i = 0
    while i < (count_choice - 1):
        i += 1
    if tasks[i].get_status() == "Yes":
        print("This task is already completed")
        return
    print(f"Title: {tasks[i].get_title()}," +
          f"\n User: {tasks[i].get_user()}," +
          f"\nDate due: {tasks[i].get_date_due()}," +
          f"\nStatus: {tasks[i].get_status()}")
    item_choice = input(
        "What do you need to edit, User (U), Due date(DD)"
        "or Mark task as complete (C)? "
        )
    if item_choice.lower() == "u":
        while True:
            user_update = input(
                "Which user is being assigned this task? "
                )
            assignable_users = get_user_list()
            if user_update not in assignable_users:
                print("That user does not exist")
            else:
                tasks[i].user = user_update
                with open("Tasks.txt", "w", encoding="utf-8") as file:
                    for task in tasks:
                        file.write(task.get_user(), task.get_title(),
                                   task.get_description(),
                                   task.get_date_assign(),
                                   task.get_date_due(), task.get_status())
                    print("Do you need to edit anything else?")
                    cont_choice = input("Enter y or n to select: ")
                    if cont_choice.lower() == "y":
                        task_edit(tasks)
                    if cont_choice.lower() == "n":
                        return
    elif item_choice.lower() == "dd":
        while True:
            try:
                date_update = input(
                    "What is the new due date? "
                    )
                date_update = date.strptime(
                    date_update, '%d-%b-%Y')
                date_update = date_update.replace("-", " ")
                tasks[i].date_due = date_update
                with open("Tasks.txt", "w", encoding="utf-8") as file:
                    for task in tasks:
                        file.write(task)
                    print("Do you need to edit anything else?")
                    cont_choice = input(
                                        "Enter y or n to select: "
                                    )
                    if cont_choice.lower() == "y":
                        task_edit(tasks)
                    elif cont_choice.lower() == "n":
                        return
            except ValueError:
                print("The date input is incorrect")
    elif item_choice.lower() == "c":
        tasks[i].task_complete()
        with open(
            "Tasks.txt", "w", encoding="utf-8"
                 ) as file:
            for task in tasks:
                file.write(task)
            print("Do you need to edit anything else?")
            cont_choice = input("Enter y or n to select: ")
            if cont_choice.lower() == "y":
                task_edit(tasks)
            if cont_choice.lower() == "n":
                return


def view_completed_tasks():
    """This function creates a list of tasks that are marked as completed
    before formatting them into a table for easy user reading"""
    completed_tasks = []
    complete_table = []
    task_list = []
    with open("Tasks.txt", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.split(',')
            task_list.append(
                Task(line[0], line[1], line[2], line[3], line[4], line[5])
                )
            for i in task_list:
                if i.get_status() == "No":
                    continue
                elif i.get_status() == "Yes":
                    completed_tasks.append(i)
            for i in completed_tasks:
                complete_table.append([i.get_user(), i.get_title(),
                                       i.get_description(),
                                       i.get_date_assign(), i.get_date_due(),
                                       i.get_status()])
            print(tabulate(complete_table, headers=["Assigned User",
                                                    "Title",
                                                    "Description",
                                                    "Date Assigned",
                                                    "Date Due",
                                                    "Task Completed?"],
                           tablefmt="github"))


def delete_task():
    """This task displays all the tasks that are currently in the
    Tasks.txt file, then asks the user to enter the title of the task
    they would like to delete. The function then searches for the index
    of the task and deletes the entire object, before re-writing the
    updated list and displaying the new list of tasks"""
    view_all()
    task_list = read_tasks()
    j = 0
    while True:
        task_choice = int(input("Enter task number to delete: "))
        if task_choice > len(task_list):
            print("That is not a valid input")
        while j < (task_choice - 1):
            j += 1
            if j == (task_choice - 1):
                task_list.pop(j)
        with open("Tasks.txt", "w", encoding="utf-8") as file:
            for task in task_list:
                file.write(f"{task.get_user()}, {task.get_title()}," +
                           f"{task.get_description()}," +
                           f"{task.get_date_assign()}," +
                           f"{task.get_date_due()}," +
                           f"{task.get_status()}\n")
        view_all()
        break


def get_user_list():
    """This function creates a list of all the usernames to reference in
    other functions"""
    people = []
    with open("user.txt", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.split(',')
            people.append(line[0])
    return people


def generate_task_report():
    """This program creates a list of tasks, checks if the report file
    already exists and deletes it so it can be made fresh with up to date
    information. Then certain data handeling is done to create a list of
    requirted information to be written to the txt file"""
    tasks = read_tasks()
    j = 0
    x = 0
    path = './task_overview.txt'
    check_file = os.path.isfile(path)
    if check_file is True:
        os.remove('task_overview.txt')
    for task in tasks:
        if task.get_status() == "Yes":
            j += 1
        continue
    incomplete_tasks = len(tasks) - j
    for task in tasks:
        task_status = task.get_status().strip().lower()
        task_due_date = task.get_date_due().strip()
        date_due_obj = datetime.strptime(task_due_date, '%d %b %Y').date()
        today_date_obj = date.today()
        if task_status == "no" and (today_date_obj > date_due_obj):
            x += 1
            continue
    incomplete_percentage = (incomplete_tasks / len(tasks)) * 100
    overdue_percentage = (x / len(tasks)) * 100
    with open("task_overview.txt", "a+", encoding="utf-8") as file:
        file.write(f"Number of tasks: {len(tasks)}\nCompleted tasks: {j}\n"
                   f"Incomplete tasks: {incomplete_tasks}\n" +
                   f"Overdue tasks: {x}\n" +
                   f"Percent incomplete: {incomplete_percentage}%\n"
                   f"Percent overdue: {overdue_percentage}%\n")


def generate_user_report():
    """This program firstly checks for the existance of user_overview.txt
    before calling functions to get the users and the task lists. It then
    writes the relevant information to the txt file"""
    path = './user_overview.txt'
    check_file = os.path.isfile(path)
    if check_file is True:
        os.remove('user_overview.txt')
    users = get_user_list()
    tasks = read_tasks()
    user_tasks = 0
    complete_tasks = 0
    overdue = 1
    task_percentage = (user_tasks / len(tasks)) * 100
    with open("user_overview.txt", "a+", encoding="utf-8") as file:
        file.write(f"Number of users: {len(users)}\n" +
                   f"Number of tasks: {len(tasks)}\n\n")
    for user in users:
        user_tasks = 0
        percentage_completed = 0
        percentage_incomplete = 100
        for task in tasks:
            task_status = task.get_status().strip().lower()
            task_due_date = task.get_date_due().strip()
            date_due_obj = datetime.strptime(task_due_date, '%d %b %Y').date()
            today_date_obj = date.today()
            if task.get_user() == user:
                user_tasks += 1
                if task_status == "yes":
                    complete_tasks += 1
                if task_status == "no" and (date_due_obj > today_date_obj):
                    overdue += 1
                    continue
        if complete_tasks != 0:
            percentage_completed = (complete_tasks / user_tasks) * 100
        percentage_incomplete = 100 - percentage_completed
        if user_tasks == 0:
            with open("user_overview.txt", "a+", encoding="utf-8") as file:
                file.write(
                        f"User: {user}\n"
                        f"Number of tasks assigned: {user_tasks}\n" +
                        f"Percentage of total assigned: {task_percentage}%\n" +
                        f"Completion percentage: {percentage_completed}%\n" +
                        "Percentage incomplete: 0%\n" +
                        "Percentage overdue: 0%\n\n"
                            )

        elif task_percentage != 0.0:
            overdue_tasks = (overdue / task_percentage) * 100
            with open("user_overview.txt", "a+", encoding="utf-8") as file:
                file.write(
                        f"User: {user}\n"
                        f"Number of tasks assigned: {user_tasks}\n" +
                        f"Percentage of total assigned: {task_percentage}%\n" +
                        f"Completion percentage: {percentage_completed}%\n" +
                        f"Percentage incomplete: {percentage_incomplete}%\n" +
                        f"Percentage overdue: {overdue_tasks}%\n\n"
                            )
        else:
            with open("user_overview.txt", "a+", encoding="utf-8") as file:
                overdue_tasks = 100
                file.write(
                        f"User: {user}\n"
                        f"Number of tasks assigned: {user_tasks}\n" +
                        f"Percentage of total assigned: {task_percentage}%\n" +
                        f"Completion percentage: {percentage_completed}%\n" +
                        f"Percentage incomplete: {percentage_incomplete}%\n" +
                        f"Percentage overdue: {overdue_tasks}%\n\n"
                            )


# ==== Login Section =====
current_user = user_login()
usernames = get_user_list()
if current_user == "admin":
    while True:
        menu = input(
            "Please make a selection:\n"
            "r - register a user\n"
            "a - add task\n"
            "va - view all tasks\n"
            "vm - view my tasks\n"
            "vc - view completed tasks\n"
            "del - delete tasks\n"
            "ds - generate task and user reports\n"
            "e - exit\n")

        menu = menu.lower()

        if menu == 'r':
            reg_user(usernames)

        elif menu == 'a':
            new_task(usernames)

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_my_tasks(current_user)

        elif menu == 'vc':
            view_completed_tasks()

        elif menu == 'del':
            delete_task()

        elif menu == 'ds':

            generate_task_report()
            generate_user_report()
            print("The reports are ready to view")

        elif menu == 'e':
            print('Goodbye!!!')
            sys.exit()

        else:
            print("You have entered an invalid input. Please try again")

else:
    while True:

        menu = input(
            """Please make a selection:
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        """)

        menu = menu.lower()

        if menu == 'a':
            new_task(usernames)

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_my_tasks(current_user)

        elif menu == 'e':
            print('Goodbye!!!')
            sys.exit()

        else:
            print("You have entered an invalid input. Please try again")
