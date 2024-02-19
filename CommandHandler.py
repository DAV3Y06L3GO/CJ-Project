import json
import DataHandler
import os
import datetime



blacklist = ["parse", "register"]


gill_types = dict(enumerate(["Adnate", "Adnexed", "Decurrent", "Emarginate", "Free", "Seceding", "Sinuate", "Subdecurrent"]))

current_session = None

def getLatestSessionNumb():
    session_list = os.listdir("./data/sessions/")

    return len(session_list)
    

    


def clear(): 
    os.system('cls' if os.name == 'nt' else 'clear')


def parse(raw_input, list=[]):
    try:
        if raw_input in str(list):
            return raw_input
    except TypeError as error:
        print(error)
        return parse(input(), list=list)

    
    try: 
        command_name, *arguments = raw_input.split()
    except:
        print("Command empty, try again or type \"help\".")
        return parse(input(), list=list)

    if command_name in globals() and callable(globals()[command_name]) and not command_name in blacklist:
        stack = globals()[command_name]
        if arguments:
            return stack(arguments[0])
        else:
            try: 
                return stack() 
            except TypeError as error:
              print(error)
              print("Given command is missing a parameter")
              return parse(input(), list=list)
    else:
        print("Command not found, try again or type \"help\".")
        return parse(input(), list=list)





def new(arg):
    clear()
    global current_session

    match arg:
        case "user":
            #new user screen
            while True:
                new_user = input("Enter name of new user: ").strip()
                if new_user and new_user.isprintable():
                    if input(f"Create a new user named {new_user}? (y/n)") in ["yes", "y"]:
                        
                        users_data = get_json("users")

                        for i in users_data.keys():
                            if users_data[i] == True:
                                users_data[i] = False
                        
                        users_data[new_user] = True

                        get_json("users", users_data)
                        
                        print(f"{new_user} has been created and selected\nType \"back\" to return home")
                        parse(input())
                        return
                else: print("Sorry the given user name is invalid please pick a different name")
        
        case "session":
            numb = getLatestSessionNumb() + 1
            current_session = DataHandler.Session(numb)
            current_session.dump()
        
        case "entry":
            
            try: 
                session_data = get_json("sessions/" + str(session_number))
            except NameError:
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

            # Substrate Registry
            register(new_entry, name, "substrate")

            # Habitat Registry
            register(new_entry, name, "terrain")

            # Gill Registry
            register(new_entry, name, "gill", "d", gill_types)

            # other
            register(new_entry, name, "other", message="Any other notes?")


            comb_entries = {**session_data, **new_entry}

            get_json("sessions/" + session_number, comb_entries)

            
def register(dict, entry, key, type="i", message=None):
    while True:
            match type:
                case "i":
                    if message:
                        print(message)
                    else:
                        print(f"What is the {key}?")
                    user_input = input()

                    if user_input.strip and user_input.isprintable():
                        dict[entry][key] = user_input
                        return
                    else:
                        print("String empty, please try again")
                
                case "d":
                    print(f"Please select a {key} type:")
                    for x in message:
                        print(f"\t{x}:{message[x]}")
                    
                    user_input = input()

                    for x in message:
                        if user_input == str(x) or user_input == message[x]:
                            dict[entry][key] = message[x]
                            return
                    print(f"String was not a valid {key} type, please try again")
                        
                    
                    

def sessions():
    global session_number
    clear()

    session_list = os.listdir("./data/sessions/")
    
    while True:
        for i in range(len(session_list)):
            session_list[i] = session_list[i].rstrip(".json")

            if session_number == session_list[i]:
                print("Session #" + session_list[i] + "(selected)")
            else:
                print("Session #" + session_list[i])
        
        raw_input = input("\nEnter session number to view or type \"back\"\n")
        session_number = raw_input

        if raw_input in session_list:
            session_data = get_json("sessions/" + raw_input)
            
            for i in session_data.keys():
                print(i)
            
            entry_name = parse(input("\nPlease type the entry you'd like to view\nOr type \"back\" to return home\n"), session_data.keys())

            clear()

            if entry_name: 
                selected_entry = session_data[entry_name]
            else:
                return
            
            print(entry_name + ":")
            for x in selected_entry:
                
                if not selected_entry[x]:
                    print(f"\t{x}:N/A")
                elif len(selected_entry[x]) > 150:
                    message = selected_entry[x][:150] + "..."
                    print(f"\t{x}:{message}")
                else:
                    print(f"\t{x}:{selected_entry[x]}")
            
            topic = parse(input("\nType the name of a topic to edit it or type \"back\" to return\n"), selected_entry.keys())

            if topic: 
                session_data[entry_name][topic] = input("%s:\n\t%s: " % (entry_name, topic))
            else:
                return
            
            get_json("sessions/" + raw_input, session_data)
            
            clear()
            return


        elif raw_input == "back":
            back()
            return
        else:
            print("Invalid Session please try again")


    
    




def users():
    clear()
    
    users_data = get_json("users")

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
            
            get_json("users", users_data)
        else:
            return
        
        clear()
        print(f"{requested_user} has been selected")


def back():
    clear()


def get_json(path, data=None):
    if data:
        with open(f"./data/{path}.json", "w") as file:
            json.dump(data, file, indent=2)
    else:
        with open(f"./data/{path}.json", "r") as file:
            return json.load(file)

