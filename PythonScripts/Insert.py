import os
import csv
import datetime
from SQLQueries import transInDatabase, insertTransaction, updateAccountBalance, categoryUpdate
from UsefulFunctions import loadFile, getToday


def getTransactions(fileName, cursor, cnx):
    '''Checks if given file exists and commits the transactions to the DB'''
    date = loadFile()
    lastRun = (date["lastRun"])
    if os.path.exists(fileName):
        if (fileName == "pcbanking.csv"):
            print("Inserting the ScotiaBank transactions")
            accountName = "ScotiaChecking"
        elif (fileName == "report.csv"):
            print("Inserting the PCFinancial transactions")
            accountName = "PCFinancial"
        transactions = parse(fileName, accountName)
        insert(transactions, cursor, lastRun, cnx, accountName)
    else:
        print("The file does not exist")

def insert(transactions, cursor, lastRun, cnx, accountName):
    '''Runs the SQL code to insert the data'''
    #A transaction is [accountName, amount, date, payee, description, category]
    insertAnom = 0
    properInsert = 0
    for trans in transactions:
        #check if new from last run
        lastDate = datetime.datetime.strptime(lastRun,'%Y-%m-%d').date()
        currDate = datetime.datetime.strptime(getToday(),'%Y-%m-%d').date()
        check = transInDatabase(trans, cursor)
        if (check == 1 or trans[2] > currDate):
            if (trans[2] < lastDate):
                #print("The transaction: " + str(trans) + " has already been added since the last run, skipping...")
                insertAnom = insertAnom + 1
            elif (trans[2] > currDate):
                print("PCFinancial Fucked Up with: " + str(trans))
            else:
                ans = input("The transaction: " + str(trans) + " already exists, would you like to add anyways? (y/n): ")
                insertAnom = insertAnom + 1
                if (ans == 'y'):
                    insertTransaction(trans, cursor)
                    updateAccountBalance(trans, cursor)
                else:
                    print("Skipping")
        else:
            insertTransaction(trans, cursor)
            properInsert = properInsert + 1
    updateAccountBalance(accountName, cursor)
    print("There were a total of " + str(properInsert+insertAnom) + " transactions")
    print("There were a total of " + str(insertAnom) + " insertion anomalies")
    cnx.commit()
    categoryUpdate(cursor)
    cnx.commit()

#CSV Parser
def parse(fileName, accountName):
    '''Returns the transactions from a CSV file'''
    all_transactions = []
    file = open(fileName)
    reader = csv.reader(file)
    header = hasHeader(file)
    if (header == False):
        file.seek(0)
    for row in reader:
        all_transactions.append(createTransaction(row, accountName))
    file.close()
    return all_transactions

def createTransaction(row, accountName):
    '''Creates a unified (depending on which csv it's given) "transaction" to send to the database.
        A transaction is [accountName, amount, date, payee, description, category_name]'''
    trans = [accountName]

    if (accountName == "ScotiaChecking"):
        #Builds the transactions
        row[0] = fixDate(row[0]) #date
        row[0] = datetime.datetime.strptime(row[0],'%Y-%m-%d').date()
        row[1] = float(row[1]) #amount
        row[4] = cleanString(row[4]) #payee
        row[3] = cleanString(row[3]) #description

        trans.append(row[1])
        trans.append(row[0])
        if (row[1] < 0):
            trans.append(row[4])
            trans.append(row[3])
        else:
            trans.append(row[4])
            trans.append(row[3])
        trans.append("Unsorted")

    elif (accountName == "PCFinancial"):
        #Builds the transactions
        row[3] = fixDate(row[3]) #date
        row[3] = datetime.datetime.strptime(row[3],'%Y-%m-%d').date()
        row[5] = fixSign(float(row[5])) #flips sign of amount
        row[0] = cleanString(row[0]) #payee
        row[1] = cleanString(row[1]) #description

        trans.append(row[5])
        trans.append(row[3])
        if (row[5] < 0):
            trans.append(row[0])
            trans.append(row[1])
        else:
            trans.append(row[0])
            trans.append(row[1])
        trans.append("Unsorted")
    return trans

def fixDate(date):
    '''Changes the date to the proper format'''
    oldDate = date.split("/")
    fixedDate = oldDate[2] + "-" + oldDate[0] + "-" + oldDate[1]
    return fixedDate

def fixSign(amount):
    return amount*-1

def hasHeader(file):
    '''Checks to see if there is a number value within the first row of the file'''
    flag = True
    row = file.readline()
    for i in row:
        try:
            float(i)
            flag = False
        except ValueError:
            pass
    return flag

def cleanString(messy):
    '''Cleans the output of the string, removing blank spaces'''
    clean = ""
    for i in range(len(messy)):
        if (messy[i] == " " and messy[i+1] == " "):
            return clean
        else:
            clean = clean + messy[i]
    return clean
