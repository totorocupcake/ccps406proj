import text_file_processor
import classes.Object as Object
import game_initialization

# need for function" dynamic_variable_processor" to process %_% variables
import game_loop


def interaction_commands(world_state,charac,command):
    # lookup command (iteraction: ACTION ENTITY)



#-------------------------------------------------------------------------
# 0. setup interaction command list/array:
#       setup interaction array:
#-------------------------------------------------------------------------

    interaction_key = command.strip()

    # check for empty string in interaction key/command:
    if interaction_key == "":
        print("Command not recognized")
        return world_state
        # return None

    interaction_array = interaction_key.split(maxsplit=1)

    if len(interaction_array) < 2:
        # invalid interaction, so do print message and return:
        print("Command not recognized")
        return world_state




#-------------------------------------------------------------------------
# 1. does the noun, e.g. "barn", exist in the coord that the char is in? 
#   if theres no barn in their coords, meaning tile, check inventory of the tile, 
#   or character in that tile, inventory of the character.
#   If not found, then reject the command
#-------------------------------------------------------------------------

    interac_noun = interaction_array[1]
    interac_noun = interac_noun.lower()

    interac_verb = interaction_array[0]
    interac_verb = interac_verb.lower()

    current_x, current_y = charac.get_coords()

    # set found = False (for each of tile, tile inv., char, char inv.)
    found_interac_tile = False
    found_interac_tile_inventory = False
    found_interac_char = False
    found_interac_char_inv = False
    
    # needed for processing advanced state change interaction
    advanced_change_state_to = False

    found_obj_inv_list = []

    # used for interaction lookup:
    interac_name = ""
    interac_general_type = ""
    interac_type = ""

    # ------
    # 1. (a) 
    # check current tile matches 'interac_noun':
    current_tl = world_state.get_tiles()[current_x][current_y]
    
    if current_tl.get_name().lower() == interac_noun:
        # found tile named 'interac_noun', so update interac_ data:
        found_interac_tile = True
        interac_name = interac_noun
        interac_general_type = "Tile"
        interac_state = current_tl.get_state()


    # ------
    # 1. (b) 
    # if not tile, check tile inventory for match:
    if not found_interac_tile:
        tl_inv_list = current_tl.get_inventory()     
        if len(tl_inv_list) > 0:
            for inv_elem in tl_inv_list:
                if inv_elem.get_name().lower() == interac_noun:
                    # found in tile inventory, so update interac_ data:
                    found_interac_tile_inventory = True
                    interac_name = interac_noun
                    interac_general_type = "Object"
                    interac_state = inv_elem.get_state()
                    # track the tile object that matches
                    tile_current_obj_found = inv_elem
                    break


    # ------
    # 1. (c) 
    # if not tile and not in tile inventory, check character on tile
    if (not found_interac_tile) and (not found_interac_tile_inventory):
        chars_list = world_state.get_chars_at_tile(charac.get_coords())
        if len(chars_list) > 0:
            for char_elem in chars_list:
                if char_elem.get_name().lower() == interac_noun:
                    # found matching character, so update interac_ data:
                    found_interac_char = True
                    interac_name = interac_noun
                    interac_general_type = "Character"
                    interac_type = char_elem.get_type()
                    interac_state = char_elem.get_state()
                    # track the character that matches
                    tile_char_found = char_elem

                    # print("\t\tDEBUG: found_interac_char : ", char_elem.get_name().lower(), ",", char_elem.get_type())

                    break


    # ------
    # 1. (d) 
    # if not tile, not in tile-inventory, not char name, check charac inventory
    if (not found_interac_tile) and (not found_interac_tile_inventory) and (not found_interac_char):

        charac_inv = charac.get_inventory()
        if len(charac_inv) > 0:
            for inventory_elem in charac_inv:
                if inventory_elem.get_name().lower() == interac_noun:
                    found_interac_char_inv = True
                    interac_name = interac_noun
                    interac_general_type = "Object"
                    interac_state = inventory_elem.get_state()


                    #----------------------------------------------------------
                    # NOTE: special case for 'take' interaction:
                    #   if object is in inventory and try to 'take', print 
                    #   message and return world_state:
                    #----------------------------------------------------------

                    if interac_verb == "take":
                        print(interac_noun, "is already in inventory.")
                        return world_state

                    break

      



    # ------
    # 1. (e) 
    # the interaction noun was not found, so print an 'error' message and return
    if (not found_interac_tile) and (not found_interac_tile_inventory) and \
        (not found_interac_char) and (not found_interac_char_inv):
        print("Command not recognized")
        return world_state











