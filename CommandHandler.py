import json
import os



def screen_clear(): 
    os.system('cls' if os.name == 'nt' else 'clear')

def parse(raw_input, list=[]):
    if raw_input in list:
        for i in list:
            if raw_input == i:
                return i
    
    try: 
        command_name, *arguments = raw_input.split()
    except:
        print("Command empty, try again or type \"help\".")
        parse(input(), list=list)

    if command_name in globals() and callable(globals()[command_name]):
        stack = globals()[command_name]
        if arguments:
            stack(arguments[0])
            return
        else:
            stack()
            return
    else:
        print("Command not found, try again or type \"help\".")
        parse(input(), list=list)
    


def users():
    screen_clear()
    
    with open("./data/users.json", "r") as file:
        users_data = json.load(file)

    while True:
        user_list = []
        user_string = ""
        user_selected = ""
        for i in users_data["users"].keys():
            user_list.append(i)
            if users_data["users"][i] == True:
                user_string += "%s(selected)\n" % i
                user_selected = i
            else:
                user_string += i + "\n"

        print("Select a user: \n")
        print(user_string)
        print("Type \"back\" to return to the homescreen")

        requested_user = parse(input(), list=user_list)

        if requested_user in user_list:
            
            print("MATCHED")
            users_data["users"][user_selected] = False
            users_data["users"][requested_user] = True
            with open("./data/users.json", "w") as file:
                json.dump(users_data, file, indent=2)
                print("DUMPED")
        else:
            return
        
        screen_clear()
        print("%s has been selected" % requested_user)

def back():
    screen_clear()