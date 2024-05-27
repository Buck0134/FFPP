from csv import Error
import pandas as pd
from datetime import date

#import Card_n_Transcarions.py

# Global Var
Statement_Summary = "Empty_Message"

# Loading the base-data excel

class Transaction:
    def __init__(self, Date, Expanse, Amount, Paid_by, Card, Billed_to):
        self.date = Date
        self.expanse = Expanse
        self.amount = Amount
        self.Paid_by = Paid_by
        self.Card = Card
        self.Billed_to = Billed_to

#class Card:
#    def __init__(self, Name, Transactions):
#        self.Name =


# Read the excel file
df = pd.read_excel('Statements/Expanse_DataBase.xlsx')

# Convert each row in the DataFrame to a Transaction object, and store all the objects in a list
transactions = [Transaction(row['date'], row['Expanse'], row['amount'],row['Paid By'], row['Card'], row['Billed_To']) for index, row in df.iterrows()]

def Add_Transction(new_df):
    user_input_who = input("Please tell us who is paying this transcation\n");
    user_input_card = input("Please tell us which card is this?\n")
    ## DO LATER create card object with a overall card list
    New_transactions = [Transaction(row['Date'], row['Description'], row['Amount'],user_input_who, user_input_card, "Unknown") for index, row in new_df.iterrows()]
    transactions.extend(New_transactions)
    print("Transcation Added")

def recoginze_Transcations():
    # Add in the option where there is no unsettled transcations
    for transaction in transactions:
        if(transaction.Billed_to == "Unknown"):
            while True:
                print(f"Date: {transaction.date}, Expanse: {transaction.expanse}, Amount: {transaction.amount}, Paid_by: {transaction.Paid_by}, Card: {transaction.Card}, Billed_To: {transaction.Billed_to}\n")
                user_input_bill_to = input("Please enter who is repsonsible for this transcation.\nYou can choose from\n 0: Both\t1: Bucky\t2: Charlie\t3:Payment\t4:Other(Manual Input)\nPlease Enter U for keeping the current transaction under unknown\nEnter *B to exit the current function\n")
                if(user_input_bill_to == "U"):
                    break
                # DONE: add a break code: when user inpit a certain value, break the current loop and go back to the main menu.
                elif(user_input_bill_to == "*B"):
                    return
                elif(user_input_bill_to == "0" or user_input_bill_to == "1" or user_input_bill_to == "2"or user_input_bill_to == "3"or user_input_bill_to == "4"):
                    if(user_input_bill_to == "0" ):
                        transaction.Billed_to = "Both";
                    elif(user_input_bill_to == "1" ):
                        transaction.Billed_to = "Bucky";
                    elif(user_input_bill_to == "2" ):
                        transaction.Billed_to = "Charlie";
                    elif(user_input_bill_to == "3" ):
                        transaction.Billed_to = "Payment";
                    elif(user_input_bill_to == "4"):
                        user_input_other_billed_to = input("Please manually type in the transcation billed_to information.\n")
                        user_input_other_billed_to = "Other_" + user_input_other_billed_to
                        transaction.Billed_to = user_input_other_billed_to
                    print("\n")
                    print("Logged.. Next Transcation\n")
                    break
                else:
                    print("Please choose from the options below:")
                    

def email_summary(Statement_Summary):
    import smtplib

    # Set the SMTP server and port
    smtp_server = 'smtp.gmail.com'
    port = 587  # For starttls

    # Sender and receiver
    sender_email = 'bucky.yu.chenkai@gmail.com'
    receiver_emails = ['charlieji99@icloud.com', 'gradbucky22@gmail.com']  # List of receivers

    password = "lyuhrlkbmxrddmgn"

    # Email body
    subject = "Automatic Message from Faimly Finance Processing Program(FFPPVenv)\n"
    body = "This email was sent from Faimly Finance Processing Program(FFPPVenv). An update on the balance has been made:\n\n" + Statement_Summary
    message = f'Subject: {subject}\n\n{body}'
    
    # Create a secure SSL context
    context = smtplib.SMTP(smtp_server, port)

    try:
        # Identify yourself to the server
        context.ehlo()
        # Start encryption
        context.starttls()
        # Login to the server
        context.login(sender_email, password)
        # Send the email
        # Send the email to each recipient
        for receiver_email in receiver_emails:
            context.sendmail(sender_email, receiver_email, message)
    finally:
        # Close the connection
        context.quit()

def save_total():
    print("Saving Changes")
    # Create a list of dictionaries from the transactions
    data = [{'date': t.date, 'Expanse': t.expanse, 'amount': t.amount, 'Paid By': t.Paid_by, 'Card': t.Card, 'Billed_To':t.Billed_to} for t in transactions]
    # Create a DataFrame from the list of dictionaries
    df_save = pd.DataFrame(data)
    print(df_save)
    df_save.to_excel('Expanse_DataBase.xlsx', index=False)

def summary():
    # print("Please select a time frame")
    BuckyTotal = 0
    BuckyOwe = 0
