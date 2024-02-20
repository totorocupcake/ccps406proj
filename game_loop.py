import World_State

def play_game(world_state):
    # MAIN FUNCTION within this module, that calls all other game_loop methods.
    # Coordinates the flow of game loop phase of our game.
    
    command = "None"

    # exit game conditions on the while loop
    while (world_state.get_game_won() == "N") or (command != "exit"):
        
        # prints description to console for active_player=Y
        console_output(world_state)
        
        for charac in world_state.get_characters():
            # cycle through each character in game to get their command and process it
            command = command_input(world_state, charac)
            world_state=state_update(world_state,charac,command)


def console_output(world_state):
    # Prints to console out the description at active player's location
    
    for charac in world_state.get_characters():
        # Find the active player
        if charac.get_active_player()=='Y':
            current_coord= charac.get_coords()
            break # We found the active player so break out of loop
    
    print(world_state.get_description(current_coord),charac.get_visited())
    

def command_input(world_state,charac):
    # Based on the Character passed through and the world_state, generate either a scanf if activeplayer
    # or call charac.get_next_action() class method if its a computer controlled character.
    # Sends the command for command processing for validation and formatting.
    # Returns back a string which is the command to be sent for state update.
    
    valid_command=False
    
    while valid_command == False:
        # keep prompting for a command until command is valid
        
        if charac.get_active_player() =='Y':
            command = input("Please enter your next action: ")
        else:
            command = charac.get_next_action()
            
        command = command.strip()
        
        # Command processor validates and formats the command
        valid_command,command = command_processor(world_state,charac,command)

    # exitted loop, so return the valid and formatted command for state update
    return command 


def command_processor(world_state,charac,command):
    # Based on the passed through string command and Character that submitted that command,
    # do any formatting for the command. So that we can pass formatted command to state_update function.
    # Function returns back a tuple containing:
    # 1. boolean, true=command is valid for state update, false=command not valid, need to ask for another command
    # 2. string, command formatted for state update (not sure if this is the only output)
    
    
    pass

def state_update(world_state,charac,command):
    # Make the updates to world_state (and any other updates required) to process the command
    # Returns back updated world_state object
    
    common_commands = ["N","S","W","E","inventory","exit"]
    
    world_state.increment_turn()
    pass
        