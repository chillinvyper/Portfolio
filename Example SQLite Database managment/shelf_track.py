import sqlite3
import sys
from tabulate import tabulate

db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()
# creating and populating book table
with db:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS book
                (
                id INTEGER PRIMARY KEY,
                title TEXT,
                authorID INTEGER,
                qty INTEGER,
                FOREIGN KEY (authorID)
                        REFERENCES author (id)
                    )
                ''')
    db.commit()
    cursor.execute('''
    INSERT OR IGNORE INTO book(id, title, authorID, qty)
                VALUES
                (3001, 'A Tale of Two Cities', 1290, 30),
                (3002, "Harry Potter and the Philosopher's stone", 8937, 40),
                (3003, 'The Lion, the Witch, and the Wardrobe', 2356, 25),
                (3004, 'The Lord of the Rings', 6380, 37),
                (3005, "Alice's Adventures in Wonderland", 5620, 12)
                ''')
    db.commit()

    # creating and populating author table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS author
                (
                id INTEGER PRIMARY KEY,
                name TEXT,
                country TEXT
                )
                ''')
    db.commit()
    cursor.execute('''
    INSERT OR IGNORE INTO author(id, name, country)
                VALUES
                (1290, 'Charles Dickens', 'England'),
                (8937, 'J.K.Rowling', 'England'),
                (2356, 'C.S.Lewis', 'Ireland'),
                (6380, 'J.R.R.Tolken', 'South Africa'),
                (5620, 'Lewis Carroll', 'England')
                ''')
    db.commit()


def add_author():
    '''This function allows the user to add an author if the author isnt
    currently in the database'''
    with db:
        author_name = input("What is the name of the author? ")
        cursor.execute('''SELECT name FROM author WHERE name = ?''',
                       author_name)
        author = cursor.fetchone()
        # A check to ensure author isnt already in database and returns
        # their ID
        if author:
            cursor.execute('''SELECT id FROM author WHERE name = ?''',
                           author_name)
            author_id = cursor.fetchone()
            print("That author is already in the database, their ID is" +
                  f"{author_id}")
            return author_id
        # An error catch to ensure the correct ID format for the new author
        while True:
            new_code = int(input("What is the new authors 4 digit code? "))
            if len(str(new_code)) != 4:
                print("That is an invalid input, please try again")
            else:
                break
        new_country = input("What country is the author from? ")
        # Writes all the new author information to the database
        cursor.execute(
            '''
            INSERT INTO author(id, name, country)
            VALUES(?, ?, ?)
            ''', (new_code, author_name, new_country)
        )
        db.commit()
        return new_code


def display_book(book_to_display_id):
    '''A helper function to display a book based on the input book ID'''
    table = []
    with db:
        cursor.execute('''SELECT book.id, book.title, author.name,
                       book.qty FROM book WHERE book.id = ?''',
                       (book_to_display_id))
        book_to_display = cursor.fetchone()
        table.append([book_to_display[0], book_to_display[1],
                      book_to_display[2], book_to_display[3]])
        print(tabulate(table, headers=['Book ID', 'Book Title', 'Author Name',
                                       'Book Quantity']))


