#    BANK MANAGEMENT SYSTEM
from dotenv import load_dotenv
import os
load_dotenv()
import pymysql

con = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=3306
)

cursor = con.cursor()


#ADD NEW DATA--------------------------------------------------------------------------------------------
def adding_data():
    password = int(os.getenv("STAFF_PASSWORD"))
    check=int(input("enter password:" ))
    if check!=password:
        print("wrong password")
        return
    else: 
        try:
            while True:
                name=input("enter name:")
                if len(name.strip( ))==0:
                    print("enter name")
                    continue
                balance=int(input("enter amount present:"))
                pin=int(input("enter pin:"))
                query="insert into accounts(name,balance,pin) values(%s, %s, %s)"
                cursor.execute(query,(name,balance,pin))
                con.commit()
                ch=input("want to add more record(y/n):")
                if ch in "nN":
                    print("every data added succesfully")
                    break
        except Exception as e:
            print("ERROR:",e)
      


#STAFF VIEWING DATA--------------------------------------------------------------------------------------
def staff_view_data():
    password = int(os.getenv("STAFF_PASSWORD"))
    check=int(input("enter password:"))
    if check!=password:
        print("wrong password")
    else:
        ch=int(input("enter whether want whole data(1)\nspecific person data(2):"))
        if ch==1:
            query="select * from accounts"
            cursor.execute(query)
            data=cursor.fetchall()
            print("All accounts data:")
            for i in data:
                print("Id:", i[0], "Name:", i[1], "Balance:", i[2])
        elif ch==2:
            id=int(input("Enter Id:"))
            query="select * from accounts where id=%s"
            cursor.execute(query,(id,))
            data=cursor.fetchone()
            if data is None:
                print("account doesn't exist")
                return
            print("Accounts data:")            
            print("Id:", data[0], "Name:", data[1], "Balance:", data[2])


#CUSTOMER ABLE TO SEE DATA-------------------------------------------------------------------------------
def customer_view_data():
    id=int(input("enter your Id: "))
    query="select * from accounts where id=%s"
    cursor.execute(query,(id,))
    data=cursor.fetchone()
    if data:
        print("Id:", data[0], "Name:", data[1], "Balance:", data[2])
    else:
        print("account doesn't exist")


#CASH WITHDRAWING----------------------------------------------------------------------------------------
def withdrawal():
    try:
        pin=int(input("Enter your pin: "))
        query="select * from accounts where pin=%s"
        cursor.execute(query,(pin,))
        data=cursor.fetchone()
        if data is None:
            print("no account found")
            return
        amount_withdrawing=int(input("enter amount to withdrawal: "))
        if amount_withdrawing <= 0:
            print("amount cannot be withdrawal ")
            return
        if data[2] < amount_withdrawing:
            print("not sufficient balance")
        else:
            query="update accounts set balance=balance-%s where pin=%s"
            cursor.execute(query,(amount_withdrawing,pin))
            con.commit()
            print("amount has been deducted")
    except Exception as e:
        print("ERROR: ",e)


#DEPOSIT IN BANK ACCOUNT---------------------------------------------------------------------------------
def deposit():
    try:
        accno=int(input("enter your Id: "))
        if accno < 0 :
            print("Id doesn't exist")
            return
        amount=int(input("enter amount to be deposit: "))
        if amount < 0:
            print("can't deposit negative")
            return
        query="update accounts set balance=balance+%s where Id=%s"
        cursor.execute(query,(amount,accno))
        con.commit()
        print("Amount deposit:",amount)
    except Exception as e:
        print('ERROR',e)


#UPDATING ACCOUNT DETAILS--------------------------------------------------------------------------------
def update_details():
    try:
        accno=int(input("enter your Id: "))
        if accno < 0 :
            print("Id doesn't exist")
            return
        query="select* from accounts where id=%s"
        cursor.execute(query,(accno,))
        check=cursor.fetchone()
        if check is None:
            print("account doesn't exist")
            return
        pin=int(input("enter your pin: "))
        if pin < 0 :
            print("pin doesn't exist")
            return
        ch=int(input("what you want to update\nfor name(1)\nfor pin(2): "))
        if ch==1:
            new_name=input("enter your new name=")
            query="update accounts set name=%s where Id=%s"
            choice=input("want to confirm(y/n): ")
            if choice == 'n' or choice=='N':
                print("change is cancelled")
                return
            elif choice == 'y' or choice=='Y':
                cursor.execute(query,(new_name,accno))
                con.commit()
                print("data updated")
            else:
                print("wrong input")
        elif ch==2:
            newpin=int(input("enter your new pin: "))
            query="update accounts set pin=%s where id=%s"
            ch=input("you want to confirm this pin?(y/n)")
            if ch=='y' or ch=='Y':
                cursor.execute(query,(newpin,accno))
                con.commit()
                print("new pin updated")
            elif ch=='n' or ch=='N':
                return
            else:
                print("wrong input")
    except Exception as e:
        print("ERROR",e)


#--------------------------------------------------------------------------------------------------------
#EXECUTION

while True:
   
    print("adding data press------------------------>(1)")
    print("view account details (FOR STAFF) press--->(2)")
    print("view your account details press---------->(3)")
    print("withdrawing money from account press----->(4)")
    print("deposit money in account press----------->(5)")
    print("update account details press------------->(6)")
    print("want to (exit press)--------------------->(7)")
                 
    ch=int(input("enter your choice: "))


    if ch==1:
        adding_data()
    elif ch==2:
        staff_view_data()
    elif ch==3:
        customer_view_data()
    elif ch==4:
        withdrawal()
    elif ch==5:
        deposit()
    elif ch==6:
        update_details()
    elif ch==7:
        print("EXIT")
        break
    else:
        print("wrong input")