import os
import json

import CommandHandler;

commandList = {"new", "entries", "users", "void"}

#Stores username
def newUser():
    while True:
        user = input("Please enter username: ") 


        if input("\n%s is correct? (y/n)" % (user)) in {"yes", "y"}:
            os.system('cls' if os.name == 'nt' else 'clear')
            return user

print("Initializing Mycological Observational Navigation System and Tracker for Enviromental Research...")

print("M.O.N.S.T.E.R is ready!")



print("Greetings, \nWelcome to the M.O.N.S.T.E.R. \n\nTo start a new entry type \"new entry\" \nType \"help\" to show a list of commands")




