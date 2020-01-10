import os
def collect(cursor):
    query = ("SELECT * FROM TRANSACTION_T")
    cursor.execute(query)
    transactions = cursor.fetchall()
    fixedTrans = []
    for i in transactions:
        fixedTran = [i[0], i[1], float(i[2]), str(i[3]), i[4], i[5], i[6], i[7]]
        fixedTrans.append(fixedTran)


    file = open(r"AllTrans","w")
    for i in fixedTrans:
        i = str(i)
        i = i.replace('[', '')
        i = i.replace(']', '')
        file.write(i)
        file.write("\n")

def readsaved(cursor):
    file = open(r"AllTrans","r")
    for line in file:
        trans = file.readline().split(",")
        for i in range(len(trans)):
            trans[i]=trans[i].strip()
            trans[i]=trans[i].strip("'")
        trans = trans[slice(1, 7)]
        insert(cursor, trans)

def insert(cursor, trans):
    add_transaction = ("INSERT INTO transaction_t"
        "(account_name, trans_amount, trans_date, trans_payee, trans_desc, category_name)"
        " VALUES (%s, %s, %s, %s, %s, %s)")
    trans_data = (trans[0],trans[1],trans[2],trans[3],trans[4], trans[5])
    cursor.execute(add_transaction, trans_data)