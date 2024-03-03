import text_file_processor
import classes.Object as Object
import text_formatting
import classes.Character as Character

def interaction_commands (world_state,charac,command):
    # main function to process interactions, directs the overall flow and logic of entire module
    
    command_status, interaction_array = check_command(command)  # check command length is valid
    
    if command_status == False:    # command length is not valid
        return world_state

    interac_noun = interaction_array[1].lower()
    interac_verb = interaction_array[0].lower()
    current_x, current_y = charac.get_coords()
    
    # check noun exists on current location of charac, if it does return the entity associated with the string interac_noun
    check_noun_status,noun_entity = check_noun_exists(world_state,charac,current_x,current_y,interac_noun,interac_verb)
    
    if check_noun_status == False:   # noun does not exist on current location of charac
        if charac.get_type()=="Character" and charac.get_active_player()=='Y':
            print("Command not recognized")
        return world_state

    # as command is valid, check the interaction requirements to see if pass
    req_status,int_JSON_obj = check_requirements(world_state,charac,noun_entity,interac_verb)
    
    if req_status == False:  # failed interaction requirements
        return world_state
    
    # As we now passed the interaction requirements, process state_updates to world_state.
    # First, we go through the interaction requirements and make necessary updates:
    world_state = process_requirements(world_state,int_JSON_obj,charac,interac_verb)
    world_state = process_requirements_turn(world_state,int_JSON_obj,noun_entity)
    
    # Next, we check the interaction field "change_state_to" and make updates:
    world_state = process_change_state_to(world_state,charac,int_JSON_obj,noun_entity)
    
    # Next, we check in interaction obtain field, and make updates for additional side-effects:
    process_obtain(world_state,int_JSON_obj,charac)
    
    return world_state   # done processing command, all updates made to world_state
 

def check_command(command):
    # This command checks if given command string is correct length for further processing
    # Also returns back the command split by space if valid
    
    interaction_key = command.strip()

    # check for empty string in interaction key/command:
    if interaction_key == "":
        print("Command not recognized")
        return False,""

    interaction_array = interaction_key.split(maxsplit=1)

    if len(interaction_array) < 2:
        # invalid interaction, so print message and return:
        print("Command not recognized")
        return False,""
    
    return True,interaction_array


def check_noun_exists(world_state,charac,current_x,current_y,interac_noun,interac_verb):
    # This function checks if the provided interac_noun exists in the current location of the charac
    # if found, also returns the entity found associated with interac_noun
    
    # check tile at location
    current_tl = world_state.get_tiles()[current_x][current_y]
    
    if current_tl.get_name().lower() == interac_noun:
        return True, current_tl

    # ------
    # check tile's inventory only if tile is "open" i.e. not closed 
    if current_tl.get_movable() == 'Y':
        tl_inv_list = current_tl.get_inventory()     
        if len(tl_inv_list) > 0:
            for inv_elem in tl_inv_list:
                if inv_elem.get_name().lower() == interac_noun:
                    return True, inv_elem
    # ------
    # check characters on character's location only if tile is "open" i.e. not closed 
    if current_tl.get_movable() == 'Y':
        chars_list = world_state.get_chars_at_tile(charac.get_coords())
        if len(chars_list) > 0:
            for char_elem in chars_list:
                if char_elem.get_name().lower() == interac_noun:
                        # found matching character, so update interac_ data:
                    return True, char_elem        
    # ------
    # check character's own inventory
    charac_inv = charac.get_inventory()
    if len(charac_inv) > 0:
        for inventory_elem in charac_inv:
            if inventory_elem.get_name().lower() == interac_noun:
                if (interac_verb == "take") or (interac_verb == "buy") \
                or (interac_verb == "make"):
                    print(interac_noun, "is already in inventory.")
                    return False, None
                else:
                    return True,inventory_elem
      
    return False, None    # couldn't find the noun anywhere on the specified location


def check_obj_requirement(charac,req_elem):
    # This is a helper function for check_requirements to check if obj requirement is satisifed
    if len(charac.get_inventory()) > 0:
       for inv_elem in charac.get_inventory():
            if (inv_elem.get_name().lower() == req_elem["name"]) and \
                (inv_elem.get_state().lower()== req_elem["state"]) and \
                (inv_elem.get_quantity() >= req_elem["qty"]):
                return True
    return False
    
    
