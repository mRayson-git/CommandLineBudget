def delete(cursor):
    query = ("DELETE FROM transaction_t")
    cursor.execute(query)
    query = ("UPDATE account_t set account_balance = 0.00")
    cursor.execute(query)

def transInDatabase(trans, cursor):
    check = ("SELECT EXISTS (SELECT account_name, trans_amount, trans_date FROM transaction_t "
        "WHERE account_name = %s AND trans_amount = %s AND trans_date = %s)")
    check_data = (trans[0],trans[1],trans[2])
    cursor.execute(check, check_data)
    exists = cursor.fetchone()[0]
    return exists

def insertTransaction(trans, cursor):
    add_transaction = ("INSERT INTO transaction_t"
        "(account_name, trans_amount, trans_date, trans_payee, trans_desc, category_name)"
        " VALUES (%s, %s, %s, %s, %s, %s)")
    trans_data = (trans[0],trans[1],trans[2],trans[3],trans[4], trans[5])
    cursor.execute(add_transaction, trans_data)

def updateAccountBalance(accName, cursor):
    query = ("SELECT sum(trans_amount) FROM transaction_t WHERE account_name = %s")
    data = (accName,)
    cursor.execute(query, data)
    balance = cursor.fetchone()[0]
    query = ("UPDATE account_t SET account_balance = %s WHERE account_name = %s")
    data = (balance, accName)
    cursor.execute(query, data)

def getMonthAccountBalance(date, cursor):
    dataDate = date + "%"
    query = ("SELECT sum(trans_amount) FROM transaction_t WHERE trans_date LIKE %s")
    data = (dataDate,)
    cursor.execute(query, data)
    balance = cursor.fetchone()[0]
    if (balance == None):
        balance = 0.0
    return float(balance)

def categoryUpdate(cursor):
    query = ("SELECT DISTINCT trans_payee FROM transaction_t WHERE category_name = 'Unsorted'")
    cursor.execute(query)
    results = cursor.fetchall() #result should be [payee]
    fails = []
    for i in results:
        query = ("SELECT EXISTS (SELECT trans_payee FROM transaction_t WHERE trans_payee = %s AND category_name != 'Unsorted')")
        data = (i[0],)
        cursor.execute(query, data)
        exists = cursor.fetchone()[0]
        if (exists == 1):
            query = ("SELECT category_name FROM transaction_t WHERE trans_payee = %s AND category_name != 'Unsorted'")
            data = (i[0],)
            cursor.execute(query, data)
            catName = cursor.fetchone()[0]
            query = ("UPDATE transaction_t SET category_name = %s WHERE trans_payee = %s")
            data = (catName, i[0])
            cursor.execute(query,data)
            print("Auto detected the category name: " + catName + " for the payee: " + i[0])
        elif (exists == 0):
            fails.append(i)
    if (fails != []):
        print("Manual Intervention Needed for these transactions:")
        for i in fails:
            print("What is the category name for this payee? - " + str(i[0]))
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
            ans = -1
            while (ans < 0 or ans > 16):
                ans = int(input("Which category does the transaction fall into: "))
                print("{:~^43}".format(""))
                print()
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
            query = ("UPDATE transaction_t SET category_name = %s WHERE trans_payee = %s")
            data = (catDict[ans], i[0])
            cursor.execute(query, data)

    #bandaid fix for rent
    query = ("SELECT trans_id, trans_amount FROM transaction_t WHERE category_name LIKE '%Misc'")
    cursor.execute(query)
    results = cursor.fetchall()
    for i in results:
        if (float(i[1]) == -675):
            query = ("UPDATE transaction_t SET category_name = 'Monthly Expense: Rent' WHERE trans_id = %s")
            data = (i[0],)
            cursor.execute(query,data)
    query = ("SELECT trans_id, trans_amount FROM transaction_t WHERE category_name LIKE '%Rent'")
    cursor.execute(query)
    results = cursor.fetchall()
    for i in results:
        if (float(i[1]) != -675):
            query = ("UPDATE transaction_t SET category_name = 'Transfer: Misc' WHERE trans_id = %s")
            data = (i[0],)
            cursor.execute(query,data)
    