#-------------------------------------------------------------------------
# 2. if "barn" (interac_noun) does exist in their coord, what is the state of the barn? and its general type?
#       we updated state and general type in code above ^
#    If found, we are ready to lookup the interaction in Step 3 below
#-------------------------------------------------------------------------

    if ( found_interac_tile) or ( found_interac_tile_inventory) or \
        ( found_interac_char) or ( found_interac_char_inv):












#-------------------------------------------------------------------------
# 3. use def lookup_interaction (type, name, state, interaction_key) 
#       to grab the interaction data from JSON
#-------------------------------------------------------------------------

        # print("\t\tDEBUG: charac.get_type(): ", charac.get_type())
        # print("\t\tinterac_type = ", interac_type)

        if interac_type == "player":
            interac_name = "%player_name%"

        int_JSON_obj = text_file_processor.lookup_interaction(interac_general_type, \
            interac_name, interac_state, interaction_array[0])

        # print("DEBUG: int_JSON_obj: ")
        # print(int_JSON_obj)


        # ----------------------------
        # if interaction was not found, print message and return:
        if int_JSON_obj is None:
            # print()
            print("Command not recognized")
            # print()
            return world_state











#-------------------------------------------------------------------------
# 4. process the interaction based on data from Step 3.
#-------------------------------------------------------------------------
 
        # ------
        # 4. (a) 
        # check for requirements, if any:
        requirements_satisfied = False

        # ----------
        # 4. (a) (i)
        # if no requirements, assume requirements are satisfied:
        if int_JSON_obj["requirement"] is None:
            
            # print("DEBUG: int_JSON_obj['requirement'] = None")

            requirements_satisfied = True

        else:
            # print("DEBUG: int_JSON_obj['requirement'] (Not None) = ", int_JSON_obj["requirement"])

        # ----------
        # 4. (a) (ii)
        # else, check all requirements in array, for each type of requirement:
        #   'Gold', 'Character', 'object/item', 'tile'
            found_gold_req = True
            found_char_req = True
            found_obj_req = True
            tile_req_satisfied = True



