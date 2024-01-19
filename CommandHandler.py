import json
import os
import datetime



blacklist = ["parse"]

session_number = 1

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
    global session_number

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
            
            try: 
                with open(f"./data/entries/{session_number}.json", "r") as file:
                    session_data = json.load(file)
            except:
                print("Session not found or not selected please select or create a new session.\n")
                return
            
            name = input("What would you like to call this entry?\n")
            new_entry = {
                name: {
                    "gps": None,
                    "date": None,
                    "genus": None,
                    "species": None,
                    "substrate": None,
                    "terrain": None,
                    "gill": None,
                    "other": None
                }
            }

            ####################GPS GOES HERE########################
            
            # time & date register
            now = datetime.datetime.now()
            new_entry[name]["date"] = now.strftime("%x, %H:%M")

            # Genus registry
            register(new_entry, name, "genus")
            
            
            # Species Registry
            register(new_entry, name, "species")




            comb_entries = {**session_data, **new_entry}

            with open(f"./data/entries/{session_number}.json", "w") as file:
                json.dump(comb_entries, file, indent=2)

            
def register(dict, entry, key, type="i"):
    while True:
            match type:
                case "i":
                    user_input = input(f"What is the {key}?\n")
                    if user_input.strip and user_input.isprintable():
                        dict[entry][key] = user_input
                        break
                    else:
                        print("String empty, please try again")

                

                
            
            




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