from tkinter import *
import time
import sqlite3


class login_GUI():
    def __init__(self,master):
        self.createwidgets(master)
     
    def getdatabase(self):
        db=sqlite3.connect('login.db')
        cursor = db.cursor()
        self.userentered = self.userenteredname.get()
        self.passentered = self.passenteredname.get()
        usersql = "SELECT username from userDetails where username = ?"
        passsql = "SELECT password from userDetails where password = ?"
        cursor.execute(usersql, (self.userentered,))
        self.usernames = cursor.fetchall()
        cursor.execute(passsql,(self.passentered,))
        self.passwords = cursor.fetchall()
        db.commit()
        db.close()

    def createwidgets(self,master):
        self.master=master
        self.master.title("Login Menu")
        
        self.userlabel=Label(self.master,text="Enter your username",width=20).grid(row=0,column=1)
        
        self.userenteredname=StringVar()
        self.userentry=Entry(self.master,textvariable=self.userenteredname)
        self.userentry.grid(row=1,column=0,columnspan=2)

        self.passlabel=Label(self.master,text="Enter your password",width=20).grid(row=2,column=1)

        self.passenteredname=StringVar()
        self.passentry=Entry(self.master,textvariable=self.passenteredname)
        self.passentry.grid(row=4,column=0,columnspan=2)

        self.confirmbutton=Button(self.master,text="Submit",command=self.checkdetails,width=20).grid(row=5,column=1)

        self.confirmlabeltext=StringVar()
        self.confirmlabel=Label(self.master,textvariable=self.confirmlabeltext,width=30).grid(row=6,column=1)

    def checkdetails(self):
        self.getdatabase()
        
        if len(self.usernames)>0 and len(self.passwords)>0 :
            self.confirmlabeltext.set("Success")
            self.newwindow=Toplevel(self.master)
            self.username = self.userentered
            newWindow(self.newwindow,self.username,self.passentered)
        else:
            if len(self.usernames)>0:
                self.confirmlabeltext.set('Incorrect Password')
            elif len(self.passwords)>0:
                self.confirmlabeltext.set('Incorrect Username')

            else:
                self.confirmlabeltext.set('Both Fields are Incorrect')
    
        self.userentry.delete(0,END)
        self.passentry.delete(0,END)

        
class newWindow():
    def __init__(self,master,username,password):
        self.username=username
        self.password = password
        self.master=master
        self.title = 'Welcome ' + self.username
        self.master.title(self.title)
        
        message=Label(self.master,text="Welcome",fg="red",bg="yellow",width=50).grid(row=0,column=0)

        backbutton=Button(self.master,text="Return",width=20,command=self.close).grid(row=1,column=0)
        changepasswordbut = Button(self.master,text='Change Pasword',command = self.changepassword).grid(row=2,column=0)

    def changepassword(self):
        self.passwordwindow = Toplevel(self.master)
        changepasswordwindow(self.passwordwindow,self.username,self.password)
        
    def close(self):
        self.master.destroy()
         
class changepasswordwindow():
    def __init__(self,master,username,password):
        self.oldpasswordcheck = password
        self.newpasswordentered = StringVar()
        self.oldpassword = StringVar()
        self.username = username
        self.master = master
        self.master.title = 'Change Password'

        self.passlabel = Label(self.master,text='Enter New Password').grid(row=2,column=0)
        self.newpassentry = Entry(self.master,textvariable=self.newpasswordentered).grid(row=3,column=0)
        self.newpassbut = Button(self.master,text='Change Password',command=self.changepassword).grid(row=4,column=0)

        self.oldpasslabel = Label(self.master,text='Enter Old Password').grid(row=0,column=0)
        self.oldpassentry = Entry(self.master,textvariable = self.oldpassword).grid(row=1,column=0)
        
    def changepassword(self):
        self.newpassword = self.newpasswordentered.get()
        if self.oldpassword.get() == self.oldpasswordcheck:
            db=sqlite3.connect('login.db')
            cursor = db.cursor()
            passSQL = 'UPDATE userDetails set password = ? where username == ?'
            cursor.execute(passSQL,(self.newpassword,self.username,))
            db.commit()
            db.close()
            self.correctlabel = Label(self.master,text='Password Accepted').grid(row=5,column=0)

        elif self.oldpassword.get() != self.oldpasswordcheck:
            self.incorrectlabel = Label(self.master,text='Incorrect password').grid(row=5,column=0)

        else:
            self.incorrectlabel = Label(self.master,text='Unknown Error').grid(row=5,column=0)


    def pwstrength(self):
        print('checking strength')

def main():
    root=Tk()
    login=login_GUI(root)
    root.mainloop()

if __name__=="__main__":
    main()