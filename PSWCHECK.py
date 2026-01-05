'''
Check whether password, mobile and mail are valid
'''
import re 
def CheckPassword(psw):
    c=d=e=f=0
    if len(psw)>=8 and len(psw)<=12:
        for i in psw:
            if i==" ":
                return False
            if i.islower():
                c=c+1
            elif i.isupper():
                d=d+1
            elif i.isdigit():
                e=e+1
            else:
                f=f+1
        if c>0 and d>0 and e>0 and f>0:
            return True
        
    return False
                

def CheckMobile(m):
    print(m,type(m))
    if len(str(m))==10:
        return True
    return False


def CheckEmail(mail):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail))
    
