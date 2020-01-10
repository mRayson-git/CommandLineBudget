import json
import datetime
from os import system, name

def loadFile():
    with open('config.json') as file:
        data = json.load(file)
    return data

def getToday():
    currDate = datetime.datetime.today()
    return str(currDate.strftime('%Y-%m-%d'))

def getThisMonth():
    currDate = datetime.date.today()
    return currDate.strftime('%Y-%m')

def getLastMonth():
    currDate = datetime.date.today()
    first = currDate.replace(day = 1)
    lastMonth = first - datetime.timedelta(days=1)
    return str(lastMonth.strftime('%Y-%m'))

def configDateUpdate():
    '''Updates the date fields in the config file. Past, Present, Future'''

    #read the config file
    with open('config.json') as file:
        data = json.load(file)

    #set the date values
    data['lastRun'] = getToday()

    #write to the config file
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

def clear():
    if (name == 'nt'):
        _ = system('cls')
    else:
        _ = system('clear')