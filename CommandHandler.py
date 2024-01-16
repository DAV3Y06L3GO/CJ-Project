import json
import os
import datetime



blacklist = ["parse"]

def clear(): 
    os.system('cls' if os.name == 'nt' else 'clear')

def parse(raw_input, list=[]):
    if raw_input in list:
        return raw_input
    
    try: 
        command_name, *arguments = raw_input.split()
    except:
        print("Command empty, try again or type \"help\".")
        return parse(input(), list=list)

    if command_name in globals() and callable(globals()[command_name]) and not command_name in blacklist:
        stack = globals()[command_name]
        if arguments:
            stack(arguments[0])
        else:
            try: 
                stack() 
            except:
                print("Given command is missing a parameter")
                return parse(input(), list=list)
    else:
        print("Command not found, try again or type \"help\".")
        return parse(input(), list=list)



def new(arg):
    clear()
    match arg:
        case "user":
            #new user screen
            while True:
                new_user = input("Enter name of new user: ").strip()
                if new_user and new_user.isprintable():
                    if input(f"Create a new user named {new_user}? (y/n)") in ["yes", "y"]:
                        with open("./data/users.json", "r") as file:
                            users_data = json.load(file)

                        for i in users_data.keys():
                            if users_data[i] == True:
                                users_data[i] = False
                        
                        users_data[new_user] = True

                        with open("./data/users.json", "w") as file:
                            json.dump(users_data, file, indent=2)
                        print(f"{new_user} has been created and selected\nType \"back\" to return home")
                        parse(input())
                        return
                else: print("Sorry the given user name is invalid please pick a different name")
        
        case "session":
            entry_dirs = os.listdir("./data/entries/")
            newest_dir = entry_dirs[len(entry_dirs) - 1]
            session_number = int(newest_dir.rstrip(".json")) + 1

            with open(f"./data/entries/{session_number}.json", "x") as file:
                return

                
                
        
        case "entry":
            
            with open("./data/entries.json", "r") as file:
                entry_data = json.load(file)
            
            now = datetime.datetime.now()

            print("Current date: %s?\n" % (now.strftime("%x, %H:%M %p")))
            date_conf = input("Type \"confirm\" or enter a custom date")

            #if date_conf == "confirm":


                

                
            
            




def users():
    clear()
    
    with open("./data/users.json", "r") as file:
        users_data = json.load(file)

    while True:
        user_list = []
        user_string = ""
        user_selected = ""
        for i in users_data.keys():
            user_list.append(i)
            if users_data[i] == True:
                user_string += f"{i}(selected)\n"
                user_selected = i
            else:
                user_string += i + "\n"

        print("Select a user: \n")
        print(user_string)
        print("Type \"back\" to return to the homescreen")

        requested_user = parse(input(), list=user_list)

        if requested_user in user_list:
            
            print("MATCHED")
            users_data[user_selected] = False
            users_data[requested_user] = True
            with open("./data/users.json", "w") as file:
                json.dump(users_data, file, indent=2)
                print("DUMPED")
        else:
            return
        
        clear()
        print(f"{requested_user} has been selected")


def back():
    clear()