# ======================================================
#   for 'object' requirements, there can potentially be 
#   more than one, eg,
#       'honey' requires: 'bee smoker' and 'beekeeping suit'
#   need to count and keep track of number of object requirements
#       
            obj_req_count = 0
            found_multiple_obj_req = 0
            for req_elem in int_JSON_obj["requirement"]:
                if req_elem["type"].lower() == "object":
                    obj_req_count += 1





            for req_elem in int_JSON_obj["requirement"]:

                
                # ----------
                # 4. (a) (ii) (I)
                #   check 'object' requirements, must be in charac's inventory:
                if req_elem["type"].lower() == "object":

                    found_obj_req = False

                    act_char = charac
                    act_char_inv = act_char.get_inventory()
                    
                    if obj_req_count == 1:

                        if len(act_char_inv) > 0:
                            for inv_elem in act_char_inv:
                                if (inv_elem.get_name().lower() == req_elem["name"]) and \
                                    (inv_elem.get_quantity() >= req_elem["qty"]):
                                    found_obj_req = True 
                                    break
                        if not found_obj_req:
                            requirements_satisfied = False
                            break

                    # more than one object is required in inventory:
                    else: 

                        # found_multiple_obj_req = 0
                        if len(act_char_inv) > 0:
                            for inv_elem in act_char_inv:
                                if (inv_elem.get_name().lower() == req_elem["name"]) and \
                                    (inv_elem.get_quantity() >= req_elem["qty"]):
                                    found_multiple_obj_req += 1
                                    break











                # ----------
                # 4. (a) (ii) (II)
                #   check 'tile' requirements, must be on tile-state:
                elif req_elem["type"].lower() == "tile":

                    


                # ----------
                # 4. (a) (ii) (II.1)
                #   Advanced Requirement Processing:
                #   check for CHANGE_STATE_TO substring in requiements-state

                    tile_req_satisfied = False                    

                    advanced_change_state_to = False
                    substring = "CHANGE_STATE_TO"
                    index = req_elem["state"].find(substring)
                    if index != -1:

                        print()
                        advanced_change_state_to = True
                        change_state_to_str_arr = req_elem["state"].split()
                        print("DEBUG: change_state_to_str_arr[0] = ", change_state_to_str_arr[0])
                        print("DEBUG: change_state_to_str_arr[1] = ", change_state_to_str_arr[1])
                        print("DEBUG: change_state_to_str_arr[2] = ", change_state_to_str_arr[2])

                        tile_to_update = world_state.get_tile_by_name(req_elem["name"])

                        print("DEBUG:")
                        print("DEBUG: tile_to_update.get_state() = ", tile_to_update.get_state())
                        print("DEBUG:")
                        
                        if tile_to_update.get_state() == change_state_to_str_arr[0]:
                            tile_req_satisfied = True

                            new_tile_name = req_elem["name"]
                            new_tile_state = change_state_to_str_arr[2]
                        else:
                            tile_req_satisfied = False

                    else:  # not a "CHANGE_STATE_TO" requirement, just check current tile:
                        if req_elem["name"].lower() == current_tl.get_name().lower():
                            tile_req_satisfied = True
                        else:
                            tile_req_satisfied = False




                    #         print("DEBUG:")
                    #         print("DEBUG: new_tile_state = ", new_tile_state)
                    #         print("DEBUG:")
                       
                    #         new_tile_id = text_file_processor.lookup_tileID_by_name_state(new_tile_name, new_tile_state)
                            
                    #         new_tile = load_Tiles_temp.get_tile_by_name_and_state(new_tile_name,new_tile_state)
                            
                    #         # not sure if this is needed, but:
                    #         new_tile.set_tile_id(new_tile_id)

                    #         new_tile.update_coords(tile_to_update.get_coords())

                    #         world_state.update_tile(new_tile.get_coords(), new_tile)
                    #     else:
                            # tile_req_satisfied = False
                    # else: 
                        

                    #     new_tile_name = current_tl.get_name().lower()
                    #     new_tile_state = int_JSON_obj["change_state_to"]

                    #     new_tile_id = text_file_processor.lookup_tileID_by_name_state(new_tile_name, new_tile_state)
                    #     new_tile = load_Tiles_temp.get_tile_by_name_and_state(new_tile_name,new_tile_state)
                    #     new_tile.set_tile_id(new_tile_id)

                    #     new_tile.update_coords( world_state.get_tile_by_name(new_tile_name).get_coords())


                    # # update the tile in world_state:
                    # world_state.update_saved_tiles("add", world_state.get_tile_by_name(current_tl.get_name().lower()))
                    
                    # world_state.update_tile(new_tile.get_coords(), new_tile)





                # ----------
                # 4. (a) (ii) (III)
                #   check 'Gold' requirements:
                #       pay / steal requirement type = "Gold":
                elif req_elem["type"] == "Gold":
                    found_gold_req = False


                    # ----------
                    # 4. (a) (ii) (III.1)
                    #   pay landlord:

                    if int_JSON_obj["name"].lower() == "pay":

                        # print("DEBUG: int_JSON_obj['requirement'] = ", int_JSON_obj["requirement"])

                        rent_amount = game_loop.dynamic_variable_processor(world_state, str(req_elem["qty"]))

                        # print("\tDEBUG: rent_amount =", rent_amount)
                        # print("\tDEBUG: charac.get_current_gold() = ", charac.get_current_gold())

                        if charac.get_current_gold() >= int(rent_amount):
                            found_gold_req = True
                            charac.increment_current_gold( (-1) * int(rent_amount))
                            # print()
                            # print("\tDEBUG: charac.get_current_gold() = ", charac.get_current_gold())

                    # ----------
                    # 4. (a) (ii) (III.2)
                    #   steal from player:
                    elif int_JSON_obj["name"].lower() == "steal":   
                        steal_amount = game_loop.dynamic_variable_processor(world_state, str(req_elem["qty"]))
                        
                        steal_amount = int(steal_amount)

                        active_char = world_state.get_active_char()
                        total_gold = active_char.get_current_gold()
                        if total_gold >= steal_amount:
                            found_gold_req = True



                # ----------
                # 4. (a) (ii) (IV)
                #   check "Character" requirement, npc must be on tile
                elif req_elem["type"] == "Character":

                    npc_at_tile_list = world_state.get_npc_chars_at_tile(charac.get_coords())

                    found_char_req = False

                    if len(npc_at_tile_list) > 0:
                        for npc_elem in npc_at_tile_list:
                            if npc_elem.get_name().lower() == req_elem["name"].lower() and npc_elem.get_state().lower() == req_elem["state"].lower():
                                # print("\tDEBUG: found required Character: ", npc_elem.get_name())
                                found_char_req = True




