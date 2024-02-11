import json

CHARACTERS_JSON_FILE = "Characters_02b.json"
OBJECTS_JSON_FILE = "objects_02m.json"
TILES_JSON_FILE = "tiles_template.json"

OBJECTS_STATUS_JSON_FILE = "object_status_template.json"
CHARACTER_STATUS_JSON_FILE = "character_status_template.json"

TILE_ID_MAPPING_JSON_FILE = "tileIDMapping.json"


def load_object_status_file():
    # returns a JSON array of object-status data 
    # from the JSON objects_status file
    
    with open(OBJECTS_STATUS_JSON_FILE, 'r') as file:
        parsed_object_status_data = json.load(file)

    return parsed_object_status_data


def load_character_status_file():
    # returns a JSON array of character-status data 
    # from the JSON character_status file
    
    with open(CHARACTER_STATUS_JSON_FILE, 'r') as file:
        parsed_character_status_data = json.load(file)

    return parsed_character_status_data
    

def load_tileIDMapping_file():
    # returns a JSON array of tile-id-mappings data
    # from the JSON tileIDMapping file
    
    with open(TILE_ID_MAPPING_JSON_FILE, 'r') as file:
        tile_mapping_id_data = json.load(file)

    return tile_mapping_id_data




def lookup_desc (long_short , type, name, state):
    # Given arguments find, return the matching description from in-game text files
    # Returns None if not match
    # long_short determines whether to return long_desc vs short_desc
    # type determines if lookup is tile , character, object
    

# cheap and dirty solution to get started, 
# but will have to wrap in a class eventually
# because we don't want to be open and loading from the JSON file
# on every function call - too slow


    # Object:
    if type == "Object":

        found_object = False

        with open(OBJECTS_JSON_FILE, 'r') as file:
            parsed_object_data = json.load(file)

        for obj in parsed_object_data:
       
            if (obj["name"] == name) and (obj["state"] == state):

                found_object = True
                if long_short == "long":
                    return obj["description"]["long_desc"]
                else:
                    return obj["description"]["short_desc"]

        if found_object == False:
            return None

    elif type == "Character":
        
        found_character = False

        with open(CHARACTERS_JSON_FILE, 'r') as file:
            parsed_character_data = json.load(file)

        for char_elem in parsed_character_data:

            if (char_elem["name"] == name) and (char_elem["state"] == state):
                found_character = True
                if long_short == "long":
                    return char_elem["description"]["long_desc"]
                else:
                    return char_elem["description"]["short_desc"]

        if found_character == False:
            return None
    else:

        found_tile = False

        with open(TILES_JSON_FILE, 'r') as file:
            parsed_tile_data = json.load(file)

        for tile in parsed_tile_data:
            if (tile["name"] == name) and (tile["state"] == state):
                found_tile = True
                if long_short == "long":
                    return tile["description"]["long_desc"]
                else:
                    return tile["description"]["short_desc"]

            if found_tile == false:
                return None




def lookup_interaction (type, name, state, interaction_key): 
    pass  # Placeholder indicating that the function's logic will be implemented later


def lookup_interaction_key_only (interaction_key):
    # Given arguments return the matching interaction object as an array for command processing
    # Return None if not match
    
    # get data from JSON files:

    with open(OBJECTS_JSON_FILE, 'r') as file:
        parsed_object_data = json.load(file)

    with open(CHARACTERS_JSON_FILE, 'r') as file:
        parsed_character_data = json.load(file)

    with open(TILES_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)


    # setup interaction array:
    interaction_key = interaction_key.strip()
    interaction_array = interaction_key.split(maxsplit=1)

    # 1) search Objects JSON, if found return

    found_object = False
    found_interac = False

    # iterate through each object from the JSON file:
    for obj in parsed_object_data:

        # if the interaction has been found, then exit the loop.
        if found_interac:
            break

        # if the object name matches, print its details...:
        if obj["name"] == interaction_array[1]:

            found_object = True

            # print("Name:", obj["name"])
            # print("state:", obj["state"])
            
            # iterate through each interaction for the found object:
            for interac in obj["interactions"]:

                # if the interaction name matches, print its details...:
                if interac["name"] == interaction_array[0]:

                    found_interac = True
                    # print("\tinteraction - name: ", interac["name"])
                    
                    return interac




    # 2) search Characters JSON, if found return
    if found_interac == False:


        found_char_elem = False
        found_interac = False

        # iterate through each object from the JSON file:
        for char_elem in parsed_character_data:

            # if the interaction has been found, then exit the loop.
            if found_interac:
                break

            # if the object name matches, print its details...:
            if char_elem["name"] == interaction_array[1]:

                found_char_elem = True

                # print("Name:", obj["name"])
                # print("state:", obj["state"])
                
                # iterate through each interaction for the found object:
                for interac in char_elem["interactions"]:

                    # if the interaction name matches, print its details...:
                    if interac["name"] == interaction_array[0]:

                        found_interac = True
                        # print("\tinteraction - name: ", interac["name"])
                        
                        return interac





    # 3) search Tiles, if found return
    if found_interac == False:


        found_tile = False
        found_interac = False

        # iterate through each object from the JSON file:
        for tile in parsed_tile_data:

            # if the interaction has been found, then exit the loop.
            if found_interac:
                break

            # if the object name matches, print its details...:
            if tile["name"] == interaction_array[1]:

                found_tile = True

                # print("Name:", obj["name"])
                # print("state:", obj["state"])
                
                # iterate through each interaction for the found object:
                for interac in tile["interactions"]:

                    # if the interaction name matches, print its details...:
                    if interac["name"] == interaction_array[0]:

                        found_interac = True
                        # print("\tinteraction - name: ", interac["name"])
                        
                        return interac


    # 4) else return None
    return None