def check_tile_requirement(world_state,charac,req_elem):
    # This is a helper function for check_requirements to check if tile requirement is satisifed
    current_x, current_y = charac.get_coords()
    current_tl= world_state.get_tiles()[current_x][current_y]
    
    if len(req_elem["state"].split())>1:
        req_elem_state = req_elem["state"].split()[0]
    else:
        req_elem_state = req_elem["state"]
    
    if req_elem["name"].lower() == current_tl.get_name().lower() and req_elem_state.lower() == current_tl.get_state().lower():
        return True
    else:
        return False
    
    
def check_gold_requirement (world_state,charac,req_elem,interac_verb):
    # This is a helper function for check_requirements to check if gold requirement is satisifed
    if interac_verb == "steal":
        for char in world_state.get_characters():
            if char.get_type() == "player":
                entity = char
                break
    else:
        entity = charac
    
    if entity.get_current_gold() >= int(text_formatting.dynamic_variable_processor(world_state,str(req_elem["qty"]))):
        return True
    else:
        return False
    
    
def check_char_requirement (req_elem,npc_at_tile_list):
    # This is a helper function for check_requirements to check if character requirement is satisifed
    if len(npc_at_tile_list) > 0:
        for npc_elem in npc_at_tile_list:
            if npc_elem.get_name().lower() == req_elem["name"].lower() and npc_elem.get_state().lower() == req_elem["state"].lower():
                return True
    return False


def print_failed_requirement(world_state, int_JSON_obj,charac):
    # This is a helper function for check_requirements to print the associated interaction failed text to console
    if charac is not None and charac.get_general_type()=="Character" and charac.get_active_player()=='Y':
        print()
        output = text_formatting.dynamic_variable_processor(world_state, int_JSON_obj["fail_desc"])
        print(text_formatting.justify(output))
        print()


def print_success_requirement(world_state,int_JSON_obj,charac):
    # This is a helper function for check_requirements to print the associated interaction success text to console
    if charac is not None and charac.get_general_type()=="Character" and charac.get_active_player()=='Y':
        print()
        output = text_formatting.dynamic_variable_processor(world_state, int_JSON_obj["success_desc"])
        print(text_formatting.justify(output))
        print()
                     
                        
def check_requirements(world_state,charac,noun_entity,interac_verb):
    # given a noun_entity and the interac_verb (interaction verb) find it's interaction data from JSON
    # if found, check if the interaction requirements are met and returns the interaction data from JSON
    
    if noun_entity.get_type() == "player":
        interac_name = "%player_name%"
    else:
        interac_name = noun_entity.get_name()

    # lookup the interaction data from our JSON file
    int_JSON_obj = text_file_processor.lookup_interaction(noun_entity.get_general_type(), \
            interac_name, noun_entity.get_state(), interac_verb)
    
    if int_JSON_obj is None:    # not found, so no need to process further
        if charac is not None and charac.get_general_type()=="Character" and charac.get_active_player()=='Y':
            print("Command not recognized")
        return False, None
    
        
    if int_JSON_obj["requirement"] is None:
    # check if there are no requirements required and assume requirements are satisfied:  
        print_success_requirement(world_state,int_JSON_obj,charac)
        return True,int_JSON_obj

    else:
        # as there are requirements, we check if we pass all requirements. 
        # Perform check for each requirement based on their requirement type
        for req_elem in int_JSON_obj["requirement"]:
            
            if req_elem["type"].lower() == "object":
                if check_obj_requirement(charac,req_elem) == False:
                    print_failed_requirement(world_state,int_JSON_obj,charac)
                    return False,None
                
            elif req_elem["type"].lower() == "tile":
                if check_tile_requirement(world_state,charac,req_elem) == False:
                    print_failed_requirement(world_state,int_JSON_obj,charac)
                    return False,None
                    
            elif req_elem["type"] == "Gold":
                if check_gold_requirement(world_state,charac,req_elem,interac_verb)== False:
                    print_failed_requirement(world_state,int_JSON_obj,charac)
                    return False,None  
                    
            elif req_elem["type"] == "Character":
                if check_char_requirement(req_elem,world_state.get_npc_chars_at_tile(charac.get_coords())) == False:
                    print_failed_requirement(world_state,int_JSON_obj,charac)
                    return False,None
    
    # if got to here, means all requirements passed, so return true and print associatedsuccess text        
    print_success_requirement(world_state,int_JSON_obj,charac)
    return True,int_JSON_obj
                  
                    
