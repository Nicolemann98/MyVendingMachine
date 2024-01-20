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
    Creates instance of Product
    """
    def __init__(self, item_name, quantity, price):
        self.item_name = item_name
        self.quantity = int(quantity)
        self.price = int(price)

    def get_product_text(self):
        """
        Takes the product object and shows in a user readable format for the menu screen, also lets user know if item is out of stock
        """
        if (self.is_item_in_stock()):
            return f"{self.item_name} - {self.format_price()} - {self.quantity} in stock"
        else:
            return f"{self.item_name} - OUT OF STOCK"

    def format_price(self):
        """
        Takes the price from a number in pence (e.g. 124) and returns it in standard price format (e.g. £1.24)
        """
        pounds = self.price // 100
        pence = self.price % 100
        
        return f"£{pounds}.{str(pence).zfill(2)}"

    def is_item_in_stock(self):
        return self.quantity != 0


def set_up_products():
    """
    Takes the data from the product spreadsheet, creates a Product object for each row and adds to the all_products list
    """
    product_worksheet = SHEET.worksheet("product")
    for product_unformatted in product_worksheet.get_all_values()[1:]:
        product = Product(product_unformatted[0], product_unformatted[1], product_unformatted[2])
        all_products.append(product)

def get_user_input():
    """
    Displays the welcome screen and asks the user for their item
    """
    print("Welcome to the Vending Machine")
    input("Please press enter to start")
    print("What would you like today?")
    print(f"Please enter a number between 0 and {len(all_products)} to choose your selection")
    for i in range(len(all_products)):
        product = all_products[i]
        print(f"{i}: {product.get_product_text()}")
        # TODO rename this to stock manager and put shut down inside there
    print(f"{len(all_products)}: Shut down")

    is_selection_valid = False
    while not is_selection_valid:
        selection = input("Selection: ")
        is_selection_valid = validate_selection(selection)

    selection_number = int(selection)

    if selection_number == len(all_products):
        # TODO stock manager workflow
        return True
    else:
        chosen_product = all_products[selection_number]
        dispense_item(chosen_product, selection_number)
        return False

def dispense_item(product, selection_number):
    """
    This asks for the user's money, "dispenses" the item and adjusts the stock + money levels
    """
    print(f"You have chosen {product.item_name}")
    print(f"That will be {product.format_price()} please")
    input("Please press enter to insert the money")
    print(f"Dispensing {product.item_name}")
    print("Thank you for using the vending machine today!")

    new_quantity = product.quantity - 1
    product.quantity = new_quantity

    product_worksheet = SHEET.worksheet("product")
    product_worksheet.update_cell(selection_number + 2, PRODUCT_QUANTITY_CELL_NUMBER, str(new_quantity))


def validate_selection(selection):
    """
    Takes the user's selection input and checks that it is both a valid input and that the chosen item is in stock.
    Returns True if the input is valid and False if it is invalid
    """
    if selection == str(len(all_products)):
        #  this is for the shut down selection option
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

def main():
    """
    Run the vending machine workflow from power-up to shut-down
    """
    print("Starting Vending Machine. Welcome!")
    set_up_products()

    while True:
        should_quit = get_user_input()
        if (should_quit):
            break
    print("Vending Machine Powering Down. Goodbye!")


main()