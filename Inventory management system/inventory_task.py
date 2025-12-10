'''A simple shoe inventory system, with search and order functions as well as
functions to find what shoes should be on sale, and which need odering in.
Finally there is functionality to add new shoes to the stock list'''

import sys
from tabulate import tabulate


class Shoe:
    '''Creates the class Shoe, each object has: product name, code,
    country, quantity, cost'''

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_code(self):
        """Returns the code value of the object for data handling"""
        return self.code

    def get_cost(self):
        """Returns the cost value of the object for data handling"""
        return self.cost

    def get_quantity(self):
        """Returns the quantity value of the object for data handling"""
        return self.quantity

    def get_product(self):
        """Returns the product name of the object for data handling"""
        return self.product

    def get_country(self):
        """Returns the country of the object for data handling"""
        return self.country

    def __str__(self):
        '''returns the string representation of the object'''
        return (
            f"{self.country}, {self.code}, {self.product}, {self.cost}\
                {self.quantity}"
        )


# =============Shoe list===========
# an empty list for storing shoes
shoe_list = []


# ==========Functions outside the class==============
def sequential_search(to_find, items):
    '''iterates over the list and returns the index, or else none'''
    for index in range(len(items)):
        if items[index] == to_find:
            return index
    # if target item not found returns none
    return None


def highest_qty(shoes_list):
    '''returns the highest quantity in the list of shoes'''
    largest_stock = max(shoes_list, key=lambda x: int(x.get_quantity()))
    return largest_stock


def lowest_quantity(shoes_list):
    '''returns the lowest quantity in the list of shoes'''
    min_stock = min(shoes_list, key=lambda x: int(x.get_quantity()))
    return min_stock


def read_shoes_data():
    """creates a list of objects from all entries in the inventory text file"""
    shoes_list = []
    while True:
        try:
            with open("inventory.txt", "r+", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines[1::]:
                    line = line.strip("\n")
                    line = line.split(",")
                    shoes_list.append(
                        Shoe(line[0], line[1], line[2], line[3], line[4])
                        )
        except FileNotFoundError:
            print("That file has not been found please try again")
        return shoes_list


def capture_shoes(list_of_shoes):
    '''Takes information from the user and creates an object, then add
    it to the list and also updates the text file'''

    country = input("What country is the shoe from? ")
    prod_code = input("What is the products code? ")
    prod_name = input("What is the name of the new product? ")

    while True:
        try:
            prod_cost = int(input("How much does the new product cost? £ "))
            while True:
                try:
                    prod_quant = int(input(""
                                     "How much of the product do we have? "))
                    list_of_shoes.append(
                     Shoe(country, prod_code, prod_name, prod_cost, prod_quant)
                    )
                    break
                except ValueError:
                    print("Sorry that is an invalid input, please try again")
            break
        except ValueError:
            print("Sorry that is an invalid input, please try again")

    with open("inventory.txt", "a+", encoding="utf-8") as f:
        f.write(f"\n{country},{prod_code},{prod_name},{prod_cost},{prod_quant}"
                )


def view_all(shoes_list):
    '''Iteraltes through the list and displays the products in a table'''
    table = []
    for i in shoes_list:
        table.append([i.get_country(), i.get_code(), i.get_product(),
                      i.get_cost(), i.get_quantity()])
    print(tabulate(table, headers=["Country", "Code", "Product", "Cost",
                                   "Quantity"], tablefmt="github"))


def re_stock(shoe_list, target, low_shoe):
    """This allows the user to add an amount to the quantity value and then
    re-writes the file with all the updated values"""
    order_val = int(input("How many more would you like to order? "))
    target.quantity = int(target.quantity) + order_val
    print(
        f"The new stock value of {target.get_product()} is\
            {target.get_quantity()}"
        )
    shoe_names = []
    for i in shoe_list:
        shoe_names.append(i.get_product())
    low_shoe_index = sequential_search(low_shoe, shoe_names)
    shoe_list.pop(low_shoe_index)
    shoe_list.append(Shoe(target.get_country(), target.get_code(),
                     target.get_product(),
                     target.get_cost(), target.get_quantity()))
    for i in shoe_list:
        with open("inventory.txt", "w", encoding="utf-8") as file:
            file.write(
                    f"{i.get_country()}, {i.get_code()}, " +
                    f"{i.get_product()}, "
                    + f"{i.get_cost()}, {i.get_quantity()} \n"
                    )
    read_shoes_data()


def search_shoe(shoes_list):
    '''This takes the shoe code and runs a search of the index, then
    uses that index to display all information on the shoe'''

    while True:
        try:
            to_find = input("Enter product code: ")
            code_list = []
            for i in shoes_list:
                code_list.append(i.get_code())
            index = sequential_search(to_find, code_list)
            if index is None:
                print("That code could not be found")
            else:
                print(f"Product: {shoes_list[index].get_product()} " +
                      f"Price: {shoes_list[index].get_cost()} " +
                      f"Quantity: {shoes_list[index].get_quantity()}")
                break
        except ValueError:
            print("That code is incorrect, please try again")


def value_per_item(shoes_list):
    '''iterates through the objects, and displays the name, code
    quantity and cost per item, before calculating the total value of the stock
    and displaying it in a table'''
    cost_table = []
    for i in shoes_list:
        quantity_item = i.get_quantity()
        product = i.get_product()
        code = i.get_code()
        cost = i.get_cost()
        value = int(quantity_item) * float(cost)
        value = format(value, ",")
        cost_table.append([product, code, value])
    print(tabulate(cost_table, headers=["Product", "Code", "Total Value"],
          tablefmt="grid"))


# ==========Main Menu=============


while True:
    shoe_list = read_shoes_data()

    print("What would you like to do?")
    print("1. View all the shoes in inventory")
    print("2. Check which shoe needs re-stocking")
    print("3. Search for a particular shoe")
    print("4. Check the current value of all shoes")
    print("5. See which shoe is to go on sale")
    print("6. Add a new product")
    print("7. Exit")
    menu_choice = int(input("Enter your selection here: "))

    if menu_choice == 1:
        view_all(shoe_list)

    elif menu_choice == 2:
        lowest_quantity(shoe_list)
        target = lowest_quantity(shoe_list)
        print(f"We have the lowest stock of {target.get_product()}")
        low_shoe = target.get_product()
        re_stock(shoe_list, target, low_shoe)

    elif menu_choice == 3:
        search_shoe(shoe_list)

    elif menu_choice == 4:
        value_per_item(shoe_list)

    elif menu_choice == 5:
        max_item = highest_qty(shoe_list)
        sequential_search(max_item, shoe_list)
        print(f"The shoe that needs to be on sale is {max_item.get_product()}")

    elif menu_choice == 6:
        capture_shoes(shoe_list)

    elif menu_choice == 7:
        print("Goodbye!")
        sys.exit()

    else:
        print("Sorry, thats not valid, please try again")