def process_change_state_to(world_state,charac,int_JSON_obj,noun_entity): 
   # this function makes update to world_state by processing the "change_state_to" field within the interaction data
   # returns back the updated world state
   
    # first we check if there is a turn requirement, if so, we don't update the state immediately as we need to wait for
    # specified number of turns
    no_turn_required = True
    if int_JSON_obj["requirement"] is not None:
        for requirement in int_JSON_obj["requirement"]:
            
            if requirement["type"]=="turn":
                no_turn_required=False
                break
    
    # check if no turn delay is required, then we make updates directly to the state based on change_state_to field in JSON
    if no_turn_required ==True: 
        if int_JSON_obj["change_state_to"] != noun_entity.get_state():
            if noun_entity.get_general_type() == "Tile":
                # update here is specified if the noun_entity is tile:
                
                if "CHANGE_TILE_TO" in int_JSON_obj["change_state_to"]:
                    # check if change state to has CHANGE_TILE_TO within it and make updates based on the provided tile id
                    id = int_JSON_obj["change_state_to"].split()[1]
                    noun_entity.update_tile_by_id(id)
                    world_state = interaction_commands (world_state,noun_entity,"DEFAULT " + noun_entity.get_name())
                else:
                    # make update to tile based on provided new state stored in change_state_to JSON field
                    noun_entity.update_tile_by_state(int_JSON_obj["change_state_to"])
                    
                world_state = interaction_commands (world_state,noun_entity,"DEFAULT " + noun_entity.get_name())
                # in the above line, we make a call to submit command "DEFAULT tile_name" in case the updated tile 
                # has a default interaction
                    
            elif noun_entity.get_general_type() == "Character":
                # update here is specified if the noun_entity is a character:
                
                if int_JSON_obj["change_state_to"] == "delete":
                    world_state = world_state.remove_character(noun_entity)
                else:
                    noun_entity.set_state(int_JSON_obj["change_state_to"])
                    world_state = interaction_commands (world_state,noun_entity,"DEFAULT " + noun_entity.get_name())
                    # in the above line, we make a call to submit command "DEFAULT character_name" in case the updated character
                    # has a default interaction
            else: 
                # update here is specified if the noun_entity is an object (item):
                
                if int_JSON_obj["change_state_to"] == "delete":
                    x,y = charac.get_coords()
                    if noun_entity in world_state.get_tiles()[x][y].get_inventory():
                        world_state.get_tiles()[x][y].update_inventory("remove",[noun_entity])
                    else:
                        charac.update_inventory("remove", [noun_entity])
                else:
                    noun_entity.set_state(int_JSON_obj["change_state_to"])
     
    return world_state # all necessary updates done, return updated world state


def obtain_item(world_state,charac,obtain_elem):
    # this is a helper function for process_obtain function that creates object (item) as specified by the obtain field in JSON
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
            charac.update_inventory("add", [new_obj])
            return world_state
        else:       # print fail_desc:
            print()
            print("DEBUG: found_in_current_inv = ", found_in_current_inv)            
            print()
            print(obtain_elem["name"], "is already in inventory.")          
            return world_state


def obtain_tile(world_state, obtain_elem):
    # this is a helper function for process_obtain function that creates tile as specified by the obtain field in JSON
    for row in world_state.get_tiles():
        for tl in row:
            if tl.get_name() == obtain_elem["name"]:
                tl.update_tile_by_state(obtain_elem["state"])
    return world_state


def obtain_gold(world_state,charac,obtain_elem):
    # this is a helper function for process_obtain function that creates gold as specified by the obtain field in JSON
    obtain_amount = int(text_formatting.dynamic_variable_processor(world_state, str(obtain_elem["qty"])))
    charac.increment_current_gold(obtain_amount)
    return world_state
         
         
def obtain_char(world_state,charac,obtain_elem):
    # this is a helper function for process_obtain function that creates a new Character as specified by the obtain field in JSON
    
    new_charac=Character.Character()
    new_charac.set_name(obtain_elem["name"])
    new_charac.set_state(obtain_elem["state"])
    new_charac.set_type(text_file_processor.lookup_type("Character",obtain_elem["name"],obtain_elem["state"]))
    new_charac.update_coords(charac.get_coords())
    new_charac.set_current_hp(text_file_processor.lookup_current_hp(obtain_elem["name"],obtain_elem["state"]))
    new_charac.set_max_hp(text_file_processor.lookup_max_hp(obtain_elem["name"],obtain_elem["state"]))
    world_state.spawn_character(new_charac)
    
    return world_state
    
    
