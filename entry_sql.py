'''
Enter the info derived from signup into the sql database
Also checks whether user already exists
'''
import mysql.connector

mycon=mysql.connector.connect(host="localhost",user="root",passwd="1234",database="stock")
mycon.autocommit=True
cursor=mycon.cursor()

def sqlsave(name,mail,mobile,state,city,password):

    s="INSERT INTO USER VALUES('{}','{}',{},'{}','{}','{}')".format(name,mail,mobile,state,city,password)
    cursor.execute(s)
        
def sqlread(mail,pw):
    c=0
    s="SELECT MAIL FROM USER WHERE MAIL='{}'".format(mail)
    cursor.execute(s)
    row=cursor.fetchone()
    if pw==row[1]:
        return True
    return False
          

def exists(mail):
    s="SELECT MAIL FROM USER WHERE MAIL='{}'".format(mail)
    cursor.execute(s)
    row=cursor.fetchone() #read only one value from the cursor 
    if row == None:
        return False
    return True 
    
def exists_psw(mail,PW):
    s="SELECT PASSWORD FROM USER WHERE MAIL='{}'".format(mail)
    cursor.execute(s)
    row=cursor.fetchone() #read only one value from the cursor
    if row[0] == PW:
        return True
    return False

