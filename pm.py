#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import crypto
from getpass import getpass
import password


# access database 
def sql_connection():
    try:
        con = sqlite3.connect("/Users/adamromayor/Projects/Passwords/.passwords.db", isolation_level=None)
        print("Connection is established")
        return con
    except Error:
        print(Error)


# user must login before accessing password manager
def login_user(cursorObj):
    user = input("Enter your username or \'q\' to quit: ") 
    user = user.lower()

    if(user == 'q'):
        return "QUIT"
    pw = getpass("Password: ")
    cursorObj.execute('SELECT * FROM users WHERE username = ?',(user,))

    data=cursorObj.fetchall()
    if len(data)==0:
        print('\nIncorrect username or password')
        return None
    else:
        check = crypto.decrypt_password(data[0][2]).decode("utf-8")      
        if(pw == check):
            print('\nYou now have access... welcome!\n ~~~\t~~~\t~~~\t~~~\n')
            return user
        
        print('\nIncorrect username or password')
        return None


# add another user to password manager
def add_user(cursorObj):
    while True:
        user = input("Enter a new username: ") 
        user = user.lower()
        cursorObj.execute('SELECT * FROM users WHERE username = ?',(user,))

        data = cursorObj.fetchall()
        if len(data) > 0:
            print("Username already exists.")
        else:
            break

    while True:
        pw = getpass("Enter a new password: ")
        check_pw = getpass("Retype password to confirm:")

        if(pw != check_pw):
            print("Passwords don't match!\n")
        else:
            break

    
    pw = crypto.encrypt_password(pw)
    cursorObj.execute('INSERT INTO users (username, password) VALUES(?,?)',(user, pw))



# update password for password manager
def update_password(cursorObj, user):
    while True:
        print("Are you sure you want to update the password of: " + user + "?")
        option = input("y/n: ").lower()
        if (option == 'y'):
            break
        elif(option == 'n'):
            print("Will not update password")
            return

    while True:
        pw = getpass("Enter a new password: ")
        check_pw = getpass("Retype password to confirm:")

        if(pw != check_pw):
            print("Passwords don't match!\n")
        else:
            break
    
    pw = crypto.encrypt_password(pw)
    cursorObj.execute('UPDATE users SET password = ? where username = ?', (pw, user))
    print("\nPassword Updated.\n")



# view login info of given website
def view_login(cursorObj, user, website):
    sql = "SELECT * FROM passwords WHERE username = ? AND website = ?"
    cursorObj.execute(sql,(user, website))

    data = cursorObj.fetchall()

    if(len(data) == 0):
        print(f"\n *** Login information for {website} does not exist ***\n")
    else:
        print(f"\nLogin credentials for {website}:")
        print(f"\tUsername: {data[0][4]}")
        pw = crypto.decrypt_password(data[0][3]).decode("utf-8")
        print(f"\tPassword: {pw}")
    return



# add login info of given website: username and password
# cannot add if website already exists
def add_login(cursorObj, user, website):
    sql = "SELECT * FROM passwords WHERE username = ? AND website = ?"
    cursorObj.execute(sql,(user, website))

    data = cursorObj.fetchall()

    if(len(data) > 0):
        print(f"\n *** Login information for {website} already exits ***\n")

    else:
        login =input(f"Username for {website}: ").lower()

        while True:
            choice = input("Generate random password (y/n)? ").lower()
            if(choice == "y"):
                pw = password.generate_pass(17)
                print(f"Password: {pw}")
                break
            elif(choice == "n"):
                while True:
                    pw = getpass()
                    c_pw = getpass("Retype password to confirm: ")
                    if(pw != c_pw):
                        print("Passwords don't match")
                    else:
                        break
                break
        
        pw = crypto.encrypt_password(pw)
        sql = "INSERT INTO passwords (username, website, password, login) VALUES(?, ?, ?, ?)"
        cursorObj.execute(sql, (user, website, pw, login))
        print(f"Successfully added login information for {website}")