def new_book():
    '''This function takes required inputs and addes them into the
    book table, after checking they dont already exist. if all checks are
    passed, inserts it into the new row'''
    with db:
        cursor.execute('''SELECT id FROM book''')
        book_ids = cursor.fetchall()
    high_id = max(book_ids)
    highest_id, *blank = high_id
    new_book_id = highest_id + 1

    with db:
        book_title = input("What is the name of the new book? ")
        cursor.execute('''SELECT title FROM book WHERE title = ?''',
                       (book_title,))
        title_check = cursor.fetchone()
        # Ensures the book is not already in the database, or the name already
        # exists
        if title_check:
            print("That book is already in the database")
            return
    with db:
        while True:
            try:
                # A check for an existing author, or if they do not exist
                # calls a function to add a new author to the database
                author_add = input("What is the name of the author? ")
                cursor.execute(
                    '''SELECT name FROM author WHERE name = ?''',
                    (author_add,))
                author_check = cursor.fetchone()
                if author_check:
                    cursor.execute(
                        '''SELECT id FROM author WHERE name = ?''',
                        author_add)
                    author_check_id = cursor.fetchone()
                    break
                author_check_id = add_author()
                break
            except ValueError:
                print("That is an invalid input")
        while True:
            try:
                # A small error catch to ensure the quantity is an integer
                new_quant = int(input("How many copies do you have? "))
                break
            except ValueError:
                print(
                    "Invalid input, please use whole numbers only")
        # Writes all the new details to the database
        with db:
            cursor.execute(
                '''
                INSERT INTO book(id, title, authorID, qty)
                VALUES (?, ?, ?, ?)
                ''', (new_book_id, book_title, author_check_id, new_quant,)
            )
            db.commit()
            print("New book added to database")


def update_book_qty():
    '''this function takes the book ID and verifies its existance before
    recieving the new qty to update the database with'''

    while True:
        try:
            id_to_update = int(input("What is the id of the book to update? "))
            break
        except ValueError:
            print("Enter 4 numbers only")

    # Searches for the entered ID in the database and
    # calls the function to display the details
    # to ensure it is the correct book they are trying to update
    with db:
        cursor.execute('''SELECT id FROM book WHERE id = ?''', (id_to_update))
        book_to_update = cursor.fetchone()
        if not book_to_update:
            print("That book doesnt exist please go back and check ID")
            return
        display_book(id_to_update)

    # Takes the new qty and checks that it is an integer, before updating
    # the value in the database
    while True:
        try:
            update_qty = int(input("What is the new quantity? "))
            break
        except ValueError:
            print("Enter whole numbers only")
    cursor.execute('''
                    UPDATE book SET book.qty = ? WHERE book.id = ?''',
                   (update_qty, id_to_update))
    db.commit()
    print("Quantity has been updated")


def update_book_title():
    '''this function takes the book ID and verifies its existance before
    recieving the new qty to update the database with'''
    while True:
        try:
            id_to_update = int(input("What is the id of the book to update? "))
            break
        except ValueError:
            print("Enter 4 numbers only")

    # Searches for the entered ID in the database and displays the details
    # to ensure it is the correct book they are trying to update
    with db:
        cursor.execute('''SELECT id FROM book WHERE id = ?''', (id_to_update))
        book_to_update = cursor.fetchone()
        if not book_to_update:
            print("That book doesnt exist please go back and check ID")
            return
        display_book(id_to_update)

    # Takes the new title string input and updates it to the database
    update_title = input("What is the updated title? ")
    cursor.execute('''
                    UPDATE book SET book.title = ? WHERE book.id = ?''',
                   (update_title, id_to_update))
    db.commit()
    print("Quantity has been updated")


def update_author():
    '''this function takes the book ID and verifies its existance before
    recieving the new qty to update the database with'''
    while True:
        try:
            id_to_update = int(input("What is the id of the book to update? "))
            break
        except ValueError:
            print("Enter 4 numbers only")

    # Searches for the entered ID in the database and displays the details
    # to ensure it is the correct book they are trying to update
    cursor.execute('''SELECT id FROM book WHERE id = ?''', (id_to_update))
    book_to_update = cursor.fetchone()
    if not book_to_update:
        print("That book doesnt exist please go back and check ID")
    display_book(id_to_update)

    # Takes the author ID input, ensures it is a valid integer and exists
    # in the database, before updating the database with the new author
    while True:
        try:
            with db:
                author_to_update = int(input("Enter the ID of the new author ")
                                       )
                cursor.execute('''
                                SELECT author.name From author WHERE
                               author.id = ?
                            ''', (author_to_update))
                author_check = cursor.fetchone()
                if not author_check:
                    print("That author ID doesnt exist, please try again")
                break
        except ValueError:
            print("Enter the 4 digit ID using numbers only")
    with db:
        cursor.execute('''UPDATE book SET book.authorID = ?
                       WHERE book.id = ?''',
                       (author_to_update, id_to_update))
        db.commit()
        print("Author has been updated")


