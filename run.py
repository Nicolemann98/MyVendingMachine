import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("my_vending_machine")


all_products = []
PRODUCT_QUANTITY_CELL_NUMBER = 2

class Product():
    """
    Creates instance of Product. The class variables of this object should match the column names of the product table
    """
    def __init__(self, item_name, quantity, price, sales, income):
        self.item_name = item_name
        self.quantity = int(quantity)
        self.price = int(price)
        self.sales = int(sales)
        self.income = int(income)

    def get_product_text(self):
        """
        Takes the product object and shows in a user readable format for the menu screen, also lets user know if item is out of stock
        """
        if (self.is_item_in_stock()):
            return f"{self.item_name} - {format_price(self.price)} - {self.quantity} in stock."
        else:
            return f"{self.item_name} - OUT OF STOCK."

    def is_item_in_stock(self):
        return self.quantity != 0

    def buy_item(self):
        self.quantity -= 1
        self.sales += 1
        self.income += self.price


def format_price(price_in_pence):  
        """
        Takes the price from a number in pence (e.g. 124) and returns it in standard price format (e.g. £1.24)
        """  
        pounds = price_in_pence // 100
        pence = price_in_pence % 100
        
        return f"£{pounds}.{str(pence).zfill(2)}"

def set_up_products():
    """
    Takes the data from the product spreadsheet, creates a Product object for each row and adds to the all_products list
    """
    product_worksheet = SHEET.worksheet("product")
    for product_unformatted in product_worksheet.get_all_values()[1:]:
        product = Product(product_unformatted[0], product_unformatted[1], product_unformatted[2], product_unformatted[3], product_unformatted[4])
        all_products.append(product)

def get_user_input():
    """
    Displays the welcome screen and asks the user for their item
    """
    def validate_selection(selection):
        """
        Takes the user's selection input and checks that it is both a valid input and that the chosen item is in stock.
        Returns True if the input is valid and False if it is invalid
        """
        if selection == str(len(all_products)):
            #  this is for the stock manager selection option
            return True
        else:
            try:
                chosen_product = all_products[int(selection)]
                if chosen_product.is_item_in_stock():
                    return True
                else:
                    print(f"Apologies {chosen_product.item_name} is currently out of stock.")
                    return False
            except:
                print(f"{selection} is not a valid input. Please select one of the options.")
                return False

    print("\nWelcome to the Vending Machine.")
    input("Please press enter to start.")
    print("\nWhat would you like today?")
    print(f"Please enter a number between 0 and {len(all_products)} to choose your selection.")
    for i in range(len(all_products)):
        product = all_products[i]
        print(f"{i}: {product.get_product_text()}")
    print(f"{len(all_products)}: Log in as stock manager.")

    is_selection_valid = False
    while not is_selection_valid:
        selection = input("Selection: ")
        is_selection_valid = validate_selection(selection)

    selection_number = int(selection)

    if selection_number == len(all_products):
        return manager_log_in()
    else:
        chosen_product = all_products[selection_number]
        dispense_item(chosen_product, selection_number)
        return False

def dispense_item(product, selection_number):
    """
    This asks for the user's money, "dispenses" the item and adjusts the stock + money levels
    """
    print(f"You have chosen {product.item_name}.")
    print(f"That will be {format_price(product.price)} please.")
    input("Please press enter to insert the money.")
    print(f"Dispensing {product.item_name}.")
    print("Thank you for using the vending machine today!")

    product.buy_item()
    update_product_in_worksheet(product)
    add_row_to_money_worksheet(product.price)

def manager_log_in():
    """
    This contains all of the wokflow for the stock manager, including stock/price updates and data analytics retrieval 
    """
    CORRECT_MANAGER_PASSCODE = "1234"
    passcode = input("Please enter passcode: ")
    if passcode != CORRECT_MANAGER_PASSCODE:
        print("That is incorrect. Returning to user screen")
        return False

    while True:
        print("\nWhat action would you like to perform?")
        print("0. Update stock")
        print("1. Update prices")
        print("2. Remove Money")
        print("3. View Sales Insights")
        print("4. Return to user screen")
        print("5. Power off")
        selection = input("Selection: ")

        if selection == "0":
            manager_update_stock()
        elif selection == "1":
            manager_update_prices()
        elif selection == "2":
            remove_money()
        elif selection == "3":
            view_analytics()
        elif selection == "4":
            return False
        elif selection == "5":
            return True
        else:
            print("That is not a valid selection, please try again.")

        input("Press enter to continue")

def manager_update_stock():
    """
    This gives the manager the ability to update the quantity column of all items in product
    """
    for product in all_products:
        print(f"There are currently {product.quantity} {product.item_name}")
        additions = 0
        while True:
            additions_input = input("How many would you like to add? ")
            try:
                additions = int(additions_input)
                product.quantity += additions
                update_product_in_worksheet(product)
                break
            except:
                print("That is not a valid input, please enter stock a whole number")

