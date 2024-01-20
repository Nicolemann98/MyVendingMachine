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

product_worksheet = SHEET.worksheet("product")

all_products = []

class Product():
    """
    Creates instance of Product
    """
    def __init__(self, item_name, quantity, price):
        self.item_name = item_name
        self.quantity = quantity
        self.price = price

    def get_product_text(self):
        """
        Takes the product object and shows in a user readable format for the menu screen
        """
        return f"{self.item_name} - {self.format_price()}"

    def format_price(self):
        """
        Takes the price from a number in pence (e.g. 124) and returns it in standard price format (e.g. £1.24)
        """
        length = len(self.price)
        pounds = self.price[:length-2]
        if (pounds == ""):
            pounds = "0"
        pence = self.price[length-2:]
        return f"£{pounds}.{pence}"


def set_up_products():
    """
    Takes the data from the product spreadsheet, creates a Product object for each row and adds to the all_products list
    """
    for product_unformatted in product_worksheet.get_all_values():
        product = Product(product_unformatted[0], product_unformatted[1], product_unformatted[2])
        all_products.append(product)

def get_user_input():
    """
    Displays the welcome screen and asks the user for their item
    """
    print("Welcome to the Vending Machine, what would you like today?")
    # The items and stock manager login will go here
    for i in range(1, len(all_products)):
        product = all_products[i]
        print(f"{i}: {product.get_product_text()}")
    return True


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