# ======================================================
#   for 'object' requirements, there can potentially be 
#   more than one, eg,
#       'honey' requires: 'bee smoker' and 'beekeeping suit'
#   need to count and keep track of number of object requirements
#

            if (obj_req_count > 1) and (obj_req_count == found_multiple_obj_req):
                found_obj_req = True




            # ----------
            # 4. (a) (ii) (cont.)
            #   since there can be more than one requirement, need to use 'and' 
            if found_obj_req and tile_req_satisfied and found_char_req and found_gold_req:
                # print("\tDEBUG: requirements satisfied")
                requirements_satisfied = True








#-------------------------------------------------------------------------
# 5. if all requirements are satisfied, begin processing the interaction:
#       (a) advanced change state
#       (b) 'normal' change state to, ie, for (tile, char, obj)
#       (c) change_state_to = 'delete' situation (char, obj)
#       (d) process the interaction's 'obtain' field
#       
#-------------------------------------------------------------------------
 

        if requirements_satisfied:
            
            # ----------
            # 5. (a) 
            #    advanced change state: 
            if advanced_change_state_to == True and tile_req_satisfied == True:

                print("DEBUG:")
                print("DEBUG: new_tile_state = ", new_tile_state)
                print("DEBUG:")
            
                new_tile_id = text_file_processor.lookup_tileID_by_name_state(new_tile_name, new_tile_state)
                
                new_tile = game_initialization.get_tile_by_name_and_state(new_tile_name,new_tile_state)
                
                # not sure if this is needed, but:
                new_tile.set_tile_id(new_tile_id)

                new_tile.update_coords(tile_to_update.get_coords())

                world_state.update_tile(new_tile.get_coords(), new_tile)


            # ----------
            # 5. (b) 
            #    'normal' change state: 
            #    if current state == change_state_to, don't bother 
            #    updating state info
            if int_JSON_obj["change_state_to"] != interac_state:


                # ----------
                # 5. (b) (i)
                #   update the state for Tile in World_State:
                if interac_general_type == "Tile":

                    # save tile to restore later:
                    prev_tile = world_state.get_saved_tile_by_name(current_tl.get_name().lower())
                    if prev_tile is not None:
                        world_state.update_saved_tiles("remove", prev_tile)
                        found_prev_tile = True
                        new_tile = prev_tile
                    else:

                    # update current tile's state in World_State

                        new_tile_name = current_tl.get_name().lower()
                        new_tile_state = int_JSON_obj["change_state_to"]

                        new_tile_id = text_file_processor.lookup_tileID_by_name_state(new_tile_name, new_tile_state)
                        new_tile = game_initialization.get_tile_by_name_and_state(new_tile_name,new_tile_state)
                        new_tile.set_tile_id(new_tile_id)

                        new_tile.update_coords( world_state.get_tile_by_name(new_tile_name).get_coords())


                    # update the tile in world_state:
                    world_state.update_saved_tiles("add", world_state.get_tile_by_name(current_tl.get_name().lower()))
                    
                    world_state.update_tile(new_tile.get_coords(), new_tile)
                    
                    print("DEBUG: change_state_to: ", int_JSON_obj["change_state_to"])
                    print("\tDEBUG: need to replace appropriate tile info in World_State based on 'change_state_to' info")
                    
                    print("DEBUG: current_tl.get_name().lower()", current_tl.get_name().lower())
                    print("DEBUG: current_tl.get_state()", current_tl.get_state())
                    print("DEBUG: current_tl.get_tile_id()", current_tl.get_tile_id())
                    print("DEBUG: interac_state", interac_state)
                    print()
                    print("DEBUG: new_tile.get_name().lower()", new_tile.get_name().lower())
                    print("DEBUG: new_tile.get_state()", new_tile.get_state())
                    print("DEBUG: new_tile.get_tile_id()", new_tile.get_tile_id())
                    print()

