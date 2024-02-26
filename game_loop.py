import World_State
import re
import state_updates
import save_game

def play_game(world_state):
    # MAIN FUNCTION within this module, that calls all other game_loop methods.
    # Coordinates the flow of game loop phase of our game.
    
    exit_state=False
    command = "None"
    
    # exit game conditions in the while loop
    while (world_state.get_game_won() == 'N') and (exit_state==False):
        
        # prints description to console for active_player=Y
        console_output(world_state)
        
        for charac in world_state.get_characters():
            # cycle through each character in game to get their command and process it
            
            command, command_type = command_input(world_state, charac)
            
            if command == "exit":
                # exit game condition, so break out of game loop
                exit_state=True
                break
                 
            # make updates to game based off validated command
            world_state=state_updates.state_update(world_state,charac,command,command_type)
            
        world_state.increment_turn() # all characters played their turn, next turn time
    
    # after game exited:
    if (world_state.get_game_won() == 'Y'): 
        print("You win!")
    else: 
        # runs on manual exit
        print("Goodbye.")


def console_output(world_state):
    # Prints to console out the description at active player's location
    
    print("-" * 30)
    print("\033[1mTurn Number: \033[0m",world_state.get_turn_number())
    
    #find active char based on active player flag = Y then find their coordinate
    active_char = world_state.get_active_char()
    current_coord =  active_char.get_coords()
    print("")
    print_minimap(world_state,current_coord,active_char)
    print("")
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
        
        # gets next command either from console or Character's method
        if charac.get_active_player() =='Y':
            command = input("Please enter your next action: ")
        else:
            command = world_state.get_next_action(charac)
        
        # do some command formatting cleansing here
        if command:

# ------------------------------------------
#       NOTE from john:  
#           I had to remove .lower() from command formatting because
#           our data is pretty inconsistent with upper/lower case
#           ie, 'kitchen' is all lowercase
#           while 'Wold' is capitalized
#           

            command = command.strip().lower()
            
        # Command processor checks, validates, formats the command. 
        # If the command is not valid, will keep getting new command until valid
        valid_command,command,command_type = command_processor(world_state,charac,command)

    # command was validated by command processor, so return formatted command for state update
    return (command, command_type) 


def command_processor(world_state,charac,command):

    # Based on the passed through string command and Character that submitted that command,
    # do any formatting for the command. So that we can pass formatted command to state_update function.
    # Function returns back a tuple containing:
    # 1. boolean, true=command is valid for state update, false=command not valid, need to ask for another command
    # 2. string, command formatted for state update (not sure if this is the only output)
    # 3. command_type, which tells state_update what type of command it is (basic, normal, advanced)
    
    basic_commands = {"n","s","e","w","inventory"}
    
    replacement_dict = {
        # use this to replace commands, so that more than one word can be recognized as same command
        "north":"n",
        "south":"s",
        "east":"e",
        "west":"w"
    }
    
    command = replacement_dict.get(command, command) 
    
    # validate the command, check for what kind of command it is, basic, common, advanced
    if command in basic_commands:
        # check if command is a basic command, based off basic_commands set
        return (True, command,"basic") 
    elif command == "save" or command == "save game":
        save_game.save_game(world_state)
        return (False, command, "basic")
    
    elif command == "cheat":
        # cheat mode command recognition
        if world_state.get_cheat_mode() == 'Y':
            world_state.set_cheat_mode('N')
            print("Cheat mode turned off")
        elif world_state.get_cheat_mode() == 'N':
            world_state.set_cheat_mode('Y')
            print("Cheat mode turned on")
        return (False, command, "basic")
    elif command is not None and command.startswith("cheat "):
        if world_state.get_cheat_mode() == 'Y':
            words = command.split()
            command_without_first_word = ' '.join(words[1:])
            return (True, command_without_first_word, "cheat")
        else:
            print("You're not allowed to do that, cheat mode is not activated.")
            return (False, command, "basic")

    
    else:
        # TO EXPAND this if statement to recognize more commands as valid, default rest to true for now

        # ****************************************************************
        # John: changed this to 'basic' for testing of interaction commands:
        # return (True, command,"To expand") 
        return (True, command,"basic") 
        # ****************************************************************

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
                if charac.get_type() == "player":
                    return charac.get_name()
        elif keyword == "rent_amount":
            return str(world_state.get_rent_amount())
        elif keyword == "rent_due_days_away":
            return str(world_state.get_rent_due_date())
        elif keyword=="gold":
            for charac in world_state.get_characters():
                if charac.get_type() == "player":
                    return charac.get_current_gold()

def print_minimap(world_state,coords,active_char):
    # Function handles printing one tile around the provided co-ord, assuming player is on co-ord.
    x,y = coords
        
    max_cols = len(world_state.get_tiles()[0])-1
    max_rows = len(world_state.get_tiles())-1
   
    if world_state.get_cheat_mode() == 'N':
        # print only 1 tile around active player with no cheat mode
        # first row ######################################################################################################
        if y-1 >=0:
            if x-1 >=0:
                print(print_tile (world_state.get_tiles()[x-1][y-1],world_state.get_npc_chars_at_tile((x-1,y-1))),end="")
            print(print_tile (world_state.get_tiles()[x][y-1],world_state.get_npc_chars_at_tile((x,y-1))),end="")
            if x+1 <= max_rows:
                print(print_tile (world_state.get_tiles()[x+1][y-1],world_state.get_npc_chars_at_tile((x+1,y-1))))
            else:
                print("") # reached end of row, prints new line
        
        # second row ######################################################################################################
        if x-1 >=0:
            print(print_tile (world_state.get_tiles()[x-1][y],world_state.get_npc_chars_at_tile((x-1,y))),end="")
        # active player is represented as a green X on the minimap:
        print ("\033[32m\033[1m X \033[0m",end="")
        if x+1 <= max_rows:
            print(print_tile (world_state.get_tiles()[x+1][y],world_state.get_npc_chars_at_tile((x+1,y))))
        else:
            print("") # reached end of row, prints new line
            
        # third row ######################################################################################################
        if y+1 <= max_cols:
            if x-1 >=0:
                print(print_tile (world_state.get_tiles()[x-1][y+1],world_state.get_npc_chars_at_tile((x-1,y+1))),end="")
            print(print_tile (world_state.get_tiles()[x][y+1],world_state.get_npc_chars_at_tile((x,y+1))),end="")
            if x+1<= max_rows:
                print(print_tile (world_state.get_tiles()[x+1][y+1],world_state.get_npc_chars_at_tile((x+1,y+1))))
            else:
                print("") # reached end of row, prints new line
    else:
        # cheat mode is activated, so we display the entire world map
        transposed_world_map= [list(row) for row in zip(*world_state.get_tiles())]

        for row in transposed_world_map:
            for tile in row:
                coords = tile.get_coords()
                x,y = coords
                
                if active_char.get_coords() == coords:
                    print ("\033[32m\033[1m X \033[0m",end="")
                else:
                    print (print_tile(tile, world_state.get_npc_chars_at_tile(coords)),end="")
                if x==max_rows:
                    print("") # reached end of row, prints new line
                
def print_tile (tile,characters):
    # given a provided tile or char, provide the character string to represent it as on mini-map
    if characters != []:
        # print C if theres any other char other than the player
        return " C "
    if tile.get_type() == "building":
        return " B "
    if tile.get_type() == "non-building" and tile.get_name() != "grasslands":
        return " ? "
    if tile.get_type() == "non-building":
        return " _ "
        

