'''
This code is used in FORGOTPASSWORD_GUI to fetch the wapp no.
of the corresponding userid(mail)and update the changed password in the database
'''
import mysql.connector

mycon=mysql.connector.connect(host="localhost",user="root",passwd="1234",database="stock")
mycon.autocommit=True
cursor=mycon.cursor()


def sqlmodify(mail,psw1):
    s="UPDATE user SET password='{}' WHERE mail='{}'".format(psw1,mail)
    cursor.execute(s)
    

def sql_user_mob(email):
    s="select mobile from user where mail='{}'".format(email)
    cursor.execute(s)
    mob=cursor.fetchone()
    #print (int(mob[0]))
    return int(mob[0])
    
'''
email='rikdas@gmail.com'
sql_user_mob(email)
'''
