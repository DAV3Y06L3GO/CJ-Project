primative = {"users", "entries", "help"}
twoStage = {"void", "new"}

def parse(raw_input):
    command_name, *arguments = raw_input.split()

    if command_name in globals() and callable(globals()[command_name]):
        stack = globals()[command_name]
        if arguments:
            stack(arguments[0])
        else:
            stack()
    else:
        return "Command not found, try again or type \"help\"."
    

def users():
    print("WAHOOO")