#************************************************************************************                       

                    world_state.update_tile(new_tile.get_coords(), new_tile)

                    # debug only:
                    print("DEBUG: world_state.get_tiles()[current_x][current_y].get_state() = ", \
                        world_state.get_tiles()[current_x][current_y].get_state())
                    

                    pass 

                # ----------
                # 5. (b) (ii)
                #   update the state for Character in World_State:
                elif interac_general_type == "Character":
                    # find and update the character's state in World_State
                    #     interac_name
                    #     interac_state
                    char_on_tile = world_state.get_chars_at_tile(current_tl.get_coords())

                    if len(char_on_tile) > 0:
                        for char_elem in char_on_tile:
                            if char_elem.get_name().lower() == interac_name:
                                world_state.remove_character(char_elem)

                                new_char_state = int_JSON_obj["change_state_to"]
                                char_elem.set_state(new_char_state)
                                                                
                                world_state.spawn_character(char_elem)

                                # debug only:
                                print("DEBUG: Update Char state: ", char_elem.get_name().lower(), ",", char_elem.get_state())

# ******
# ****** Delete character from game if int_JSON_obj["change_state_to"] == "delete":
# ******

                                if int_JSON_obj["change_state_to"] == "delete":
                                    world_state.remove_character(char_elem)

                                    break
                    

                # ----------
                # 5. (b) (ii)
                #   update the state for Object in World_State:
                else:  # interac_general_type == "Object"                    
                    
                    # ----------
                    # 5. (b) (ii) (I)
                    #    first, if it was in tile's inventory, update there:
                    if found_interac_tile_inventory:

                        # print("DEBUG: found in Tile inventory")

# ******
# ****** Delete object/item from current Tile's inventory and add to char's inventory:
# ******

                        # ----------
                        # 5. (c) (i)
                        #   if 'delete', remove object from tile inventory
                        if int_JSON_obj["change_state_to"] == "delete":


                            # delete the item from the current tile's inventory, 
                            # if its there                            
                            tl_obj_inv_list = current_tl.get_inventory()

                            if len(tl_obj_inv_list) > 0:
                                for obj_elem in tl_obj_inv_list:
                                    if obj_elem.get_name().lower() == interac_name:
                                        # remove that object from tile's inventory
                                        found_obj_inv_list.append(obj_elem)
                                        # obj_list = []

                                        # obj_list.append(obj_elem)
                                        current_tl.update_inventory("remove", found_obj_inv_list)

