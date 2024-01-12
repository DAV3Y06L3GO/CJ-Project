import CommandHandler

commandList = {"new", "entries", "users", "void"}

#Stores username
def newUser():
    while True:
        user = input("Please enter username: ") 


        if input(f"\n{user} is correct? (y/n)") in {"yes", "y"}:
            CommandHandler.screen_clear()
            return user



print("Initializing Mycological Observational Navigation System and Tracker for Enviromental Research...")

print("M.O.N.S.T.E.R is ready!")

while True:
    print("Greetings, \nWelcome to the M.O.N.S.T.E.R. \n\nTo start a new entry type \"new entry\" \nType \"help\" to show a list of commands")

    CommandHandler.parse(input())