def delete_book():
    '''This function takes the ID of the book to delete, checks that it
    exists and is entered properly, before removing it forom the database'''
    while True:
        # Checks that the input is a valid integer
        try:
            delete_id = int(input("Enter ID of book to delete "))
            break
        except ValueError:
            print("Enter the ID as numbers only")

    # Trys to retrieve book from database to ensure its existance
    with db:
        cursor.execute('''SELECT * FROM book WHERE id = ?''', (delete_id))
        exist_check = cursor.fetchone()

    # If the book exists, deletes it, otherwise displays an error
    if exist_check:
        with db:
            cursor.execute('''
                            DELETE FROM book WHERE book.id = ?''', (delete_id))
            print("Book deleted successfuly")
    else:
        print("That book is not in the database")


def search_book():
    '''This function takes the book ID, verifies its a correct input. It
    then attempts to retieve the details from the database, if there are
    no results, displays an error otherwise it displays the details'''
    while True:
        # An error check to ensure a correct integer input
        try:
            search_id = int(input("Enter ID of book to find "))
            break
        except ValueError:
            print("Enter the ID as numbers only")
    # Attempts to retrieve details of the book from the database
    cursor.execute('''
                   SELECT book.id, book.title, authorID, qty FROM book WHERE
                   book.id = ?''', (search_id))
    search_result = cursor.fetchone()
    # If there is a book, displays all the details, otherwise displays
    # an error
    if search_result:
        table = []
        table.append(search_result[0], search_result[1], search_result[2],
                     search_result[3])
        print(tabulate(table, headers=['Book ID', 'Book Title', 'Author ID',
                                       'Book Quantity'], tablefmt='grid'))
    print("That book is not in the database")


def view_all():
    '''This function retrieves all the information from the database and
    displays it all in a table format'''
    table = []
    with db:
        cursor.execute('''
                        SELECT book.id, book.title, author.name,
                       author.country,
                        book.qty FROM book INNER JOIN author ON book.authorID =
                        author.id
                        ''')
        book_details = cursor.fetchall()
        for book in book_details:
            table.append([book[0], book[1], book[2], book[3], book[4]])
        print(tabulate(table, headers=['Book ID', 'Book Title', 'Author Name',
                                       'Author Country', 'Book Quantity'],
                       tablefmt='grid'))


# =========Main Menu===========
while True:
    print("=====Main Menu=====")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search book")
    print("5. View all book details")
    print("0. Exit")

    try:
        menu_choice = int(input("What would you like to do? "))
        if menu_choice == 1:
            new_book()
        elif menu_choice == 2:
            while True:
                try:
                    print("What would you like to update?")
                    print("1. Book Quantity")
                    print("2. Book Author")
                    print("3. Book Title")
                    print("0. Back to Main Menu")
                    update_choice = int(input("Enter your choice here: "))
                    break
                except ValueError:
                    print("That is an invalid input, enter the number"
                          "to select option")
            if update_choice == 1:
                update_book_qty()
            elif update_choice == 2:
                update_author()
            elif update_choice == 3:
                update_book_title()
            elif update_choice == 0:
                break
            else:
                print("That is an invalid input")

        elif menu_choice == 3:
            delete_book()
        elif menu_choice == 4:
            search_book()
        elif menu_choice == 5:
            view_all()
        elif menu_choice == 0:
            print("Goodbye!")
            sys.exit()
        else:
            print("That is an invalid input, please try again")

    except ValueError:
        print("please enter the number of your selection only")


# ======= Future Development ==========
# 1. refactor update, get book choice in seperate function and pass input
# as argument

# 2. delete confirmation?
