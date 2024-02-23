import json
import DataHandler
import os
import datetime



blacklist = ["parse", "register"]


gill_types = dict(enumerate(["Adnate", "Adnexed", "Decurrent", "Emarginate", "Free", "Seceding", "Sinuate", "Subdecurrent"]))

current_session = None
    
def dropdownMenu(key, message):
    while True:
        print(f"Please select a {key} type:")
        for x in message:
            print(f"\t{x}:{message[x]}")
                            
        user_input = input()

        for x in message:
            if user_input == str(x) or user_input == message[x]:
                return message[x]
                                    
        print(f"String was not a valid {key} type, please try again")
        


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
            sdir = os.listdir("./data/sessions")
            time = datetime.datetime.now().strftime("%m-%d-%y")
            numb = 2
            for i in sdir:
                if time == i.rstrip(".dat"):
                    time = i.rstrip(".dat") + f" ({numb})"
                    loop = True
                    while loop:
                        for i in sdir:
                            if time == i.rstrip(".dat"):
                                time = time.rstrip(f" ({numb})") + f" ({numb + 1})"
                                numb += 1
                            else:
                                loop = False
                                break


            current_session = DataHandler.Session(time)
            current_session.dump()
        
        case "entry":
            
            if current_session:

                name = input("What would you like to call this entry?\n")

                gps = None
                date = datetime.datetime.now().strftime("%x, %H:%M")

                genus = input("What is the genus?\n")
                species = input("What is the species?\n")
                substrate = input("What is the substrate?\n")
                terrain = input("What is the terrain?\n")
                
                gill = dropdownMenu("gill", gill_types)

                other = input("Any other notes?\n")

                current_session.constructEntry(name, gps, date, genus, species, substrate, terrain, gill, other)

                current_session.dump()

            else:
                print("Session not found or not selected please select or create a new session.\n")
                return

                        
                    
                    

def sessions():
    global current_session
    
    clear()

    session_list = DataHandler.getSessions()

    while True:
        
        for i in session_list:
            if not current_session == None:
                if str(current_session.id) == i:
                    print(i + " (selected)")
                else:
                    print(i)
            else:
                print(i)

        raw_input = input("\nEnter session number to view or type \"back\"\n")

        if raw_input in session_list:
            clear()

            current_session = DataHandler.load(raw_input)

            entry_names = current_session.getEntryNames()

            for i in entry_names:
                print(i)
            
            entry_name = parse(input("\nPlease type the entry you'd like to view\nOr type \"back\" to return home\n"), entry_names)

            if entry_name == None:
                return

            clear()

            selected_entry = current_session.getEntry(entry_name)
            
            print(entry_name + ":")

            print(entryFormater("GPS", selected_entry.gps))
            print(entryFormater("Date", selected_entry.date))
            print(entryFormater("Genus", selected_entry.genus))
            print(entryFormater("Species", selected_entry.species))
            print(entryFormater("Substrate", selected_entry.substrate))
            print(entryFormater("Terrain", selected_entry.terrain))
            print(entryFormater("Gill", selected_entry.gill))
            print(entryFormater("Notes", selected_entry.other))
                
            
            parse(input())


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




def entryFormater(x, data):
    if not data:
        return f"\t{x}: N/A"
    elif len(data) > 150:
        message = data[:150] + "..."
        return f"\t{x}: {message}"
    else:
        return f"\t{x}: {data}"


def back():
    clear()


def get_json(path, data=None):
    if data:
        with open(f"./data/{path}.json", "w") as file:
            json.dump(data, file, indent=2)
    else:
        with open(f"./data/{path}.json", "r") as file:
            return json.load(file)

