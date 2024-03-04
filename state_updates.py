# import state_updates_interactions
import text_file_processor
import state_updates_interactions
import test

def state_update(world_state,charac,command,command_type):
    # Make the updates to world_state (and any other updates required) to process the command.
    # Command type is the type of command determined by command processor which determines what updates needs to be made.
    # Returns back updated world_state object
    
    # update char's visited field
    current_x,current_y = charac.get_coords()
    world_state=visited_updates(world_state,charac,current_x,current_y)
    
    # parse command and make updates
    if command_type == "basic":
        return basic_commands(world_state,charac,command)
    elif command_type == "normal":
        # to be done, these are normal interactions based off the JSON interaction array data.
        pass
    elif command_type == "advanced":
        # to be done, these are commands that are more specific and documented to be handled separately
        pass
    elif command_type == "cheat":
        world_state = world_state.cheat_mode(command,charac)
        return world_state
    else:
        # do nothing, just return original world state as command was not recognized but passed through command processor
        return world_state


def basic_commands(world_state,charac,command):
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
        world_state = test.interaction_commands(world_state, charac, command)

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
    object_string=""
    print("\033[1mInventory: \033[0m",end="")
        
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
    object_string += ". \033[1mGold: \033[0m"
    object_string += str(charac.get_current_gold()) +"."
        
    print(object_string)

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
            
# def interaction_commands(world_state,charac,command):
#     # lookup command (iteraction: ACTION ENTITY)



# # heres some quick steps that i think needs to be done to process an interaction.
# # when someone types for e.g. "open barn". We need to check:

# # 0. setup interaction command list/array:
#     # setup interaction array:
#     interaction_key = command.strip()

#     if interaction_key == "":
#         return None

#     interaction_array = interaction_key.split(maxsplit=1)

#     if len(interaction_array) < 2:
#         # invalid interaction, so do print message and return:
#         print("Command not recognized")
#         return world_state

# # 1. does the noun "barn" exist in the coord that the char is in? 
# #   if theres no barn in their coords, meaning tile, inventory of the tile, 
# #   or inventory of the character, characters in that tile 
# #   then reject the command

#     interac_noun = interaction_array[1]
#     current_x, current_y = charac.get_coords()

#     # found = False
#     found_interac_tile = False
#     found_interac_tile_inventory = False
#     found_interac_char = False
#     found_interac_char_inv = False


#     interac_name = ""
#     interac_general_type = ""

#     # check current tile matches 'interac_noun':
#     current_tl = world_state.get_tiles()[current_x][current_y]
    
#     if current_tl.get_name() == interac_noun:
#         # found tile named 'interac_noun'
#         found_interac_tile = True
#         interac_name = interac_noun
#         interac_general_type = "Tile"
#         interac_state = current_tl.get_state()

#         # (interac_general_type, \
#         #     current_tl.get_name(), current_tl.get_state(), interaction_array[0])


#     # if not tile, check tile inventory for match:
#     if not found_interac_tile:
#         tl_inv_list = current_tl.get_inventory()     
#         if len(tl_inv_list) > 0:
#             for inv_elem in tl_inv_list:
#                 if inv_elem.get_name() == interac_noun:
#                     found_interac_tile_inventory = True
#                     interac_name = interac_noun
#                     interac_general_type = "Object"
#                     interac_state = inv_elem.get_state()
#                     # track the tile object that matches
#                     tile_current_obj_found = inv_elem
#                     break

#     # if not tile and not in tile inventory, check character/npc on tile
#     if (not found_interac_tile) and (not found_interac_tile_inventory):
#          #et_chars_at_tile()
#         chars_list = world_state.get_chars_at_tile(charac.get_coords())
#         if len(chars_list) > 0:
#             for char_elem in chars_list:
#                 if char_elem.get_name() == interac_noun:
#                     found_interac_char = True
#                     interac_name = interac_noun
#                     interac_general_type = "Character"
#                     interac_state = char_elem.get_state()
#                     # track the character that matches
#                     tile_char_found = char_elem
#                     break

#     # if not tile, not in tile-inventory, not char/npc name, check char/npc inventory
#     if (not found_interac_tile) and (not found_interac_tile_inventory) and (not found_interac_char):
#         chars_list = world_state.get_chars_at_tile(charac.get_coords())
#         if len(chars_list) > 0:
#             for char_elem in chars_list:
#                 char_inv = char_elem.get_inventory()
#                 if len(char_inv) > 0:
#                     for inv_elem in char_inv:
#                         if inv_elem.get_name() == interac_noun:
#                             found_interac_char_inv = True
#                             interac_name = interac_noun
#                             interac_general_type = "Object"
#                             interac_state = inv_elem.get_state()
#                             break
#                 if found_interac_char_inv:
#                     break


#     # the interaction noun was not found, so print a message and return
#     if (not found_interac_tile) and (not found_interac_tile_inventory) and \
#         (not found_interac_char) and (not found_interac_char_inv):
#         print("Command not recognized")
#         return world_state



# # 2. if "barn" does exist in their coord, what is the state of the barn? and its general type?

#     if ( found_interac_tile) or ( found_interac_tile_inventory) or \
#         ( found_interac_char) or ( found_interac_char_inv):

#         print("DEBUG: current_tl.get_name() = ", current_tl.get_name())
#         print("DEBUG: current_tl.get_state() = ", current_tl.get_state())
#         print("DEBUG: current_tl.get_general_type() = ", current_tl.get_general_type())


# # 3. use def lookup_interaction (type, name, state, interaction_key) to grab the interaction data from JSON

#         int_JSON_obj = text_file_processor.lookup_interaction(interac_general_type, \
#             interac_name, interac_state, interaction_array[0])

#         print("DEBUG: int_JSON_obj: ")
#         print(int_JSON_obj)

# # 4. process the interaction based on data from 3.
 






        

#     return world_state






























#     # # old way: interac = text_file_processor.lookup_interaction_key_only(command)
#     # # new way: using Interaction object:
#     # interac_obj = text_file_processor.lookup_interaction_ret_object(command)

#     # if interac_obj is None:
#     #     print("I don't understand that command")
#     # else:
        
#     #     # for now, just debugging info

#     #     print("DEBUG: (interaction_commands()): interac_obj.get_entity_name(): ", \
#     #             interac_obj.get_entity_name() )
#     #     print("DEBUG: (interaction_commands()): interac_obj.get_entity_general_type(): ", \
#     #             interac_obj.get_entity_general_type())
#     #     print("DEBUG: (interaction_commands()): interac_obj.get_entity_state(): ", \
#     #             interac_obj.get_entity_state())
#     #     print("DEBUG: (interaction_commands()) -------------")
#     #     print("DEBUG: (interaction_commands()): interac_obj.get_interaction_data(): ", \
#     #             interac_obj.get_interaction_data())
#     #     print("DEBUG: (interaction_commands()): ")
        
#     #     interac_JSON_data = interac_obj.get_interaction_data()

#     #     print("\tchange_state_to: ", interac_JSON_data["change_state_to"])

#     #     int_requirements = interac_JSON_data["requirement"]

#     #     if len(int_requirements) > 0:
#     #        for req_elem in int_requirements:
#     #             print("\trequirement: ", \
#     #                     req_elem["type"], ",", req_elem["name"], ",", \
#     #                     req_elem["state"], ",", req_elem["qty"], ",", \
#     #                     req_elem["remove_obj"] )
                