# deletes login credentials of given website
def delete_login(cursorObj, user, website):
    sql = "SELECT * FROM passwords WHERE username = ? AND website = ?"
    cursorObj.execute(sql,(user, website))

    data = cursorObj.fetchall()

    if(len(data) == 0):
        print(f"\n *** Login information for {website} does not exist ***\n")
    else:
        while True:
            choice = input(f"Are you sure you want to delete login info for {website} (y/n)? ").lower()

            if(choice == "y"):
                sql = "DELETE FROM passwords WHERE username = ? AND website = ?"
                cursorObj.execute(sql, (user, website))
                print(f"Login info for {website} successfully deleted")
                return
            elif (choice == "n"):
                print(f"Did not delete login info for {website}")
                return



# only update password for the website, not the username
def update_pass_website(cursorObj, user, website):
    sql = "SELECT * FROM passwords WHERE username = ? AND website = ?"
    cursorObj.execute(sql,(user, website))

    data = cursorObj.fetchall()

    if(len(data) == 0):
        print(f"\n *** Login information for {website} does not exist ***\n")
        return
    else:
        # user can auto generate password or create own
        while True:
            choice = input("Generate random password (y/n)? ").lower()
            if(choice == "y"):
                pw = password.generate_pass(17)
                print(f"Password: {pw}")
                break
            elif(choice == "n"):
                while True:
                    pw = getpass()
                    c_pw = getpass("Retype password to confirm: ")
                    if(pw != c_pw):
                        print("Passwords don't match")
                    else:
                        break
                break
        
        pw = crypto.encrypt_password(pw)
        sql = "UPDATE passwords SET password = ? WHERE username = ? AND website = ?"
        cursorObj.execute(sql, (pw, user, website))
        print(f"Password for {website} updated successsfully")



# list all websites saved in password manager
def list_websites(cursorObj, user):
    sql = "SELECT website FROM passwords WHERE username = ? ORDER BY website"
    cursorObj.execute(sql, (user,))
    data = cursorObj.fetchall()
    for d in data:
        print(f"\t> {d[0]}")


# list all login information
# not recommended because it lists passwords
def all_logins(cursorObj, user):
    sql = "SELECT website FROM passwords WHERE username = ? ORDER BY website"
    cursorObj.execute(sql, (user,))
    data = cursorObj.fetchall()
    for d in data:
        view_login(cursorObj, user, d[0])



tables = ["passwords", "users"]

def main():
    con = sql_connection()
    cursorObj = con.cursor()

    
    while True:
        user = login_user(cursorObj)
        if (user == "QUIT"):
            print("Goodbye...")
            return -1
        elif (user != None):
            break
        print()
    
    
    while True:
        print("\n##################################\n")
        print("What would you like to do?")
        print("\t(N) Add new user")
        print("\t(C) Change password of current user")
        print("\t(V) View login info of website")
        print("\t(A) Add login info for website")
        print("\t(U) Update password for website")
        print("\t(L) List all saved websites")
        print("\t(D) List login info for all websites (not recommended)")
        print("\t(X) Delete login info for website")
        print("\t(E) Exit")
        

        option = input("Choice: ").lower()

        if (option == 'n'):
            print('Adding user')
            add_user(cursorObj)
        elif (option == 'c'):
            print('Changing Password')
            update_password(cursorObj, user)
        elif (option == 'v'):
            web = input("\nWhich website? \nWebsite: ").lower()
            view_login(cursorObj, user, web)
        elif (option == 'a'):
            web = input("\nWhich website? \nWebsite: ").lower()
            add_login(cursorObj, user, web)
        elif(option == 'l'):
            print("\nList of websites with login info:")
            list_websites(cursorObj,user)
        elif(option =='d'):
            all_logins(cursorObj, user)
        elif(option =='u'):
            web = input("\nWhich website? \nWebsite: ").lower()
            update_pass_website(cursorObj,user, web)
        elif(option =='x'):
            web = input("\nWhich website? \nWebsite: ").lower()
            delete_login(cursorObj,user, web)
        elif (option == 'e'):
            print("\nGoodbye!")
            return 0
        
    

if __name__ == "__main__":
    main()