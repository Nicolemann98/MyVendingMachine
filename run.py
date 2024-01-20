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

product = SHEET.worksheet("product")

product_data = product.get_all_values()

def get_user_input():
    print("Welcome to the Vending Machine, what would you like today?")
    # The items and stock manager login will go here
    print("--------------------------------------------------")
    return True


def main():
    """
    Run the vending machine workflow
    """
    print("Starting Vending Machine. Welcome!")
    while True:
        should_quit = get_user_input()
        if (should_quit):
            break
    print("Vending Machine Powering Down. Goodbye!")


main()