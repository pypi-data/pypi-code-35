from random import random, choice, randint
import pyperclip
import sys
import os
import re
import os.path
import errno
import shutil
from os.path import basename
def clear():
    os.system('cls')
def cont():
    input("Press Enter to continue.")
def invalid():
    print("Invalid input, please try again.")
def autosave(pwd):
            title = input("Name your password:")
            file = open('data/reg/'+title, "a")
            file.write(str(pwd))
            file.close()            
def lista():
    directorio = os.listdir('data/reg/')
    archivos = [os.path.splitext(x)[0] for x in directorio]
    for line in archivos:
        line = line.strip()
        line = line.split('\t', 0)
        print (line)
    return archivos
def listabk():
    directorio = os.listdir('data/backups/')
    archivos = [os.path.splitext(x)[0] for x in directorio]
    for line in archivos:
        line = line.strip()
        line = line.split('\t', 0)
        print (line)
    return archivos
def copy(src, dest):
            try:
                shutil.copytree(src, dest)
                print("Back up created.")
            except OSError as e:
                # If the error was caused because the source wasn't a directory
                if e.errno == errno.ENOTDIR:
                    shutil.copy(src, dest)
                else:
                    print('Directory not copied. Error: %s' % e)
def paster(src, dest):
            try:
                shutil.copytree(src, dest)
                print("Back up restored.")
            except OSError as e:
                # If the error was caused because the source wasn't a directory
                if e.errno == errno.ENOTDIR:
                    shutil.copy(src, dest)
                else:
                    print('Directory not copied. Error: %s' % e)                    
#MAIN MENU#
while True:
    clear()
    print("\033[92m###MAIN MENU###" '\x1b[0m')
    print("Select option:")
    print("1.Generate")
    print("2.Override")
    print("3.Retrive")
    print("4.Remove")
    print("5.Back Up")
    print("6.Exit")
    try:
        choose = int(input("Enter choice:"))
    except ValueError:
        invalid()
        cont()
        continue
#GENERATE#
    if choose == 1: 
        clear()
        try:
            lenght = int(input("Set password lenght and press enter:"))
        except ValueError:
            invalid()
            cont()
            continue    
        capitals = "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        letters = "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        digits = "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
        simbols = "!", "@", "#", "$", "%", "&", "?", "=", "+", "-", "*", "/"
        chars = capitals + letters + digits 
        min_length = lenght
        max_length = lenght
        password = "".join(choice(chars)
                           for x in range(randint(min_length, max_length)))
        print("Password generated:", password)
        pyperclip.copy(password)
        print("Your pasword is", lenght, "characters long")
        autosave(password)
        print("You password has been stored and copied to clipboard.")
        cont()
        clear()
        continue
#OVERRIDE#
    elif choose == 2: 
        clear()        
        lst = lista()
        file = str(input("Type password name to Override:"))
        if file in lst:
            newpwd = input("Type new password:")
            with open('data/reg/'+file, "w" ) as f:
                f.write(str(newpwd))
                f.close()
                print("Password succesfully overrided")
                cont()
        else:
            invalid()
            cont()
        continue
#RETRIVE#
    elif choose == 3:
        clear()
        lst = lista()
        file = input("Type password name to retrive:")
        if file in lst:
            clear()
            with open('data/reg/'+file, 'r') as myfile:
               data = myfile.read()
               print("Your "+file+" Passwoerd is:"+data)
               pyperclip.copy(data)
               print("Password copied to clipboard")
               input("Press Enter to Main Menu")
               continue                   
        else:
            print("Password not found")
            input("Press Enter to continue")            
            continue
#REMOVE# 
    elif choose == 4:           
            clear()
            lst = lista()
            rem = input("Type password name to REMOVE and press ENTER:")
            if rem in lst:           
                a = input(" Are you sure to delete current Password?\n Please enter y/n:")
                if a == "y":
                    if os.path.exists('data/reg/'+rem):
                        os.remove('data/reg/'+rem)
                        print("Password: "+rem+" REMOVED")
                        input("Press Enter to continue")
                    continue
                if a == "n":
                    print("Password not removed")
                    cont()
                else:
                    print("Please enter either y/n:")
                continue
            else:
                invalid()
                cont()
            continue
#BACK UP#
    elif choose == 5:
        clear()
        print("BACK UP OPTIONS:\n1.Write new Back Up.\n2.Restore previous Back Up.\n3.Cancel.")
        opt = input("Enter choice: ")    
        if opt == "1":
            newbk = input("Name your new Back up: ")
            copy('data/reg/','data/backups/'+newbk+'/')
            cont()        
        elif opt == "2":
            clear()
            lst = listabk()             
            bk = input("Select which copy do you want to restore: ")
            if bk in lst:
                check= input("This action will remove all previously saved data. Do you wish to continue?\nPlease enter y/n: ")
                if check == "y":
                    shutil.rmtree('data/reg/')
                    paster('data/backups/'+bk+'/','data/reg/')
                    cont()
                if check == "n":
                    print("Action CANCELED")
                    cont()
                else:
                    print("Please enter either y/n:")
                continue
        else:
            invalid()
            cont()
        continue
        
#EXIT#
    elif choose == 6:
        clear()        
        input('Press ENTER to exit')
        sys.exit(0)
            
    else:
        invalid()
        cont()
        continue
