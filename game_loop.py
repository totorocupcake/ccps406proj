import state_updates
import save_game
import text_formatting
import classes.external_files as external_files
import classes.enums as Enum

def play_game(world_state):
    # MAIN FUNCTION within this module, that calls all other game_loop methods.
    # Coordinates the flow of game loop phase of our game.
    
    exit_state=False
    command = "None"
    
    while not world_state.get_game_won() and not exit_state:
        
        # prints description to console for active_player
        console_output(world_state)
        
        for charac in world_state.get_characters():
            # cycle through each character in game to get their command and process it
            
            command, command_type = command_input(world_state, charac)
            
            if command == "exit":
                exit_state=True
                break
                 
            # make updates to game based off validated command
            world_state=state_updates.state_update(world_state,charac,command,command_type)
            
            if world_state.get_game_won():
                break
            
        world_state = world_state.increment_turn()
    
    return world_state

def console_output(world_state):
    # Prints to console out the description at active player's location
    
    print("-" * 30)
    print("\033[1mTurn Number: \033[0m",world_state.get_turn_number())
    
    active_char = world_state.get_active_char()
    current_coord =  active_char.get_coords()
    
    print("")
    text_formatting.print_minimap(world_state,current_coord,active_char)
    print("")
    
    # get description based on coordinate of active player and parse it for dynamic text variables within string
    output=world_state.get_description(current_coord,active_char.get_visited())
    output = text_formatting.dynamic_variable_processor(world_state,output) 
    print(text_formatting.justify(output))
    print("")
    
def command_input(world_state,charac):
    # Based on the Character passed through and the world_state, generate either a scanf if activeplayer
    # or call charac.get_next_action() class method if its a computer controlled character.
    # Sends the command for command processing for validation and formatting.
    # Returns back a string which is the command to be sent for state update.
    
    valid_command=False
    
    while valid_command == False:
        # keep prompting for a command until command is valid
        
        if charac.get_active_player():
            command = input("Please enter your next action: ")
        else:
            command = world_state.get_next_action(charac)
        
        if command:
            command = command.strip().lower()
            
        # Command processor checks, validates, formats the command. 
        valid_command,command,command_type = command_processor(world_state,command,charac)
        
    # command was validated by command processor, so return formatted command for state update
    return (command, command_type) 


def command_processor(world_state,command,charac):
    # Based on the passed through string command and Character that submitted that command,
    # do any formatting for the command. So that we can pass formatted command to state_update function.
    # Function returns back a tuple containing:
    # 1. boolean, true=command is valid for state update, false=command not valid, need to ask for another command
    # 2. string, command formatted for state update
    # 3. command_type, which tells state_update what type of command it is (basic, normal, advanced)
    
    basic_commands = {"n","s","e","w","inventory","store gold","take gold","exit"}
    
    replacement_dict = {
        # use this to replace commands, so that more than one word can be recognized as same command
        "north":"n",
        "south":"s",
        "east":"e",
        "west":"w",
        "take eggs": "harvest chicken",
        "harvest eggs": "harvest chicken"
    }
    
    command = replacement_dict.get(command, command) 
    
    if command is not None and ' ' in command:
        verb= command.split(' ',1)[0]
        noun= command.split(' ',1)[1]
    else:
        verb=""
        noun=""
    
    if command in basic_commands:
        return (True, command,Enum.command_type.BASIC) 
    
    elif command == "save" or command == "save game":
        save_game.save_game(world_state)
        return (False, command, Enum.command_type.BASIC)
    
    elif command == "cheat":
        # cheat mode command recognition
        if world_state.get_cheat_mode():
            world_state.set_cheat_mode(False)
            print("Cheat mode turned off")
        else:
            world_state.set_cheat_mode(True)
            print("Cheat mode turned on")
        return (False, command, Enum.command_type.BASIC)
    
    elif command is not None and command.startswith("cheat "):
        if world_state.get_cheat_mode():
            return (True, noun, Enum.command_type.CHEAT)
        else:
            print("You're not allowed to do that, cheat mode is not activated.")
            return (False, command, Enum.command_type.CHEAT)

    elif noun in {text_formatting.dynamic_variable_processor(world_state,name).lower() for name in \
        external_files.read_external_files().get_unique_names()} and verb in external_files.read_external_files().get_unique_interactions():
        return (True, command,Enum.command_type.NORMAL) 
    
    elif command is None and not charac.get_active_player():
        return (True, command, Enum.command_type.BASIC)
        
    else:
        print("Command not recognized. Please try again.")
        return (False,command,Enum.command_type.BASIC)
    