def process_obtain(world_state,int_JSON_obj,charac):
    # this function processes the obtain field within the JSON interaction data which contains side effects
    
    if int_JSON_obj["obtain"] is not None:
        for obtain_elem in int_JSON_obj["obtain"]:
            # check type of things that needs to be obtained and call relevant obtain function to handle it
            
            if (obtain_elem["type"].lower() == "item") or (obtain_elem["type"].lower() == "object"):
                world_state = obtain_item(world_state,charac,obtain_elem)
                
            elif obtain_elem["type"] == "tile":
                world_state = obtain_tile(world_state,obtain_elem)
                # here we make an extra method call to submit command "DEFAULT tile_name" to check if there
                # is any default action needed for the new tile we obtained:
                world_state = interaction_commands (world_state,charac,"DEFAULT " + obtain_elem["name"])
                
            elif obtain_elem["type"].lower() == "gold":
                world_state = obtain_gold(world_state,charac,obtain_elem)
                
            elif obtain_elem["type"].lower() == "character":
                world_state = obtain_char(world_state,charac,obtain_elem)
                # here we make an extra method call to submit command "DEFAULT character_name" to check if there
                # is any default action needed for the new character we obtained:
                world_state = interaction_commands (world_state,world_state.get_characters()[-1],"DEFAULT " + obtain_elem["name"])
                
                
def process_requirements_turn(world_state,int_JSON_obj,noun_entity):
    # this function processes any requirement that specify type=="turn" which means we have to set-up wait for X turn mechanic
    
    if int_JSON_obj["requirement"] is not None:
        for requirement in int_JSON_obj["requirement"]:
            if requirement["type"]=="turn":
                noun_entity.update_turn_counter(requirement["qty"],int_JSON_obj["change_state_to"])
    return world_state
                 

def process_requirements(world_state,int_JSON_obj,charac,interac_verb):
    # this function processes any requirements that specifies that the requirement entity needs to be removed
    # or any requirement entity that needs their state to be updated
    
    x,y = charac.get_coords()
    
    if int_JSON_obj["requirement"] is not None:
        for requirement in int_JSON_obj["requirement"]:
            if requirement["remove_obj"] == "Y":
                # check if entity to remove is an object (item) and make updates to remove the object
                if requirement["type"].lower() == "object" or requirement["type"].lower() == "item":
                    found_obj=False
                    
                    # first we check if the object to remove is in the current location's tile inventory
                    for item in world_state.get_tiles()[x][y].get_inventory():
                        if item.get_name().lower() == requirement["name"].lower() and item.get_state().lower() == requirement["state"].lower():
                            world_state.get_tiles()[x][y].update_inventory("remove",[item])
                            found_obj = True
                            break
                        
                    # next, if we couldnt find it then we check if the object to remove is in the character's inventory
                    if found_obj == False:
                        for item in charac.get_inventory():
                            if item.get_name().lower() == requirement["name"].lower() and item.get_state().lower() == requirement["state"].lower():
                                charac.update_inventory("remove",[item])
                                break
                
                # check if entity to remove is gold instead of an object       
                elif requirement["type"].lower() == "gold":
                    if interac_verb == "steal":
                        # check for special case for steal command, the entity to remove gold is the player character instead of
                        # entity submitting the steal command
                        for char in world_state.get_characters():
                            if char.get_type() == "player":
                                entity = char
                                break
                    else:
                        entity = charac
                    
                    entity.increment_current_gold(int(text_formatting.dynamic_variable_processor(world_state,str(requirement["qty"])))*-1)

            # checks if any requirement entity needs to have their state updated due to state data: "old_state CHANGE_STATE_TO new_state"
            elif len(requirement["state"].split()) >1:
                if requirement["type"].lower()=="tile":
                    new_state = requirement["state"].split()[2]
                    x,y = charac.get_coords()
                    current_tl = world_state.get_tiles()[x][y]
                    current_tl.update_tile_by_state(new_state)
                               
    return world_state