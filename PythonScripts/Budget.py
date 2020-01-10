from SQLQueries import getActivity, readBudgetValues, isBudgetNull, setMonthBudgetData, budgetExists, createBlankBudget, getAccountBalance, getMonthAccountBalance, setSingleBudget
from UsefulFunctions import clear

def setMonthBudgetValues(cursor, date):
    exists = budgetExists(cursor, date)
    if (exists == False):
        createBlankBudget(cursor, date)
    isNull = isBudgetNull(cursor, date)
    if (isNull == True):
        vals = []
        print("\nPlease enter values for the months budget")
        vals.append(input("Monthly Expense: Rent -> "))
        vals.append(input("Monthly Expense: Hydro -> "))
        vals.append(input("Monthly Expense: Internet -> "))
        vals.append(input("Everyday Expense: Groceries -> "))
        vals.append(input("Everyday Expense: Gas -> "))
        vals.append(input("Everyday Expense: Eating Out -> "))
        vals.append(input("Misc Expense: Clothes -> "))
        vals.append(input("Misc Expense: Entertainment -> "))
        vals.append(input("Misc Expense: Repair/Home -> "))
        setMonthBudgetData(cursor, vals, date)
    elif (isNull == False):
        flag = True
        while (flag == True):
            clear()
            print("Categories available to be changed: ")
            print("\n0-Unsorted")
            print("1-Monthly Expense: Rent")
            print("2-Monthly Expense: Hydro")
            print("3-Monthly Expense: Internet")
            print("4-Everyday Expense: Groceries")
            print("5-Everyday Expense: Gas")
            print("6-Everyday Expense: Eating Out")
            print("7-Misc Expense: Clothes")
            print("8-Misc Expense: Entertainment")
            print("9-Misc Expense: Bills")
            print("10-Misc Expense: Repair/Home")
            print("11-Misc Expense: School")
            print("12-Transfer: Savings")
            print("13-Transfer: Misc")
            print("14-Income: Work")
            print("15-Income: Misc\n")
            ans = input("Please enter your choice: ")
            while (ans.isnumeric() == False or int(ans) < 0 or int(ans) > 15):
                ans = input("\nPlease enter your choice: ")
            catDict = {
                0:"Unsorted",
                1:"Monthly Expense: Rent",
                2:"Monthly Expense: Hydro",
                3:"Monthly Expense: Internet",
                4:"Everyday Expense: Groceries",
                5:"Everyday Expense: Gas",
                6:"Everyday Expense: Eating Out",
                7:"Misc Expense: Clothes",
                8:"Misc Expense: Entertainment",
                9:"Misc Expense: Bills",
                10:"Misc Expense: Repair/Home",
                11:"Misc Expense: School",
                12:"Transfer: Savings",
                13:"Transfer: Misc",
                14:"Income: Work",
                15:"Income: Misc"
            }
            cat = catDict[int(ans)]
            budg = input("Buget Value: " )
            while (budg.isnumeric() == False):
                ans = input("\nBudget Value: ")
            setSingleBudget(cursor, cat, budg, date)
            choice = input("\nEnter 1 to set more, else another number: ")
            while (choice.isnumeric() == False):
                choice = input("\nEnter 1 to set more, else another number: ")
            if (int(choice) == 1):
                flag = True
            else:
                flag = False

def showBudget(cursor, date):
    '''Retrieves the budget for the given month. If none exists, creates one.'''
    exists = budgetExists(cursor, date)
    if (exists == False):
        createBlankBudget(cursor, date)
    budgetCategories = ["Monthly Expense: Rent","Everyday Expense: Groceries","Everyday Expense: Gas","Everyday Expense: Eating Out","Misc Expense: Clothes","Misc Expense: Entertainment","Misc Expense: Repair/Home"]
    budgetedValues = readBudgetValues(cursor, budgetCategories, date)
    activity = []
    for i in budgetCategories:
        activity.append(getActivity(cursor, i, date))
    remaining = []
    for i in range(len(budgetCategories)):
        remaining.append(float(budgetedValues[i]) + float(activity[i]))
    
    totalBudgeted = 0.00
    for i in budgetedValues:
        totalBudgeted = totalBudgeted + float(i)
    totalActivity = 0.00
    for i in activity:
        totalActivity = totalActivity + float(i)
    totalRemaining = 0.00
    for i in remaining:
        totalRemaining = totalRemaining + i
    
    if (totalRemaining >= 0):
        needHome = getAccountBalance(cursor) - totalRemaining


    #Display the table
    clear()
    print("\n{:^83}".format("The " + date + " budget"))
    print("{:<16} {:>9.2f}".format("Account Balance:", getAccountBalance(cursor)))
    if (totalRemaining > 0):
        print("{:<16} {:>9.2f}".format("To Be Budgeted:", needHome))
    else:
        print("{:<16} {:>9.2f}".format("Missing Funds:", totalRemaining))
    print("{:-^83}".format(""))
    print("|{:^30}|{:^16}|{:^16}|{:^16}|".format("Category","Budgeted ($)","Activity ($)","Remaining ($)"))
    print("{:-^83}".format(""))
    for i in range(len(budgetCategories)):
        print("|{:<30}|{:>16}|{:>16.2f}|{:>16.2f}|".format(budgetCategories[i], budgetedValues[i], activity[i], float(budgetedValues[i])+float(activity[i])))
    print("{:-^83}".format(""))
    print("|{:<30}|{:>16.2f}|{:>16.2f}|{:>16.2f}|".format("Totals",totalBudgeted,totalActivity, totalRemaining))
    print("{:-^83}".format(""))
    if (totalRemaining > 0):
        print("*{:<47}{:<6.2f}\n".format("Recommended you put the following in savings next month, $", totalRemaining))



