import text_file_processor
import Object
import load_Tiles_temp


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
        # found tile named 'interac_noun', so update interac_ data:
        found_interac_tile = True
        interac_name = interac_noun
        interac_general_type = "Tile"
        interac_state = current_tl.get_state()


    # if not tile, check tile inventory for match:
    if not found_interac_tile:
        tl_inv_list = current_tl.get_inventory()     
        if len(tl_inv_list) > 0:
            for inv_elem in tl_inv_list:
                if inv_elem.get_name() == interac_noun:
                    # found in tile inventory, so update interac_ data:
                    found_interac_tile_inventory = True
                    interac_name = interac_noun
                    interac_general_type = "Object"
                    interac_state = inv_elem.get_state()
                    # track the tile object that matches
                    tile_current_obj_found = inv_elem
                    break


    # if not tile and not in tile inventory, check character/npc on tile
    if (not found_interac_tile) and (not found_interac_tile_inventory):
        chars_list = world_state.get_chars_at_tile(charac.get_coords())
        if len(chars_list) > 0:
            for char_elem in chars_list:
                if char_elem.get_name() == interac_noun:
                    # found matching character, so update interac_ data:
                    found_interac_char = True
                    interac_name = interac_noun
                    interac_general_type = "Character"
                    interac_state = char_elem.get_state()
                    # track the character that matches
                    tile_char_found = char_elem
                    break


    # if not tile, not in tile-inventory, not char/npc name, check charac inventory
    if (not found_interac_tile) and (not found_interac_tile_inventory) and (not found_interac_char):

        charac_inv = charac.get_inventory()
        if len(charac_inv) > 0:
            for inventory_elem in charac_inv:
                if inventory_elem.get_name() == interac_noun:
                    found_interac_char_inv = True
                    interac_name = interac_noun
                    interac_general_type = "Object"
                    interac_state = inventory_elem.get_state()
                    break


#----------------------------------------
        # chars_list = world_state.get_chars_at_tile(charac.get_coords())
        # if len(chars_list) > 0:
        #     for char_elem in chars_list:
        #         char_inv = char_elem.get_inventory()
        #         if len(char_inv) > 0:
        #             for inv_elem in char_inv:
        #                 if inv_elem.get_name() == interac_noun:
        #                     # found in character inventory, so update interac_ data:
        #                     found_interac_char_inv = True
        #                     interac_name = interac_noun
        #                     interac_general_type = "Object"
        #                     interac_state = inv_elem.get_state()
        #                     break
        #         if found_interac_char_inv:
        #             break
#----------------------------------------


    # the interaction noun was not found, so print a message and return
    if (not found_interac_tile) and (not found_interac_tile_inventory) and \
        (not found_interac_char) and (not found_interac_char_inv):
        print("Command not recognized")
        return world_state