def lookup_movable (tile_name,state):
    # Given a tile name and state, return the matching movable flag.
    # Return None if not match

    found_tile = False

    with open(TILES_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    for tile in parsed_tile_data:
        if (tile["name"] == name) and (tile["state"] == state):
            found_tile = True
            return tile["movable"]

        if found_tile == false:
            return None






def lookup_gold_amt (obj_name, state):
    # Given an object name and state, return the matching gold_amt.
    # Return None if not match


    with open(OBJECTS_JSON_FILE, 'r') as file:
        parsed_object_data = json.load(file)


        found_object = False

        for obj in parsed_object_data:

            if (obj["name"] == name) and (obj["state"] == state):

                # print("DEBUG: found_object: ", found_object)

                found_object = True                
                return obj["gold_amt"]
                
        if found_object == False:
            return None


















if __name__ == "__main__":


# ------------------------ Test: load_tileIDMapping_file() function

    tileIDMapping_data = load_tileIDMapping_file()

    print("tileIDMapping_data[0]: ")
    print(tileIDMapping_data[0])

    print()
    print()




# ------------------------ Test: load_character_status_file() function

    character_status_data = load_character_status_file()

    print("character_status_data: ")
    print(character_status_data)

    print()
    print()






# ------------------------ Test: load_object_status_file() function

    object_status_data = load_object_status_file()

    print("object_status_data: ")
    print(object_status_data)

    print()
    print()



# ------------------------ Test: lookup_interaction_key_only (interaction_key) function


    interaction_key = "open chicken coop"

    interaction_array = lookup_interaction_key_only (interaction_key)

    print("interaction_key = ", interaction_key)
    print(interaction_array)

    print()
    print()

    print("name = ", interaction_array["name"])

    print()
    print()



    interaction_key = "take ladder"

    interaction_array = lookup_interaction_key_only (interaction_key)

    print("interaction_key = ", interaction_key)
    print(interaction_array)

    print()
    print()

    print("name = ", interaction_array["name"])

    print()
    print()

    interaction_key = "heal farmhand"

    interaction_array = lookup_interaction_key_only (interaction_key)

    print("interaction_key = ", interaction_key)
    print(interaction_array)

    print()
    print()

    print("name = ", interaction_array["name"])

    print()
    print()

# ------------------------ Test: lookup_movable (tile_name,state) function
# Tile: 

    name = "Claires house"
    state = "null"
    movable = lookup_movable(name, state)

    print("name = ", name)
    print("state = ", state)
    print("movable = ", movable)
    print()



# ------------------------ Test: lookup_gold_amt (obj_name, state) function
# Object: 

    name = "honey"
    state = "null"
    gold_amt = lookup_gold_amt(name, state)
    print("name = ", name)
    print("state = ", state)
    print("gold_amt = ", gold_amt)
    print()




# ------------------------ Test: lookup_desc (long_short , type, name, state) function
# Object:        
    long_short = "long"
    my_type = "Object"
    # name = "watering can"
    name = "honey"
    state = "null"
    description = lookup_desc (long_short , my_type, name, state)

    print("name = ", name)
    print("state = ", state)
    print("description = ", description)

    print()


# Character:        
    long_short = "long"
    my_type = "Character"
    name = "farmhand"
    state = "injured"
    description = lookup_desc (long_short , my_type, name, state)

    print("name = ", name)
    print("state = ", state)
    print("description = ", description)
    print()


# Tile:        
    long_short = "long"
    my_type = "Tile"
    name = "Claires house"
    state = "null"
    description = lookup_desc (long_short , my_type, name, state)

    print("name = ", name)
    print("state = ", state)
    print("description = ", description)

