import mysql.connector as c
from datetime import date
import csv
import os
from dotenv import load_dotenv

load_dotenv(".env")

con=c.connect(host=os.environ.get("DB_HOST", "localhost"), user=os.environ.get("DB_USER", "root"), passwd=os.environ.get("DB_PASSWORD"))
cursor=con.cursor()
lst=[]
new=[]
cursor.execute("create database if not exists trendhub")
con.commit()
cursor.execute("use trendhub")
cursor.execute("create table if not exists customer(name varchar(20), mail varchar(30) unique, mobile bigint primary key, password varchar(20), dateofjoining date)")
cursor.execute("create table if not exists fashion(pro_id int primary key, name varchar(30), clothing_type varchar(25), brand varchar(10), price bigint)")
cursor.execute("create table if not exists employee(emp_id int primary key, emp_name varchar(20), mobile bigint unique, mail varchar(30) unique, password varchar(20), department varchar(15))")
con.commit()
#to create a dummy catalogue
cursor.execute("select count(*) from fashion")
if cursor.fetchone()[0] == 0:
    with open('fashion_dummy.csv', 'r') as file:
        reader = csv.reader(file)
        for i in reader:
            lst.append(i)
    for i in range(2,len(lst),2):
        new.append(lst[i])
    for i in range(0,len(new)):
        field=new[i]
        pro_id=field[0]
        name=field[1]
        types=field[2]
        brand=field[3]
        price=field[4]
        x="insert into fashion values("+str(pro_id)+",'"+name+"','"+types+"','"+brand+"',"+str(price)+")"
        cursor.execute(x)
    con.commit()
#The user will have to login here
def login():
    print("Press 1 to log in as a customer \nPress 2 to log in as employee \nPress 3 to create a new account\n\
Press 4 to delete an account")
    a=int(input("Enter here: "))
    global name
    #To log in as a customer
    if a==1:
        lst=[]
        global log
        mobile=int(input("Enter Mobile Number to login: "))#To search User IDs in the database
        passw=input("Enter Password: ")
        x="select mobile,password,name from customer"
        cursor.execute(x)
        for i in cursor:
            lst.append(i)#The tuples are stored in a list
        for i in lst:
            try:
                if (mobile,passw)==(i[0],i[1]):
                    #Matching the login credentials
                    print("Logged in as "+(i[2]))
                    name=i[2]
                    log=1
            except:
                print("error occured")
    #To log in as Employee
    if a==2:
        lst=[]
        mobile=int(input("Enter Mobile Number or Employee Id to login: "))
        passw=input("Enter Password: ")
        x="select mobile,password,emp_name,emp_id from employee"
        cursor.execute(x)
        for i in cursor:
            lst.append(i)
        for i in lst:
            try:
                #To Match the Credentials
                if (mobile,passw)==(i[0],i[1])or(mobile,passw)==(i[3],i[1]):
                    print("Logged in as "+str(i[2]))
                    log=2
                    name=i[2]
            except:
                print("error occured")
    #To Create A New Account
    if a==3:
        c=int(input("Enter 1 for entering as Customer and Enter 2 for entering as Employee: "))
        if c==1:
            name=input("Enter Your name: ")
            mail=input("Enter your mail id: ")
            mobile=int(input("Enter your mobile number: "))
            password=input("Create password: ")
            confirm=input("Confirm your password: ")
            q=1
            #Will Run till the passwords are matched
            while q==1:
                if password==confirm:
                    print("Password created")
                    q=2
                else:
                    confirm=input("Password does not match. Confirm your password again: ")
            #To input the date of joining
            datex=date.today()
            dates=datex
            x="insert into customer values("+"'"+name+"','"+mail+"',"+str(mobile)+",'"+password+"','"+str(dates)+"')"
            cursor.execute(x)
            con.commit()
            print("Account Created")
            print("Logged in as",name)
            log=1
            
        if c==2:
            emp_id=int(input("Enter employee id given on the day of joining: "))
            name=input("Enter Your name: ")
            mail=input("Enter your mail id: ")
            mobile=int(input("Enter your mobile number: "))
            password=input("Create password: ")
            confirm=input("Confirm your password: ")
            q=1
            while q==1:
                if password==confirm:
                    print("Password created")
                    q=2
                else:
                    confirm=input("Password does not match. Confirm your password again: ")
            department=input("Enter department allotted: ")
            x="insert into employee values("+str(emp_id)+",'"+name+"',"+str(mobile)+",'"+mail+"','"+password+"','"+department+"')"
            cursor.execute(x)
            con.commit()
            print("Account Created")
            print("Logged in as",name)
            log=2
    #To Delete an account
    if a==4:
        c=int(input("Enter 1 to delete a customer data and Enter 2 to delete a employee: "))
        if c==1:
            lst=[]
            mobile=int(input("Enter Mobile Number to login: "))
            passw=input("Enter Password: ")
            x="select mobile,password,name from customer"
            cursor.execute(x)
            for i in cursor:
                lst.append(i)
            for i in lst:
                try:
                    if (mobile,passw)==(i[0],i[1]):
                        print("Deleting account of "+str(i[2]))
                        name=i[2]
                        ele=i[0]
                        print(ele)
                        log=1
                except:
                    print("error occured")
        if c==2:
            lst=[]
            mobile=int(input("Enter Employee Id to login: "))
            passw=input("Enter Password: ")
            x="select mobile,password,emp_name,emp_id from employee"
            cursor.execute(x)
            for i in cursor:
                lst.append(i)
            for i in lst:
                try:
                    if (mobile,passw)==(i[3],i[1]):
                        print("Logged in as "+(i[2]))
                        ele=i[3]
                        log=2
                except:
                    print("error occured")
        if log==1:
            x="delete from customer where mobile="+str(ele)
            cursor.execute(x)
            con.commit()
            raise Exception
        if log==2:
            x="delete from employee where emp_id="+str(ele)
            cursor.execute(x)
            con.commit()
            raise Exception
    #If value is out of Range
    if a<1 or a>4:
        raise Exception

