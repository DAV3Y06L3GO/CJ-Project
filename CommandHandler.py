import json
import DataHandler
import os
import datetime



blacklist = ["parse", "register"]


gill_types = dict(enumerate(["Adnate", "Adnexed", "Decurrent", "Emarginate", "Free", "Seceding", "Sinuate", "Subdecurrent"]))

current_session = None

def getLatestSessionNumb():
    session_list = os.listdir("./data/sessions")

    return len(session_list)
    
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
            numb = getLatestSessionNumb() + 1
            current_session = DataHandler.Session(numb)
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
    clear()

    session_list = os.listdir("./data/sessions/")
    
    while True:
        for i in range(len(session_list)):
            session_list[i] = session_list[i].rstrip(".dat")

            if current_session.id == session_list[i]:
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

