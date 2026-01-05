#forgot password
import entry_sql as sq
import sql_pass_modify as sq1
import random
import pywhatkit
import PSWCHECK as pw
def fp():
    mail=input("User ID:")
    mob=int(sq.sqlread(mail,'1234'))
    if len(str(mob))==10:
        f=True
        while f:
            otp=int(otpgenerate())
            sms="Your OTP: "+str(otp)
            mob="+91"+str(mob)
            pywhatkit.sendwhatmsg_instantly(mob,sms)
            check=int(input("Enter otp "))
            if check==otp:
                setpassword(mail)
                print("Password sucessfully updated")
                f=False
            else:
                print("OTP incorrect.Try again")
    else:
        print("User Id does not exist")
                

def otpgenerate():
    n=random.randint(1000,9999)
    return n


def setpassword(mail):
    psw1=input("New Password:")
    if pw.CheckPassword(psw1):
        f=True
        while f:
            psw2=input("Confirm Password:")
            if psw1==psw2:
                modifypassword(mail,psw1)
                f=False
            else:
                print("Confirmed password not matched")
        
            
    
def modifypassword(mail,psw1):
    print (mail,psw1)
    sq1.sqlmodify(mail,psw1)

    
    
    