def listAllTrans(cursor):
    query = ("SELECT account_name, trans_amount, trans_date, trans_payee, category_name FROM transaction_t ORDER BY trans_date DESC")
    cursor.execute(query)
    trans = cursor.fetchall()
    print("A list of all transactions in the database")
    print("{:~^42}".format(""))
    for i in trans:
        print(str(i[0]) + " had a transaction of $" + str(i[1]) + " on " + str(i[2]) + " to " + str(i[3]) + " categorized as " + str(i[4]))

def getMonthTransactions(cursor, date):
    dataDate = date + "%"
    query = ("SELECT account_name, trans_amount, trans_date, trans_payee, category_name FROM transaction_t WHERE trans_date LIKE %s")
    data = (dataDate,)
    cursor.execute(query, data)
    trans = cursor.fetchall()
    return trans

def setMonthBudgetData(cursor, values, date):
    dataDate = date + "%"
    cats = ["Monthly Expense: Rent","Monthly Expense: Hydro","Monthly Expense: Internet","Everyday Expense: Groceries","Everyday Expense: Gas","Everyday Expense: Eating Out","Misc Expense: Clothes","Misc Expense: Entertainment","Misc Expense: Repair/Home"]
    for i in range(len(cats)):
        query = ("UPDATE category_t SET category_budget = %s where category_name = %s AND category_time LIKE %s")
        data = (values[i],cats[i],dataDate)
        cursor.execute(query,data)

def setSingleBudget(cursor, cat, budg, date):
    dataDate = date + "%"
    query = ("UPDATE category_t SET category_budget = %s WHERE category_name = %s AND category_time LIKE %s")
    data = (budg, cat, dataDate)
    cursor.execute(query, data)

def getActivity(cursor, cat, date):
    dataDate = date + "%"
    query = ("SELECT sum(trans_amount) FROM transaction_t WHERE category_name = %s AND trans_date LIKE %s")
    data = (cat, dataDate)
    cursor.execute(query,data)
    activity = cursor.fetchone()[0]
    if (activity == None):
        activity = 0.00
    return activity

def budgetExists(cursor, date):
    dataDate = date + "%"
    query = ("SELECT EXISTS (SELECT category_time FROM category_t WHERE category_time LIKE %s)")
    data = (dataDate,)
    cursor.execute(query,data)
    exists = cursor.fetchone()[0]
    return exists

def isBudgetNull(cursor, date):
    dataDate = date + "%"
    query = ("SELECT category_budget FROM category_t WHERE category_time LIKE %s")
    data = (dataDate,)
    cursor.execute(query,data)
    vals = cursor.fetchall()
    print(vals)
    allNull = True
    for i in vals:
        if (i[0] != 0.00):
            allNull = False
    return allNull

def readBudgetValues(cursor, cat, date):
    dataDate = date + "%"
    vals = []
    values = []
    for i in cat:
        query = ("SELECT category_budget FROM category_t WHERE category_name = %s AND category_time LIKE %s")
        data = (i, dataDate)
        cursor.execute(query, data)
        vals.append(cursor.fetchone()[0])
    for i in vals:
        values.append(i)
    return values

def createBlankBudget(cursor, date):
    dataDate = date + "-01"
    print("Categories for this month havnt been created yet, inserting...")
    query = ("insert into category_t(category_name, category_time) values('Unsorted', %s)")
    data = (dataDate,)
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Monthly Expense: Rent', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Monthly Expense: Hydro', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Monthly Expense: Internet', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Everyday Expense: Groceries', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Everyday Expense: Gas', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Everyday Expense: Eating Out', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Misc Expense: Clothes', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Misc Expense: Entertainment', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Misc Expense: Bills', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Misc Expense: Repair/Home', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Misc Expense: School', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Transfer: Savings', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Transfer: Misc', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Income: Work', %s)")
    cursor.execute(query, data)
    query = ("insert into category_t(category_name, category_time) values('Income: Misc', %s)")
    cursor.execute(query, data)

def getAccountBalance(cursor):
    query = ("SELECT account_balance from account_t where account_name = 'ScotiaChecking'")
    cursor.execute(query)
    return float(cursor.fetchone()[0])