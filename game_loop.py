import World_State
import re
import state_updates

def play_game(world_state):
    # MAIN FUNCTION within this module, that calls all other game_loop methods.
    # Coordinates the flow of game loop phase of our game.
    
    exit_state=False
    command = "None"
    
    # exit game conditions on the while loop
    while (world_state.get_game_won() == 'N') and (exit_state==False):
        
        # prints description to console for active_player=Y
        
        console_output(world_state)
        
        for charac in world_state.get_characters():
            # cycle through each character in game to get their command and process it
            command = command_input(world_state, charac)
            
            if command == "exit":
                exit_state=True
                break
            
            world_state=state_update(world_state,charac,command)
            
        world_state.increment_turn()


def console_output(world_state):
    # Prints to console out the description at active player's location
    
    print("Turn Number: ",world_state.get_turn_number())
    
    #find active char based on active player flag = Y then find their coordinate
    active_char = world_state.get_active_char()
    current_coord =  active_char.get_coords()
    
    # get description based on coordinate of active player and parse it for dynamic text variables within string
    output=world_state.get_description(current_coord,active_char.get_visited())
    output = dynamic_variable_processor(world_state,output) # formats dynamic variables in string
    
    print(output)

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
        
        if command:
            command = command.strip().lower()
        
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
    
    
    return (True, command) #for now, just return True with same command

def state_update(world_state,charac,command):
    # Make the updates to world_state (and any other updates required) to process the command
    # Returns back updated world_state object
    
    return state_updates.basic_commands(world_state,charac,command)
    
    #return world_state

def dynamic_variable_processor(world_state,get_desc_string):
    # Given a sentence string (from get_description()) replace any dynamic variables within our text files
    # with the relevant variable value from memory
    
    pattern = r'%([^%]+)%'
    
    get_desc_string = re.sub(pattern, lambda match: dynamic_variable_logic(world_state,match.group(1)), get_desc_string)
    
    return get_desc_string
    
def dynamic_variable_logic(world_state,keyword):
    # Given the keyword string, replace it with a value and return that value back
        
        if keyword == "player_name":
            for charac in world_state.get_characters():
                if charac.get_type == "player":
                    return charac.get_name()
        elif keyword == "rent_amount":
            return str(world_state.get_rent_amount())
        elif keyword == "rent_due_days_away":
            return str(world_state.get_rent_due_date())


    
    