#    BuckyPaid = 0
    CharlieTotal = 0
    CharlieOwe = 0
#    CharliePaid = 0
    for transaction in transactions:
        if(transaction.Billed_to == "Bucky" or transaction.Billed_to == "Chenkai Yu"):
            BuckyTotal += transaction.amount
            if(transaction.Paid_by == "Charlie"):
                BuckyOwe += transaction.amount
        elif(transaction.Billed_to == "Charlie" or transaction.Billed_to == "Jiayi Ji"):
            CharlieTotal += transaction.amount
            if(transaction.Paid_by == "Bucky"):
                CharlieOwe += transaction.amount
        elif(transaction.Billed_to == "Both"):
            BuckyTotal += (transaction.amount)/2
            CharlieTotal += (transaction.amount)/2
            if(transaction.Paid_by == "Bucky"):
                CharlieOwe += transaction.amount/2
            if(transaction.Paid_by == "Charlie"):
                BuckyOwe += transaction.amount/2
    print(f"In the selected tiemframe, Charlie has spent: {CharlieTotal}")
    print(f"In the selected tiemframe, Bucky has spent: {BuckyTotal}")
    print(f"In the selected tiemframe, Charlie has to pay Bucky: {CharlieOwe}")
    print(f"In the selected tiemframe, Bucky has to pay Charlie: {BuckyOwe}")
#    printf("Do you wish to view payment summary?"):
#   To do: ask the user if he wants to view payment summary or spending summary
#   Time to fuss with the dataframe~
#    print(f"In the selected tiemframe, Bucky has paid: {BuckyPaid}")
#    print(f"In the selected tiemframe, Charlie has paid: {CharliePaid}")
    dif = CharlieOwe - BuckyOwe
    print(f"The difference is: {dif}")
    message = "In the selected tiemframe, \nCharlie has spent:\t\t" + str(CharlieTotal) + "\nBucky has spent:\t\t" + str(BuckyTotal) + "\nSo Far, Charlie has to pay Bucky:\t\t" + str(CharlieOwe) + "\nSo Far, Bucky has to pay Charlie:\t\t" + str(BuckyOwe)+ "\nThe Balance Difference is:\t\t"+ str(dif)
    return message

    

while True:
    # Read input from the user
    print("\nMain Menu\n");
    print("1. Add a new transcation excel\n");
    print("2. Recoginze Transcations\n");
    print("3. Print Summary\n");
    print("4. Save\n");
    user_input = input("Please choose from the Above options: \n")
    
    try:
        # Attempt to convert the input to an integer
        num = int(user_input)
        # Print the user's input
        if(num>= -1 and num<=5):
            print("You entered the number: " + str(num))
            # If the conversion was successful, break out of the loop
            if(num == 1):
                print("You are trying to add a new transcation excel\n")
                user_input_1 = input("Please enter the name of the new excel\n")
                user_input_1 = "Statements/" + user_input_1 + '.xlsx'
                try:
                    df_1 = pd.read_excel(user_input_1)
                    Add_Transction(df_1)
                except FileNotFoundError:
                    # If an input error occurs, print an error message
                    print("Error: Excel Missing. Please check excel name.")
            elif(num == 2):
                print("You are trying to regonzie transcations\n");
                recoginze_Transcations()
            elif(num == 3):
                print("Printing Summary")
                Statement_Summary = summary()
            elif(num == 4):
                save_total()
                if(Statement_Summary == "Empty_Message"):
                    print("\nEmail not sent, no Statment_Summary Information")
                else:
                    email_summary(Statement_Summary)
            elif(num == 0):
                print("Printing out all data points")
                for transaction in transactions:
                    print(f"Date: {transaction.date}, Expanse: {transaction.expanse}, Amount: {transaction.amount}, Paid_by: {transaction.Paid_by}, Card: {transaction.Card}, Billed_To: {transaction.Billed_to}\n")
            # Back Door Menu:
            elif(num == -1):
                while True:
                
                    print("\nBack Door Menu:")
                    user_input_num_1 = input("Please choose from the following:\n0:View Transcation labeled manually\n1: View Negative_Valued Transcation\n")
                    num_1 = int(user_input_num_1)
                    if(num_1>=0 and num_1<=1):
                        if(num_1 == 0):
                            print("\nShowing transcation labeled as other:")
                            for transaction in transactions:
                                target = transaction.Billed_to.split("_")[0]
                                if(target == "Other"):
                                    print(f"Date: {transaction.date}, Expanse: {transaction.expanse}, Amount: {transaction.amount}, Paid_by: {transaction.Paid_by}, Card: {transaction.Card}, Billed_To: {transaction.Billed_to}\n")
                            break;
                    else:
                        print("Please choose from the Options stated")
                
        else:
            print("Please choose from the 1 to 5")
    except ValueError:
        # If a ValueError occurs, print an error message
        print("Error: You did not enter a valid number. Please try again.")