#This is to display and purchase the items from the catalogue given
def displayitems():
    total=0
    itemlist=[]
    itemcode=[]
    bill=[]
    global billno
    print("Hello,",name,"Welcome to the catalogue of the trendhub. \nThis will led you to the catalogue of the outfits available with us")
    print("Let's begin with everything we have.\nThe catalogue will start up with the outfit item code followed by their name, type,\
brand and then their price")
    #To display the catalougue
    x="select*from fashion"
    cursor.execute(x)
    for i in cursor:
        itemlist.append(i)#To store in the list
        print(i)
    for j in range(0,100):
        cart=int(input("Enter the Item Number to purchase: "))
        for i in itemlist:
            if i[0]==cart:
                itemcode.append(i[0])
                total=total+int(i[4])
                bill.append(i)
        #To continue shopping
        d=int(input("Do you want to add more? Press 1 for yes and 2 for no: "))
        if d==1:
            continue
        if d==2:
            break
    print("Your Total Expenditure is Rs.",total)
    #Payment Confirmation
    pay=int(input("Continue to the Payment? Press 1 for yes and Press 2 for no: "))
    if pay==1:
        print("Thanks for purchasing items of amount Rs.",total,". The bill will be generated shortly. ")
        billno=billno+1
        print("BILL NO. ",billno)
        for i in bill:
            print(i)
        print("Logged Out after purchasing")
    if pay==2:
        print("Logging you out")
        raise Exception
    #Logged out of the account after purchasing
#The changes that only a employee can make
def editfashion():
    global asw
    print("Press 1 to add a new item\nPress 2 to update an existing item\nPress 3 to Delete an item\nPress 4 to log out ")
    a=int(input("Enter Here: "))
    #To add a new item
    if a==1:
        pro_id=int(input("Enter Product ID: "))
        name=input("Enter product name: ")
        clothing_type=input("Enter the type of clothing: ")
        brand=input("Enter brand name: ")
        price=int(input("Enter Price: "))
        x="insert into fashion values("+str(pro_id)+",'"+name+"','"+clothing_type+"','"+brand+"',"+str(price)+")"
        cursor.execute(x)
        con.commit()
        print("Item Entered")
    #To Modify items in catalougue
    if a==2:
        print("What do You want to change?\nPress 1 for Item name\nPress 2 for Clothing Type\nPress 3 for Brand\nPress 4 for Price")
        d=int(input("Enter Here: "))
        ids=int(input("Enter Item No: "))
        if d==1:
            s=input("Enter the Item Name: ")
            x="update fashion set name='"+s+"' where pro_id="+str(ids)
            cursor.execute(x)
            con.commit()
            print("Successfully Done")
        if d==2:
            s=input("Enter the Clothing Type: ")
            x="update fashion set clothing_type='"+s+"' where pro_id="+str(ids)
            cursor.execute(x)
            con.commit()
            print("Successfully Done")
        if d==3:
            s=input("Enter the Brand Name: ")
            x="update fashion set brand='"+s+"' where pro_id="+str(ids)
            cursor.execute(x)
            con.commit()
            print("Successfully Done")                                                                                              
        if d==4:
            s=int(input("Enter the Price: "))
            x="update fashion set price="+str(s)+" where pro_id="+str(ids)
            cursor.execute(x)
            con.commit()
            print("Successfully Done")
        if d<1 or d>4:
            raise Exception
    #To delete an item
    if a==3:
        w=int(input("Enter the Item Number you want to delete: "))
        x="delete from fashion where pro_id="+str(w)
        print("DELETED")
    #To log out
    if a==4:
        asw=4
    #Value out of Range
    if a>4 or a<1:
        raise Exception
#Menu Driven Program
ise=6
name=""
billno=1000
while ise>3:
    log=0
    asw=0
    try:
        login()
        if log==1:
            try:
                displayitems()
            except:
                print("Logged Out")
        if log==2:
            while ise>4:
                try:
                    editfashion()
                    if asw==4:
                        print("LOGGED OUT")
                        break
                except:
                    print("Error Occured")
                    continue
    except:
        continue    