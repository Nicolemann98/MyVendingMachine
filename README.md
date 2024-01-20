# My Vending Machine


## Plan
Before starting, I have created a short plan to help guide me through this project
![Plan](assets/images/VendingMachinePlan.png)

## Important notes
The passcode for the stock manager is `1234`, Usually this would require encryption but this is out of scope for this project so will hard-code the passcode


## Credits

Leading zeros: https://stackoverflow.com/questions/733454/best-way-to-format-integer-as-string-with-leading-zeros
gspread documentation: https://docs.gspread.org/en/latest/user-guide.html

## Struggles

Issues with updating cells (rather than just adding new rows), found solution in gspread documentation (linked in credits)
Part way through the commit for adding the salses insights, I realised that I didn't need a separate sales table as I could just add this data to the existing product table