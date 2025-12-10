import math
""" This is a simple calulator to display the values of either and investment
or monthly repayment of a bond, depending which the user required

user inputs for investments: 
    deposit amount, investment interest, type of investment (simple or 
    compound) and time invested

user inputs for bond:
    value of the property, interest rate and time to repay

returns:
    the total return of investment depending on which type of interest selected
    or
    the total monthly repayment for the bond they are calculating"""


def investment_calc_simple(interest, length, funds):
    '''This function with calculate the simple investment value
    rate: the conversion of the percentage into the decimal
    nvest_interest, length, funds: all gathered as user inputs
    total_simple: the value of the calculations, formatted for legibility'''
    rate = float(interest / 100)
    total_simple = (funds * (1 + (rate * length)))
    total_simple = round(total_simple, 2)
    total_simple = format(total_simple, ",")
    print(f"Your total after interest is {total_simple}")


def investment_calc_compound(interest, length, funds):
    '''This function to do the compound interest calculation
    rate: the conversion of the percentage into the decimal
    interest, length, funds: all gathered as user inputs
    total_comp: the calcualated value thats formatted for legibility'''
    rate = float(interest / 100)
    total_comp = funds * math.pow((1 + rate), length)
    total_comp = round(total_comp, 2)
    total_comp = format(total_comp, ",")
    print(f"Your investment total is {total_comp}")


def bond_calc(value, interest, length):
    '''This function calculates monthly repayment
    bond_rate: is the calculated monthly interest rate
    value, interest and length are all user inputs
    month_repay: the repayment value formatted for legibility'''
    bond_rate = float((interest / 100) / 12)
    month_repay = (bond_rate * value) / (1 - (1 + bond_rate) ** (-length))
    month_repay = round(month_repay, 2) and format(month_repay, ",")
    print(f"Your monthly repayment will be {month_repay}")


# where the user makes their choice about which service they need
print(
    "Investment - to calculate the amount of interest you'll earn on your investment."
    )
print(
    "Bond - to calculate the amount you'll have to pay on your home loan."
    )
# loops the main menu input to ensure correct entry by user
while True:
    try:
        menu_choice = input(
            "Enter either 'Investment' or 'Bond' from the menu above to proceed: "
            )

        # This set of nested ifs gathers all the required inputs and verifies
        # if they are valid inputs before continuing, and then are all used in
        # the various functions to perform the calculations
        if menu_choice.lower() == "investment":

            # a loop to ensure a valid int entry from the user

            while True:
                try:
                    deposit = int(input("How much money are you depositing? £"))
                    break
                except ValueError:
                    print("Enter your deposit as whole numbers only")

            # a loop to ensure a valid float input
            while True:
                try:
                    invest_interest = float(input("What is your interest rate? "))
                    break
                except ValueError:
                    print("please enter your interest rate as numbers only to 2dp")

            # a loop to ensure a valid int entry from the user
            while True:
                try:
                    invest_len = int(input(
                        "how many years are you planning on investing? "))
                    break
                except ValueError:
                    print(
                        "Please enter your investment time rounded to the whole year ")

            invest_type = input("Would you like compound or simple interest? ")
            # keeps the user in a loop until a valid input is entered and the
            # calculation function is called
            while True:
                if invest_type.lower() == "compound":
                    investment_calc_compound(invest_interest, invest_len, deposit)
                    break
                if invest_type.lower() == "simple":
                    investment_calc_simple(invest_interest, invest_len, deposit)
                    break
                print("Sorry please check spelling and try again.")

        # goes through all user inputs with looping error checks to ensure valid inputs
        elif menu_choice.lower() == "bond":
            # a loop to ensure a valid int entry from the user
            while True:
                try:
                    house_val = int(input("What is the value of the property? "))
                    break
                except ValueError:
                    print("Please enter the property value in whole numbers only")
            # a loop to ensure a valid float input
            while True:
                try:
                    bond_interest = float(input("What is the interest rate? "))
                    break
                except ValueError:
                    print("please enter the interest rate as numbers and decimals only")
            # a loop to ensure a valid int entry from the user
            while True:
                try:
                    bond_len = int(input("How many months are you planning to repay? "))
                    break
                except ValueError:
                    print("please enter the month rounded to the nearest whole month")

            bond_calc(house_val, bond_interest, bond_len)

    except ValueError:  # error response from main menu
        print("Sorry please check spelling and try again.")

# FURTHER DEVELOPMENT
# find a cleaner way to do error checks that arent while True/try loops