def manager_update_prices():
    """
    This gives the manager the ability to update the price column of all items in product
    """
    print("Updating prices")
    print("Press enter with no input to keep price the same.")
    print("Please enter the value in pence (e.g. if you want £1.20 then enter 120)")
    for product in all_products:
        print(f"{product.item_name} currently costs {format_price(product.price)}")
        new_price = 0
        while True:
            price_input = input("What would you like the new price to be? ")
            try:
                if (price_input == ""):
                    break
                new_price = int(price_input)
                product.price = new_price
                update_product_in_worksheet(product)
                break
            except:
                print("That is not a valid input, please enter the new price in pence as a whole number")

def remove_money():
    """
    This will give the manager the ability to take monry out of the machine, adding a row to the balance column of money table
    """
    print("Removing money")
    print("Please enter the value in pence (e.g. if you want £11.20 then enter 1120)")
    current_balance = get_current_balance()
    print(f"The current balance is {format_price(current_balance)}")

    while True:
        remove_input = input("How much would you like to remove? ")
        try:
            money_to_reduce = int(remove_input)
            if money_to_reduce < current_balance:
                add_row_to_money_worksheet(-money_to_reduce)
                break
            else:
                print("That is higher than the balance in the machine, please enter a lower amount.")
        except:
                print("That is not a valid input, please enter the new amount in pence as a whole number")
    
    print(f"Removed {format_price(money_to_reduce)}")
    print(f"New balance {format_price(get_current_balance())}")

def view_analytics():
    """
    This will give the manager the ability to view the analytics data tables
    """
    
    def view_analytics_summary():
        """
        This shows the user a summary of their highest/lowest sellers, their most/least profitable products and the products with low stock
        """
        most_profitable_product = all_products[0]
        for product in all_products:
            if product.income > most_profitable_product.income:
                most_profitable_product = product
        print(f"\nYour most profitable product is {most_profitable_product.item_name} making you {format_price(most_profitable_product.income)}")
        input("Press enter to continue")

        least_profitable_product = all_products[0]
        for product in all_products:
            if product.income < least_profitable_product.income:
                least_profitable_product = product
        print(f"\nYour least profitable product is {least_profitable_product.item_name} making you {format_price(least_profitable_product.income)}")
        input("Press enter to continue")

        highest_selling_product = all_products[0]
        for product in all_products:
            if product.sales > highest_selling_product.sales:
                highest_selling_product = product
        print(f"\nYour highest selling product is {highest_selling_product.item_name} with {highest_selling_product.sales} sales")
        input("Press enter to continue")

        lowest_selling_product = all_products[0]
        for product in all_products:
            if product.sales < lowest_selling_product.sales:
                lowest_selling_product = product
        print(f"\nYour lowest selling product is {lowest_selling_product.item_name} with {lowest_selling_product.sales} sales")
        input("Press enter to continue")

        print("")
        low_stocked = False
        for product in all_products:
            if (product.quantity == 0):
                low_stocked = True
                print(f"You have no stock on {product.item_name} consider refilling as soon as possible")
            elif product.quantity < 5:
                low_stocked = True
                print(f"You have low stock on {product.item_name} with only {product.quantity} currently in stock")
        if not low_stocked:
            print("There are no products with low stock")
        input("Press enter to continue")

        print(f"\nThe current balance is {format_price(get_current_balance())}")

    print("Do you want to see a summary of your sales/stock data?")
    if (input("(y/n): ").lower() == "y"):
        view_analytics_summary()

    # TODO show all data

def update_product_in_worksheet(product):
    """
    takes a Product object and updates the product worksheet so all the columns match
    """
    product_worksheet = SHEET.worksheet("product")
    row_number = product_worksheet.find(product.item_name).row

    col_number = product_worksheet.find("quantity").col
    product_worksheet.update_cell(row_number, col_number, str(product.quantity))

    col_number = product_worksheet.find("price").col
    product_worksheet.update_cell(row_number, col_number, str(product.price))

    col_number = product_worksheet.find("sales").col
    product_worksheet.update_cell(row_number, col_number, str(product.sales))

    col_number = product_worksheet.find("income").col
    product_worksheet.update_cell(row_number, col_number, str(product.income))

def add_row_to_money_worksheet(balance_increase):
    """
    Takes how much we want to increase the machine's balance by and adds a row to the money table with
    the balance increase added to the current balance (the bottom row of the money table)
    Note: this is ADDITION, to subtract from the balance, ensure balance_increase is negative
    """
    money_worksheet = SHEET.worksheet("money")

    current_balance = get_current_balance()
    new_balance = current_balance + balance_increase
    money_worksheet.append_row([str(current_balance + balance_increase)])

def get_current_balance():
    """
    Takes the last row of balance from the money table - this is the current balance of the vending machine
    """
    money_worksheet = SHEET.worksheet("money")
    last_row = len(money_worksheet.get_all_values())
    current_balance = money_worksheet.cell(last_row, 1).value
    return int(current_balance)

def main():
    """
    Run the vending machine workflow from power-up to shut-down
    """
    print("Starting Vending Machine. Welcome!")
    set_up_products()

    while True:
        should_power_off = get_user_input()
        if (should_power_off):
            break
    print("Vending Machine Powering Down. Goodbye!")

main()