# ********
# NOTE: this might not be the right place for this - should be in 'obtains' code:
#           * code moved to obtains section *
# ****
# add item/object to character's inventory list
# ********        

                                        break

                             # then update the tile in World_State:
                            world_state.update_tile(current_tl.get_coords(), current_tl)


                            # print()
                            # print("DEBUG: removed object from Tile's inventory and World_State updated")
                            # print("DEBUG: add object to character's inventory and World_State updated")


                            # print()
                            # print(int_JSON_obj["success_desc"])
                            # print()



                            # world_state.get_tiles()[current_x][current_y]

                    # # debug only:
                    # print("DEBUG: world_state.get_tiles()[current_x][current_y].get_state() = ", \
                    #     world_state.get_tiles()[current_x][current_y].get_state())

  






# ------------------------
# if 'change_state_to': 'delete', then remove from charac's inventory
# ------------------------


                    # ----------
                    # 5. (c) (ii)
                    #   if 'delete', remove object from char inventory
                    #   it was in a character's inventory, update there:
                    elif found_interac_char_inv:  
                        # print("DEBUG: found in character's inventory: found_interac_char_inv = True")

                        if int_JSON_obj["change_state_to"] == "delete":
                            item_to_delete_list = []
                            char_inv = charac.get_inventory()
                            if len(char_inv) > 0:
                                for inv_elem in char_inv:
                                    if inv_elem.get_name().lower() == interac_noun.lower():
                                        item_to_delete_list.append(inv_elem)
                                        world_state.remove_character(charac)
                                        charac.update_inventory("remove", item_to_delete_list)
                                        world_state.spawn_character(charac)

                                        


# -----------------------------------------------------
# 'obtain' field:
# -----------------------------------------------------



            # ----------
            # 5. (d)
            #   process the interaction's 'obtain' field                    
            if int_JSON_obj["obtain"] is not None:

