import text_file_processor



def interaction_commands(world_state,charac,command):
    # lookup command (iteraction: ACTION ENTITY)



# heres some quick steps that i think needs to be done to process an interaction.
# when someone types for e.g. "open barn". We need to check:

# 0. setup interaction command list/array:
    # setup interaction array:
    interaction_key = command.strip()

    if interaction_key == "":
        return None

    interaction_array = interaction_key.split(maxsplit=1)

    if len(interaction_array) < 2:
        # invalid interaction, so do print message and return:
        print("Command not recognized")
        return world_state

# 1. does the noun "barn" exist in the coord that the char is in? 
#   if theres no barn in their coords, meaning tile, inventory of the tile, 
#   or inventory of the character, characters in that tile 
#   then reject the command

    interac_noun = interaction_array[1]
    current_x, current_y = charac.get_coords()

    # found = False
    found_interac_tile = False
    found_interac_tile_inventory = False
    found_interac_char = False
    found_interac_char_inv = False

    found_obj_inv_list = []

    interac_name = ""
    interac_general_type = ""

    # check current tile matches 'interac_noun':
    current_tl = world_state.get_tiles()[current_x][current_y]
    
    if current_tl.get_name() == interac_noun:
        # found tile named 'interac_noun'
        found_interac_tile = True
        interac_name = interac_noun
        interac_general_type = "Tile"
        interac_state = current_tl.get_state()

        # (interac_general_type, \
        #     current_tl.get_name(), current_tl.get_state(), interaction_array[0])


    # if not tile, check tile inventory for match:
    if not found_interac_tile:
        tl_inv_list = current_tl.get_inventory()     
        if len(tl_inv_list) > 0:
            for inv_elem in tl_inv_list:
                if inv_elem.get_name() == interac_noun:
                    found_interac_tile_inventory = True
                    interac_name = interac_noun
                    interac_general_type = "Object"
                    interac_state = inv_elem.get_state()
                    # track the tile object that matches
                    tile_current_obj_found = inv_elem
                    break

    # if not tile and not in tile inventory, check character/npc on tile
    if (not found_interac_tile) and (not found_interac_tile_inventory):
         #et_chars_at_tile()
        chars_list = world_state.get_chars_at_tile(charac.get_coords())
        if len(chars_list) > 0:
            for char_elem in chars_list:
                if char_elem.get_name() == interac_noun:
                    found_interac_char = True
                    interac_name = interac_noun
                    interac_general_type = "Character"
                    interac_state = char_elem.get_state()
                    # track the character that matches
                    tile_char_found = char_elem
                    break

    # if not tile, not in tile-inventory, not char/npc name, check char/npc inventory
    if (not found_interac_tile) and (not found_interac_tile_inventory) and (not found_interac_char):
        chars_list = world_state.get_chars_at_tile(charac.get_coords())
        if len(chars_list) > 0:
            for char_elem in chars_list:
                char_inv = char_elem.get_inventory()
                if len(char_inv) > 0:
                    for inv_elem in char_inv:
                        if inv_elem.get_name() == interac_noun:
                            found_interac_char_inv = True
                            interac_name = interac_noun
                            interac_general_type = "Object"
                            interac_state = inv_elem.get_state()
                            break
                if found_interac_char_inv:
                    break


    # the interaction noun was not found, so print a message and return
    if (not found_interac_tile) and (not found_interac_tile_inventory) and \
        (not found_interac_char) and (not found_interac_char_inv):
        print("Command not recognized")
        return world_state



# 2. if "barn" does exist in their coord, what is the state of the barn? and its general type?

    if ( found_interac_tile) or ( found_interac_tile_inventory) or \
        ( found_interac_char) or ( found_interac_char_inv):

        # charac.get_coords()
        # print("DEBUG: charac.get_coords() = ", charac.get_coords())

        # print("DEBUG: current_tl.get_name() = ", current_tl.get_name())
        # print("DEBUG: current_tl.get_state() = ", current_tl.get_state())
        # print("DEBUG: current_tl.get_coords() = ", current_tl.get_coords())
        # print("DEBUG: current_tl.get_general_type() = ", current_tl.get_general_type())


# 3. use def lookup_interaction (type, name, state, interaction_key) to grab the interaction data from JSON

        int_JSON_obj = text_file_processor.lookup_interaction(interac_general_type, \
            interac_name, interac_state, interaction_array[0])

        print("DEBUG: int_JSON_obj: ")
        print(int_JSON_obj)

# 4. process the interaction based on data from 3.
 
