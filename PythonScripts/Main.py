from Insert import getTransactions
from Budget import showBudget, setMonthBudgetValues
from SQLQueries import listAllTrans
from UsefulFunctions import configDateUpdate, getLastMonth, getThisMonth, clear
from RetrieveReport import webScraper, moveFiles
import getpass
import mysql.connector
from Collect import collect, readsaved

def main():
    '''Establishes a connection with the database and directs user to where they want to go'''
    try:
        clear()
        dbUser = input("Please enter your database username: ")
        dbPass = getpass.getpass("Password: ")
        cnx = mysql.connector.connect(host='localhost',database='Budget',user=dbUser,password=dbPass)
        cursor = cnx.cursor(buffered=True)
        mainMenu(cursor, cnx)
        configDateUpdate()

    except (Exception, mysql.connector.Error) as err:
            print("Error while connecting to the database", err)
    finally:
        if (cnx):
            cursor.close()
            cnx.close()
            print("Connection closed")

def mainMenu(cursor, cnx):
    clear()
    flag = 1
    print("{:~^60}".format(""))
    print("{:^60}".format("Budget Bananza v1.0"))
    print("{:^60}".format("Author: Michael Rayson"))
    print("{:~^60}".format(""))
    input("{:^60}".format("\nPress enter to continue..."))
    
    while (flag == 1):
        #clear()
        print("Main Menu")
        print("{:~^43}".format(""))
        print("1) BudgetView Menu")
        print("2) Transaction Management Menu")
        print("{:~^43}".format(""))
        ans = input("\nPlease enter your choice: ")
        while (ans.isnumeric() == False or int(ans) < 1 or int(ans) > 2):
            ans = input("\nPlease enter your choice: ")
        if (int(ans) == 1):
            budgetMenu(cursor, cnx)
        elif (int(ans) == 2):
            transactionMenu(cursor, cnx)
        
        choice = input("Enter 1 to return to the main menu, otherwise another number to quit: ")
        while (choice.isnumeric() == False):
            choice = input("\nEnter 1 to return to the main menu, otherwise another number to quit: ")
        if (int(choice) == 1):
            flag = 1
        else:
            flag = 2
        

def budgetMenu(cursor,cnx):
    clear()
    print("Budget Menu")
    print("{:~^43}".format(""))
    print("1) Check Month Progression")
    print("2) Set budget values")
    print("{:~^43}".format(""))
    ans = input("\nPlease enter your choice: ")
    while (ans.isnumeric() == False or int(ans) < 1 or int(ans) > 2):
        ans = input("\nPlease enter your choice: ")
    if (int(ans) == 1):
        clear()
        print("Budget Menu 1.1")
        print("{:~^43}".format(""))
        print("1) Current Month")
        print("2) Last Month")
        print("{:~^43}".format(""))
        ans = input("\nPlease enter your choice: ")
        while (ans.isnumeric() == False or int(ans) < 1 or int(ans) > 2):
            ans = input("\nPlease enter your choice: ")
        clear()
        if (int(ans) == 1):
            showBudget(cursor, getThisMonth())
        elif(int(ans) == 2):
            showBudget(cursor, getLastMonth())
    elif (int(ans) == 2):
        clear()
        print("Budget Menu 1.2")
        print("{:~^43}".format(""))
        print("1) Current Month")
        print("2) Last Month")
        print("{:~^43}".format(""))
        ans = input("\nPlease enter your choice: ")
        while (ans.isnumeric() == False or int(ans) < 1 or int(ans) > 2):
            ans = input("\nPlease enter your choice: ")
        if (int(ans) == 1):
            setMonthBudgetValues(cursor, getThisMonth())
        elif(int(ans) == 2):
            setMonthBudgetValues(cursor, getLastMonth())
    cnx.commit()
    
def transactionMenu(cursor, cnx):
    clear()
    print("Transaction Menu")
    print("{:~^43}".format(""))
    print("1) Retrieve and Import Transactions from CSV files")
    print("2) List all transactions in the database")
    print("{:~^43}".format(""))
    ans = input("\nPlease enter your choice: ")
    while (ans.isnumeric() == False or int(ans) < 1 or int(ans) > 2):
        ans = input("\nPlease enter your choice: ")
    if (int(ans) == 1):
        password1 = getpass.getpass("Please enter scotiabank password: ")
        password2 = getpass.getpass("Please enter pcfinancial password: ")
        webScraper(password1, password2)
        moveFiles()
        getTransactions("pcbanking.csv", cursor, cnx)
        getTransactions("report.csv", cursor, cnx)
    if (int(ans) == 2):
        listAllTrans(cursor)

main()
