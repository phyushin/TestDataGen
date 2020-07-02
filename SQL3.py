#! /usr/bin/python3
import sqlite3
import string
import secrets
import datetime


from faker import Faker

TD = Faker('en_GB')#this can be set to other languages see docs for more info

def create_password(stringLength):
    chars = string.ascii_letters + string.digits + string.punctuation
    password =''.join(secrets.choice(chars) for i in range(stringLength))
    return password
    
def create_users():
    firstName = TD.first_name()
    lastName = TD.last_name()
    domain = TD.domain_name()
    email = (firstName+'.'+lastName+'@'+domain)
    StartDate = str(TD.date_this_century())
    connection = sqlite3.connect('TestData.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Users ("UID"	INTEGER ,"First_Name" TEXT ,"Last_Name" TEXT ,"Birthdate" TEXT DEFAULT "01-01-1899",  "Password" TEXT,"Email" TEXT,"Job_Title" TEXT DEFAULT "Worker","StartDate" TEXT DEFAULT "01-01-1899");')
    cursor.execute('INSERT INTO Users VALUES(:UID, :First_Name, :Last_Name, :Birthdate, :Password, :Email, :Job_Title, :StartDate)',
    {'UID':TD.random_int(1,100),'First_Name': firstName,'Last_Name': lastName  ,'Birthdate': str(TD.date_of_birth(minimum_age=17, maximum_age=85)),
    'Password': create_password(16), 'Email': email,'Job_Title': TD.job(), 'StartDate': StartDate})
    connection.commit()
    connection.close()

def multi_create_users():
    i = 0 
    count = input("How many names would you like to generate?: ")
    while i < int(count):
        create_users()
        i += 1

def create_customers():
    connection = sqlite3.connect('TestData.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS CUSTOMERS ("CID" INTEGER,"Name" TEXT, "Birthdate" TEXT, "Address" TEXT, "Email" TEXT);')
    cursor.execute('INSERT INTO CUSTOMERS VALUES(:CID, :Name, :Birthdate, :Address, :Email)',{'CID':TD.random_int(1,100), 'Name': TD.name(), 'Birthdate': str(TD.date_of_birth(minimum_age=17, maximum_age=85))
    ,'Address': TD.address(), 'Email': TD.email()})
    select_customers()
    connection.commit()
    connection.close()

def multi_create_customers():
    i = 0 
    count = input("How many names would you like to generate?: ")
    while i < int(count):
        create_customers()
        i += 1

def create_part():
    connection = sqlite3.connect('TestData.db')
    cursor = connection.cursor()
    partName = (TD.word()+'-'+str(TD.random_int(1,10000)))
    cursor.execute('CREATE TABLE IF NOT EXISTS PARTS ("PID" TEXT, "Part_Name" TEXT, "Cost" real,"BaseCurrency" TEXT, "QTY" INTEGER);')
    cursor.execute('INSERT INTO PARTS VALUES(:PID, :Part_Name, :Cost, :BaseCurrency, :QTY)',{'PID':TD.random_int(1,100), 'Part_Name': partName,'BaseCurrency':'£', 'Cost':TD.random_int(1,100)
    ,'QTY': TD.random_int(1,100)})
    select_parts()
    connection.commit()
    connection.close()

def multi_create_parts():
    i = 0 
    count = input("How many parts would you like to generate?: ")
    while i < int(count):
        create_part()
        i += 1
        

def select_users():
    connection = sqlite3.connect('TestData.db')
    cursor = connection.cursor()
    print ("############################")
    print ("########### Users ##########")
    print ("############################")
    print("Name, Dob, Password, Email, job title, start date")
    cursor.execute('SELECT * FROM Users')
    for i in cursor.execute('SELECT UID,First_Name, Last_Name, Birthdate, Password, Email, Job_Title, StartDate FROM Users'):
        print(i)
    connection.close()
    print ("############################")

def select_customers():
    connection = sqlite3.connect('TestData.db')
    cursor = connection.cursor()
    print ("############################")
    print ("######## Customers #########")
    print ("############################")
    cursor.execute('SELECT * FROM CUSTOMERS')
    for i in cursor.execute('SELECT CID, Name, Birthdate, Address, Email FROM CUSTOMERS'):
        print(i)
    connection.close()
    print ("#########################")

def select_parts():
    connection = sqlite3.connect('TestData.db')
    cursor = connection.cursor()
    print ("############################")
    print ("########## PARTS ###########")
    print ("############################")
    cursor.execute('SELECT * FROM PARTS')
    for i in cursor.execute('SELECT PID, Part_Name, Cost, BaseCurrency, QTY FROM PARTS'):
        print(i)
    connection.close()
    print ("#########################")

def select_all_data():
    select_customers()
    print("\n")
    select_users()
    print("\n")
    select_parts()
    print("\n")

def main():
    opt1 = input("Do you want to READ or WRITE (R/W/eXit): ")
    if opt1.upper() == 'R':
        opt1a = input("What data would you like to read ? Customers ,User ,All (C,U,A): ")
        if opt1a.upper() == 'C':
            select_customers()
        elif opt1a.upper() == 'U':
            select_users()
        elif opt1a.upper() == 'P':
            select_parts()
        elif opt1a.upper() == 'A':
            select_all_data()
        else:
            print ("Invalid selection")
    elif opt1.upper() == 'W':
            opt2 = input("What data would you like to Create ? Customers ,Users, Parts (C,U,P): ")
            if opt2.upper() == 'C':
                    opt2a = input("Do you want to create more than one record? (Y/N/eXit): ")
                    if opt2a.upper() == 'Y':
                        multi_create_customers()
                    elif opt2a.upper() == 'N':
                        create_customers()
                    elif opt2a.upper() == 'X':
                        print("Goodbye")
                        exit()

            elif opt2.upper() == 'U':
                    opt2a = input("Do you want to create more than one record? (Y/N/eXit): ")
                    if opt2a.upper() == 'Y':
                        multi_create_users()
                    elif opt2a.upper() == 'N':
                        create_users()
                    elif opt2a.upper() == 'X':
                        print("Goodbye")
                        exit()
            elif opt2.upper() == 'P':
                    opt2a = input("Do you want to create more than one record? (Y/N/eXit): ")
                    if opt2a.upper() == 'Y':
                        multi_create_parts()
                    elif opt2a.upper() == 'N':
                        create_part()
                    elif opt2a.upper() == 'X':
                        print("Goodbye")
                        exit()
            else:
                print ("Invalid selection")

    elif opt1.upper() == 'X':
        print("Goodbye")
        exit()
    else:
        print("Invalid option please try again")
    main()

if __name__ == "__main__":
    main()
    