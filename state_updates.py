import text_formatting
import test

def state_update(world_state,charac,command,command_type,data):
    # Make the updates to world_state (and any other updates required) to process the command.
    # Command type is the type of command determined by command processor which determines what updates needs to be made.
    # Returns back updated world_state object
    
    # update char's visited field
    current_x,current_y = charac.get_coords()
    world_state=visited_updates(world_state,charac,current_x,current_y)
    
    # parse command and make updates
    if command_type == "basic":
        return basic_commands(world_state,charac,command,data)
    elif command_type == "normal":
        # to be done, these are normal interactions based off the JSON interaction array data.
        pass
    elif command_type == "advanced":
        # to be done, these are commands that are more specific and documented to be handled separately
        pass
    elif command_type == "cheat":
        world_state = world_state.cheat_mode(command,charac,data)
        return world_state
    else:
        # do nothing, just return original world state as command was not recognized but passed through command processor
        return world_state


def basic_commands(world_state,charac,command,data):
    #added:
    directions_set = {"n","s","w","e"}
    
    if command=="inventory":
        print_inventory(charac) # prints character's inventory
        
    elif command in directions_set:
        world_state=process_movement(world_state,charac,command) # moves character based on n,s,e,w input
    
    elif command == "store gold" or command== "take gold":
        world_state=process_store_gold(world_state,charac,command) # stores/takes character's gold if at bedroom
    
    # added: for dealing with 'interaction' commands
    elif command is not None:
        world_state = test.interaction_commands(world_state, charac, command,data)

    for char in world_state.get_characters():
        # check after state updates if game is won, update flag if so in world state
        if char.get_name() == 'landlord':
            if char.get_state() == 'happy':
                world_state.set_game_won('Y')
            break
            
    return world_state

def visited_updates (world_state,charac,x,y):
    # this function updates the given charac's visited field
    # based on new location visited at coord x, y
    
    # get and update for the new tile visited
    new_tile_visited = world_state.get_tiles()[x][y]
    charac.update_visited("Tile",new_tile_visited.get_name(),new_tile_visited.get_state())
            
    # add any objects within tile's inventory      
    new_tile_objs_visited = new_tile_visited.get_inventory()
    for obj in new_tile_objs_visited:
        charac.update_visited("Object",obj.get_name(),obj.get_state())
        
    # add any characters on the same tile
    new_chars_visited = world_state.get_chars_at_tile((x,y))
    for char in new_chars_visited:
        if char != charac:
            charac.update_visited("Character",char.get_name(),char.get_state())
    
    return world_state

def print_inventory(charac):
    # This function prints character's inventory and gold to console
    object_string="Inventory: "
        
    for obj in charac.get_inventory():
        # loop through each item in character's inventory
            
        object_string+=obj.get_name()
        
        if obj.get_state() != "null":
            # append obj state if not null
            object_string+=" ("+ obj.get_state() + ")"
        
        # append x[quantity] after each item
        object_string+=" x"
        object_string+=str(obj.get_quantity())
            
        # append comma between items
        object_string+=", "
        
    # remove dangling comma added at end of last item
    object_string = object_string[:-2]
        
    # Append character's gold amount to end of string:
    object_string += ". Gold: "
    object_string += str(charac.get_current_gold()) +"."
    print("")
    print(text_formatting.justify(object_string))

def process_movement(world_state,charac,command):
    # This function moves the character coordinate based on n,s,e,w command
    x,y = charac.get_coords()
        
    if command == "n":
        y-=1
    elif command == "s":
        y+=1
    elif command == "w":
        x-=1
    elif command == "e":
        x+=1

    max_cols = len(world_state.get_tiles()[0])-1
    max_rows = len(world_state.get_tiles())-1
        
    if x<=max_rows and x>= 0 and y>=0 and y<=max_cols:
        # if coord is valid, move character to new coord
        # print(f"{charac.get_name()} moved to {x} {y}")
        charac.update_coords((x,y))
    else:
        # only print to console if its the active player turn
        if charac.get_active_player()=='Y':
            print("You cannot go there.") 
    return world_state

def process_store_gold(world_state,charac,command):
    # This function stores character's gold into the tile if they are at an open bedroom tile
    coord= charac.get_coords()
    x,y=coord
    current_tile = world_state.get_tiles()[x][y]
    words=command.split()
        
    if current_tile.get_name() == "bedroom" and current_tile.get_state() == "open" and (charac.get_type() == "player" or \
    charac.get_name() == "Thief"):
    # can only store gold if they are located at an open bedroom and the character is the player or thief 
    # (other npcs cannot store/take gold into the player's house as the house doesnt belong to them)
        
        if words[0]=="store":
            take_gold_entity = charac
            receive_gold_entity = current_tile
        else:
            take_gold_entity = current_tile
            receive_gold_entity = charac
        
        gold_to_take = take_gold_entity.get_current_gold()
        
        if gold_to_take > 0:    # check if there is gold to take first
            # swaps gold between take and e
            # receiving entity
            take_gold_entity.increment_current_gold(gold_to_take*-1)
            receive_gold_entity.increment_current_gold(gold_to_take)
            
            if charac.get_active_player()=='Y':
                print(f"You {words[0]} {gold_to_take} {'from' if words[0] == 'take' else 'into'} your bedroom's chest. Remember to lock your house to keep your gold safe!")   
       
        else:   # no gold to take, so no need to process command further
            if charac.get_active_player()=='Y':
                print(f"You don't have any gold to {words[0]}.")
    else:
        # not currently in open bedroom or not the player or thief so they shouldnt be able to do this
        print(f"You cannot {words[0]} gold here.")
    return world_state