# {'name': 'open', 'success_desc': 'The door to the kichen is already open.', 
#       'fail_desc': 'The door to the kichen is already open.', 
#       'change_state_to': 'open', 
#       'requirement': 'null', 
#       'obtain': None}

        # a) check for requirements, if any:
        requirements_satisfied = False

        # if no requirements, assume successful:

        if int_JSON_obj["requirement"] is None:
            print("DEBUG: int_JSON_obj['requirement'] = ", int_JSON_obj["requirement"])

            requirements_satisfied = True

        else:
            print("DEBUG: int_JSON_obj['requirement'] (Not None)= ", int_JSON_obj["requirement"])

        # else, check all requirements in array:



        # b) if requirements_satisfied, check 'change_state_to' field,
        #   and update 'state' where needed 
        if requirements_satisfied:

            # print("requirements_satisfied = True")
            # print("change_state_to: ", int_JSON_obj["change_state_to"])

            # check which Tile/Char/Obj to change state to:
            # print("\tinterac_general_type: ", interac_general_type)
            # print("\tinterac_name: ", interac_name)
            # print("\tinterac_state: ", interac_state)
            
            # if current state == change_state_to, don't bother updating state info
            if int_JSON_obj["change_state_to"] != interac_state:

                # update the state (Tile/Char/Obj) in World_State:

                if interac_general_type == "Tile":
                    # update current tile's state in World_State

                    # current_x, current_y
                    # def update_tile(self, coords, new_tile):
                    current_tl.get_state(interac_state)
                    world_state.update_tile(current_tl.get_coords(), current_tl)

                    # debug only:
                    print("DEBUG: world_state.get_tiles()[current_x][current_y].get_state() = ", \
                        world_state.get_tiles()[current_x][current_y].get_state())
                    

                    pass 

                elif interac_general_type == "Character":
                    # find and update the character's state in World_State
                    #     interac_name
                    #     interac_state
                    char_on_tile = world_state.get_chars_at_tile(current_tl.get_coords())

                    if len(char_on_tile) > 0:
                        for char_elem in char_on_tile:
                            if char_elem.get_name() == interac_name:
                                world_state.remove_character(char_elem)
                                char_elem.set_state(interac_state)
                                world_state.spawn_character(char_elem)

                                # debug only:
                                print("DEBUG: ", char_elem.get_name(), ",", char_elem.get_state())
                                break
                    

                else:  # interac_general_type == "Object"
                    # find and update the Object's state
                    
                    #    first, if it was in tile's inventory, update there:
                    if found_interac_tile_inventory:
                        print("DEBUG: found in Tile inventory")

# ******
# ****** Delete object/item from current Tile's inventory and add to char's inventory:
# ******

                        if int_JSON_obj["change_state_to"] == "delete":
                            # delete the item from the current tile's inventory
                            # x_coord, y_coord = current_tl.get_coords()

                            tl_obj_inv_list = current_tl.get_inventory()

                            if len(tl_obj_inv_list) > 0:
                                for obj_elem in tl_obj_inv_list:
                                    if obj_elem.get_name() == interac_name:
                                        # remove that object from tile's inventory
                                        found_obj_inv_list.append(obj_elem)
                                        # obj_list = []

                                        # obj_list.append(obj_elem)
                                        current_tl.update_inventory("remove", found_obj_inv_list)

# ********
# NOTE: this might not be the right place for this - should be in 'obtains' code:
# ****
# add item/object to character's inventory list
# ********        
                                        current_char = world_state.get_active_char()
                                        world_state.remove_character(current_char)
                                        current_char.update_inventory("add", found_obj_inv_list)
                                        world_state.spawn_character(current_char)




                                        break

                             # then update the tile in World_State:
                            world_state.update_tile(current_tl.get_coords(), current_tl)


                            print()
                            print("DEBUG: removed object from Tile's inventory and World_State updated")
                            print("DEBUG: add object to character's inventory and World_State updated")
                            print()
                            print(int_JSON_obj["success_desc"])
                            print()



                            # world_state.get_tiles()[current_x][current_y]

                    # # debug only:
                    # print("DEBUG: world_state.get_tiles()[current_x][current_y].get_state() = ", \
                    #     world_state.get_tiles()[current_x][current_y].get_state())

  


                    elif found_interac_char_inv:  # it was in a character's inventory, update there:
                        print("DEBUG: found in character's inventory: found_interac_char_inv = True")

                        pass 



    # if ( found_interac_tile) or ( found_interac_tile_inventory) or \
    #     ( found_interac_char) or ( found_interac_char_inv):


                

                        pass 

            


        # c) if requirements_satisfied, check 'obtain' field,
        #   and update where needed 
            print("Obtains:")
            print("\t", int_JSON_obj["obtain"])

            if int_JSON_obj["obtain"] is not None:
                # iteratate through the obtains list:
                for obtain_elem in int_JSON_obj["obtain"]:

                    # check to see what type it is:
                    pass

    else:
        print("DEBUG: not found:")

        

    return world_state






























    # # old way: interac = text_file_processor.lookup_interaction_key_only(command)
    # # new way: using Interaction object:
    # interac_obj = text_file_processor.lookup_interaction_ret_object(command)

    # if interac_obj is None:
    #     print("I don't understand that command")
    # else:
        
    #     # for now, just debugging info

    #     print("DEBUG: (interaction_commands()): interac_obj.get_entity_name(): ", \
    #             interac_obj.get_entity_name() )
    #     print("DEBUG: (interaction_commands()): interac_obj.get_entity_general_type(): ", \
    #             interac_obj.get_entity_general_type())
    #     print("DEBUG: (interaction_commands()): interac_obj.get_entity_state(): ", \
    #             interac_obj.get_entity_state())
    #     print("DEBUG: (interaction_commands()) -------------")
    #     print("DEBUG: (interaction_commands()): interac_obj.get_interaction_data(): ", \
    #             interac_obj.get_interaction_data())
    #     print("DEBUG: (interaction_commands()): ")
        
    #     interac_JSON_data = interac_obj.get_interaction_data()

    #     print("\tchange_state_to: ", interac_JSON_data["change_state_to"])

    #     int_requirements = interac_JSON_data["requirement"]

    #     if len(int_requirements) > 0:
    #        for req_elem in int_requirements:
    #             print("\trequirement: ", \
    #                     req_elem["type"], ",", req_elem["name"], ",", \
    #                     req_elem["state"], ",", req_elem["qty"], ",", \
    #                     req_elem["remove_obj"] )
                


