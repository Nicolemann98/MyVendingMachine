# My Vending Machine


## Plan
Before starting, I have created a short plan to help guide me through this project
![Plan](assets/images/VendingMachinePlan.png)

## Important notes
The passcode for the stock manager is `1234`, Usually this would require encryption but this is out of scope for this project so will hard-code the passcode

## Testing
I have set up the product and money tables in this way before testing.
product table: 
![product_table](assets/images/ProductTable.png)
money table:
![money_table](assets/images/MoneyTable.png)

When running the code for the first time (after pressing enter to continue), the user is asked which product they are wanting to buy.
![selection_screen](assets/images/SelectionScreen.png)
If the user provides an invalid input, then they are prompted to give another input. Examples of invalid inputs include, letters instead of numbers
![invalid_selection_letters](assets/images/InvalidSelectionNotNumber.png)
Number that is not shown in the list of selections
![invalid_selection_high_number](assets/images/InvalidSelectionHighNumber.png)
And in addition, any item that is out of stock
![invalid_selection_out_of_stock](assets/images/InvalidSelectionOutOfStock.png)

Howver, if instead, the user does give a valid input then it asks the user for money, the user presses enter as a proxy for paying, then it dispenses the item and goes back to the selection menu for the next user
![valid_selection](assets/images/ValidSelection.png)
Once this happens, the product table is updated to decrease the stock by 1, increase the sales by 1 and increase the income by the product's price
![product_table_after_selection](assets/images/ProductTableAfterSelection.png)
And a new row gets added to the money table with the current balance (calculated as the previous balance + the price of the bought product)
![money_table_after_selection](assets/images/MoneyTableAfterSelection.png)




## Credits

Leading zeros: https://stackoverflow.com/questions/733454/best-way-to-format-integer-as-string-with-leading-zeros
gspread documentation: https://docs.gspread.org/en/latest/user-guide.html

## Struggles

Creating the initial data structure, in the end I created a class for my Product table that contains a class variable for each of the columns in the table. ANd then a variable that was a list of Product objects where each item of the list is a row in the table. This did bring challenges to the initial stages of writing the code because there was a lot of setting up that needed to be done and with a lot of though to exactly the best way to organise everything, however in the end, using object oriented programming it up allowed a lot of flexibility so that I could see all of the products to be able to access and update anything I needed fairly easily especially in the sales insights section of the project.

Issues with updating cells, in the example project we only had to add new rows to the bottom of tables, however I needed to modify records directly and did not know how to do this. Thankfully after some web searching, I found the solution to my problem in the gspread documentation (linked in credits)

Part way through the commit for adding the salses insights, I realised that I didn't need a separate sales table as I could just add this data to the existing product table. This did mean adjusting the Product class, however with the way I set up the objects, this actually ended up being simpler than initially thought