# DEBUG: 
            # print("Obtains:")
            # print("\t", int_JSON_obj["obtain"])

                # if found_obj_inv_list is not None:
                #     print("\tDEBUG: found_obj_inv_list[0].get_name().lower() = ", found_obj_inv_list[0].get_name().lower())
                #     print("\tDEBUG: found_obj_inv_list[0].get_state() = ", found_obj_inv_list[0].get_state())
                #     print("\tDEBUG: found_obj_inv_list[0].get_quantity() = ", found_obj_inv_list[0].get_quantity())

                obtain_obj_list = []
                
    # iteratate through the obtains list, add items to a list of objects:
                for obtain_elem in int_JSON_obj["obtain"]:


                    # ----------
                    # 5. (d) (i)
                    #   if obtain is an item/object:
                    if (obtain_elem["type"].lower() == "item") or (obtain_elem["type"].lower() == "object"):

                        # first check if already in inventory
                        found_in_current_inv = False
                        
                        for inv_elem in  charac.get_inventory():
                        
                            if inv_elem.get_name().lower() == obtain_elem["name"].lower():
                                found_in_current_inv = True
                                break

                        if not found_in_current_inv:
                            # if not, add to inventory

                            # print("DEBUG 2: add object to character's inventory and World_State updated")

                            new_obj = Object.Object()
                            new_obj.set_general_type("Object")
                            new_obj.set_type(obtain_elem["type"])
                            new_obj.set_name(obtain_elem["name"])
                            new_obj.set_state(obtain_elem["state"])
                            new_obj.update_qty(obtain_elem["qty"])
                            obtain_obj_list.append(new_obj)

                        else:       # print fail_desc:
                            print()
                            print("DEBUG: found_in_current_inv = ", found_in_current_inv)
                            # print("DEBUG: (obtain_elem['type'] == 'Item') not found:")
                            print()

                            output = game_loop.dynamic_variable_processor(world_state, int_JSON_obj["fail_desc"])
                            print(output)

                            print()

                        # update the character's inventory based on the obtain list:
                        if (len(obtain_obj_list) > 0):
                            world_state.remove_character(charac)
                            charac.update_inventory("add", obtain_obj_list)
                            world_state.spawn_character(charac)

                    # ----------
                    # 5. (d) (ii)
                    #   if obtain is an tile:
                    elif obtain_elem["type"] == "tile":
                        prev_tile = world_state.get_saved_tile_by_name(obtain_elem["name"])
                        if prev_tile is not None:
                            world_state.update_saved_tiles("remove", prev_tile)
                            found_prev_tile = True
                            new_tile = prev_tile
                        else:


                            new_tile_id = text_file_processor.lookup_tileID_by_name_state(obtain_elem["name"], obtain_elem["state"])
                            new_tile = game_initialization.get_tile_by_name_and_state(obtain_elem["name"], obtain_elem["state"])
                            new_tile.set_tile_id(new_tile_id)
                            print("\tDEBUG: new_tile_id = ", new_tile_id)
                            print("\tDEBUG: new_tile.get_name().lower() = ", new_tile.get_name().lower())
                            print("\tDEBUG: new_tile.get_state() = ", new_tile.get_state())
                            print("\tDEBUG: new_tile.get_tile_id() = ", new_tile.get_tile_id())
                            print("\tDEBUG: new_tile.get_movable() = ", new_tile.get_movable())
                            
                            # print("\tDEBUG: new_tile (old coords) = ", new_tile.get_coords())

                            new_tile.update_coords( world_state.get_tile_by_name(obtain_elem["name"]).get_coords())
                            print("\tDEBUG: new_tile (new coords) = ", new_tile.get_coords())


    # *****************************************************************************

                        print("DEBUG: (charac.get_coords() = ", charac.get_coords())
                        
                        print("DEBUG: (obtain_elem['type'] == 'tile')")
                        print("DEBUG: OLD TILE (world_state.get_tile_by_name(obtain_elem['name']): ", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_name().lower(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_state(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_tile_id(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_coords()    )
                        
                        # update the tile in world_state:
                        world_state.update_saved_tiles("add", world_state.get_tile_by_name(obtain_elem["name"]))

                        world_state.update_tile(new_tile.get_coords(), new_tile)

                        print()
                        print("DEBUG: NEW TILE (world_state.get_tile_by_name(obtain_elem['name']): ", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_name().lower(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_state(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_tile_id(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_coords()    )

                    # ----------
                    # 5. (d) (iii)
                    #   if obtain is Gold:
                    elif obtain_elem["type"].lower() == "gold":
                        # increment gold amount:
                        active_char = world_state.get_active_char()
                        
                        obtain_amount = game_loop.dynamic_variable_processor(world_state, str(obtain_elem["qty"])) 
                        obtain_amount = int(obtain_amount)

                        world_state.remove_character(active_char)

                        # ----------
                        # 5. (d) (iii.1)
                        #   if gold is being stolen by theif, remove gold (negative increment)
                        if int_JSON_obj["name"].lower() == "steal":
                            # steal gold from player:
                            obtain_amount = (-1) * obtain_amount
                            active_char.increment_current_gold(obtain_amount)

                        # ----------
                        # 5. (d) (iii.2)
                        #   otherwise, add positive amount of gold
                        else:
                            active_char.increment_current_gold(obtain_amount)

                        world_state.spawn_character(active_char)







#-------------------------------------------------------------------------
# 6. print output, ie, success_desc or fail_desc
#       must call functions to insert variable data
#       and format the text properly       
#   (a) requirements are met
#   (b) requirements are not met
#-------------------------------------------------------------------------


            # ----------
            # 6. (a) 
            #   requirements are met
            print()
            output = game_loop.dynamic_variable_processor(world_state, int_JSON_obj["success_desc"])
            print(output)
            print()

        # ----------
        # 6. (b) 
        #   requirements are not met
        else:  
            print()
            output = game_loop.dynamic_variable_processor(world_state, int_JSON_obj["fail_desc"])
            print(output)
            print()

    else:
        # this code should never be reached:
        print("DEBUG: not found")

        

    return world_state