# 2. if "barn" (interac_noun) does exist in their coord, what is the state of the barn? and its general type?
#       we updated state and general type in code above ^

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
 
        # a) check for requirements, if any:
        requirements_satisfied = False

        # if no requirements, assume successful:

        if int_JSON_obj["requirement"] is None:
            # print("DEBUG: int_JSON_obj['requirement'] = None"), int_JSON_obj["requirement"])
            print("DEBUG: int_JSON_obj['requirement'] = None")

            requirements_satisfied = True

        else:
            print("DEBUG: int_JSON_obj['requirement'] (Not None) = ", int_JSON_obj["requirement"])

        # else, check all requirements in array:
            found_obj_req = False
            for req_elem in int_JSON_obj["requirement"]:
                # i) check 'object' requirements, must be in current char's inventory:
                if req_elem["type"] == "object":
                    # act_char = world_state.get_active_char()
                    # fix below, remove act_char, replace with charac
                    act_char = charac
                    act_char_inv = act_char.get_inventory()
                    
                    if len(act_char_inv) > 0:
                        for inv_elem in act_char_inv:
                            if (inv_elem.get_name() == req_elem["name"]) and \
                                (inv_elem.get_quantity() >= req_elem["qty"]):
                                found_obj_req = True 
                                break
                    if not found_obj_req:
                        print()
                        print(int_JSON_obj["fail_desc"])
                        print()
                        requirements_satisfied = False
                        break



                    pass
            
            # if more than one requirement, need to use 'and' 
            if found_obj_req:
                print("\tDEBUG: requirements satisfied")
                requirements_satisfied = True





        # b) if requirements_satisfied, check 'change_state_to' field,
        #   and update 'state' where needed 
        if requirements_satisfied:
            
            # if current state == change_state_to, don't bother updating state info
            if int_JSON_obj["change_state_to"] != interac_state:

                # update the state (Tile/Char/Obj) in World_State:

                if interac_general_type == "Tile":

                    # save tile to restore later:
                    prev_tile = world_state.get_saved_tile_by_name(current_tl.get_name())
                    if prev_tile is not None:
                        world_state.update_saved_tiles("remove", prev_tile)
                        found_prev_tile = True
                        new_tile = prev_tile
                    else:

                    # update current tile's state in World_State

                        new_tile_name = current_tl.get_name()
                        new_tile_state = int_JSON_obj["change_state_to"]

                        new_tile_id = text_file_processor.lookup_tileID_by_name_state(new_tile_name, new_tile_state)
                        new_tile = load_Tiles_temp.get_tile_by_name_and_state(new_tile_name,new_tile_state)
                        new_tile.set_tile_id(new_tile_id)

                        new_tile.update_coords( world_state.get_tile_by_name(new_tile_name).get_coords())


# *************************************************
# fix: cannot add tile inventory to new tile, store old tile instead,
#       and restore it on open
# *************************************************


                    # update the tile in world_state:
                    world_state.update_saved_tiles("add", world_state.get_tile_by_name(current_tl.get_name()))
                    
                    world_state.update_tile(new_tile.get_coords(), new_tile)
                    
                    print("DEBUG: change_state_to: ", int_JSON_obj["change_state_to"])
                    print("\tDEBUG: need to replace appropriate tile info in World_State based on 'change_state_to' info")
                    
                    print("DEBUG: current_tl.get_name()", current_tl.get_name())
                    print("DEBUG: current_tl.get_state()", current_tl.get_state())
                    print("DEBUG: current_tl.get_tile_id()", current_tl.get_tile_id())
                    print("DEBUG: interac_state", interac_state)
                    print()
                    print("DEBUG: new_tile.get_name()", new_tile.get_name())
                    print("DEBUG: new_tile.get_state()", new_tile.get_state())
                    print("DEBUG: new_tile.get_tile_id()", new_tile.get_tile_id())
                    print()

#************************************************************************************                       

                    world_state.update_tile(new_tile.get_coords(), new_tile)

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
#           * code moved to obtains section *
# ****
# add item/object to character's inventory list
# ********        

                                        break

                             # then update the tile in World_State:
                            world_state.update_tile(current_tl.get_coords(), current_tl)


                            print()
                            print("DEBUG: removed object from Tile's inventory and World_State updated")
                            print("DEBUG: add object to character's inventory and World_State updated")
                            # print()
                            # print(int_JSON_obj["success_desc"])
                            # print()



                            # world_state.get_tiles()[current_x][current_y]

                    # # debug only:
                    # print("DEBUG: world_state.get_tiles()[current_x][current_y].get_state() = ", \
                    #     world_state.get_tiles()[current_x][current_y].get_state())

  


                    elif found_interac_char_inv:  # it was in a character's inventory, update there:
                        print("DEBUG: found in character's inventory: found_interac_char_inv = True")

                        pass 



        # c) if requirements_satisfied, check 'obtain' field,
        #   and update where needed 
            print("Obtains:")
            print("\t", int_JSON_obj["obtain"])

            if int_JSON_obj["obtain"] is not None:

# DEBUG: 
                # if found_obj_inv_list is not None:
                #     print("\tDEBUG: found_obj_inv_list[0].get_name() = ", found_obj_inv_list[0].get_name())
                #     print("\tDEBUG: found_obj_inv_list[0].get_state() = ", found_obj_inv_list[0].get_state())
                #     print("\tDEBUG: found_obj_inv_list[0].get_quantity() = ", found_obj_inv_list[0].get_quantity())

                obtain_obj_list = []
                
    # iteratate through the obtains list, add items to a list of objects:
                for obtain_elem in int_JSON_obj["obtain"]:

        # if obtain is an item:
                    if (obtain_elem["type"] == "Item") or (obtain_elem["type"] == "object"):

                        # first check if already in inventory
                        # 
                        found_in_current_inv = False
                        
                        for inv_elem in  charac.get_inventory():
                        
                            if inv_elem.get_name() == obtain_elem["name"]:
                                found_in_current_inv = True
                                break

                        if not found_in_current_inv:
                            # if not, add to inventory
                            new_obj = Object.Object()
                            new_obj.set_general_type("Object")
                            new_obj.set_type(obtain_elem["type"])
                            new_obj.set_name(obtain_elem["name"])
                            new_obj.set_state(obtain_elem["state"])
                            new_obj.update_qty(obtain_elem["qty"])
                            obtain_obj_list.append(new_obj)

                            # print()
                            # print(int_JSON_obj["success_desc"])
                            # print()
                        else:       # print fail_desc:
                            print()
                            print("DEBUG: (obtain_elem['type'] == 'Item') not found:")
                            print()
                            print(int_JSON_obj["fail_desc"])
                            print()

                        # update the character's inventory based on the obtain list:
                        if (len(obtain_obj_list) > 0):
                            world_state.remove_character(charac)
                            charac.update_inventory("add", obtain_obj_list)
                            world_state.spawn_character(charac)

        # if obtain is an tile:
                    elif obtain_elem["type"] == "tile":
                        prev_tile = world_state.get_saved_tile_by_name(obtain_elem["name"])
                        if prev_tile is not None:
                            world_state.update_saved_tiles("remove", prev_tile)
                            found_prev_tile = True
                            new_tile = prev_tile
                        else:



                            new_tile_id = text_file_processor.lookup_tileID_by_name_state(obtain_elem["name"], obtain_elem["state"])
                            new_tile = load_Tiles_temp.get_tile_by_name_and_state(obtain_elem["name"], obtain_elem["state"])
                            new_tile.set_tile_id(new_tile_id)
                            print("\tDEBUG: new_tile_id = ", new_tile_id)
                            print("\tDEBUG: new_tile.get_name() = ", new_tile.get_name())
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
                            world_state.get_tile_by_name(obtain_elem["name"]).get_name(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_state(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_tile_id(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_coords()    )
                        
                        # update the tile in world_state:
                        world_state.update_saved_tiles("add", world_state.get_tile_by_name(obtain_elem["name"]))

                        world_state.update_tile(new_tile.get_coords(), new_tile)

                        print()
                        print("DEBUG: NEW TILE (world_state.get_tile_by_name(obtain_elem['name']): ", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_name(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_state(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_tile_id(), ",", \
                            world_state.get_tile_by_name(obtain_elem["name"]).get_coords()    )
                        


#   self.name = ""
#     self._general_type = ""
#     self.__type = ""
#     self.__state = ""
#     self.co_ord_x = 0
#     self.co_ord_y = 0
  
# [{'type': 'Item', 'name': 'medkit', 'state': 'null', 'qty': 1}]




                    # check to see what type it is:
                    # pass


            print()
            print(int_JSON_obj["success_desc"])
            print()
        else:  # requirements not met:
            print()
            print(int_JSON_obj["fail_desc"])
            print()

    else:
        print("DEBUG: not found:")

        

    return world_state


