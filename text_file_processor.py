import json
import csv

# use Interaction class to pass data back to state_updates.py
import Interaction 

CHARACTERS_JSON_FILE = "data_files/Characters_02b.json"
OBJECTS_JSON_FILE = "data_files/objects_02n.json"
TILES_JSON_FILE = "data_files/tiles_01.json"

OBJECTS_STATUS_JSON_FILE = "data_files/object_status.json"
CHARACTER_STATUS_JSON_FILE = "data_files/character_status.json"

TILE_ID_MAPPING_JSON_FILE = "data_files/tileIDMapping_01.json"

WORLD_MAP_STATUS_CSV_FILE = "data_files/world_map_status_00.csv"
# WORLD_MAP_STATUS_ROWS = 25
WORLD_MAP_STATUS_ROWS = 22
WORLD_MAP_STATUS_COLUMNS = 14

LOAD_WORLD_MAP_STATUS_CSV_FILE = "save_files/world_map_status_save.csv"
LOAD_OBJECTS_JSON_FILE = "save_files/objects_status_save.json"
LOAD_CHARACTER_STATUS_JSON_FILE = "save_files/char_status_save.json"
LOAD_WORLD_MAP_TURN_STATUS_JSON_FILE = "save_files/world_map_turn_status.json"


def load_tile_JSON_data_file():
    # returns a JSON array of tile data 
    # from the JSON tiles_01 file
    
    with open(TILES_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    return parsed_tile_data


    pass





def load_object_status_file(load_game):
    # returns a JSON array of object-status data 
    # from the JSON objects_status file
    
    if load_game =='Y':
        file_to_load = LOAD_OBJECTS_JSON_FILE
    else:
        file_to_load = OBJECTS_STATUS_JSON_FILE
    
    with open(file_to_load, 'r') as file:
        parsed_object_status_data = json.load(file)

    return parsed_object_status_data















def load_character_status_file(load_game):
    # returns a JSON array of character-status data 
    # from the JSON character_status file
    if load_game =='Y':
        file_to_load = LOAD_CHARACTER_STATUS_JSON_FILE
    else:
        file_to_load = CHARACTER_STATUS_JSON_FILE
    
    
    with open(file_to_load, 'r') as file:
        parsed_character_status_data = json.load(file)

    return parsed_character_status_data











def load_tileIDMapping_file():
    # returns a JSON array of tile-id-mappings data
    # from the JSON tileIDMapping file
    
    with open(TILE_ID_MAPPING_JSON_FILE, 'r') as file:
        tile_mapping_id_data = json.load(file)

    return tile_mapping_id_data








def lookup_tileID_by_name_state(tile_name,state):
    # given a tile name and state, find corresponding tile ID:

    found_tile = False

    with open(TILE_ID_MAPPING_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    for tile in parsed_tile_data:
        if (tile["name"] == tile_name) and (tile["state"] == state):
            found_tile = True
            return tile["tile_id"]

    if not found_tile:
        return "Not Found"
    













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
            return ""
            # return None

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
            return ""
            # return None
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

        if found_tile == False:
            return ""
            # return None








def lookup_interaction (type, name, state, interaction_key):
    # Given the name of a noun and its state, and its interaction word (verb) return it's interaction data
    # Return None if not match

    if type == "Object":
        with open(OBJECTS_JSON_FILE, 'r') as file:
            parsed_data = json.load(file)
    elif type == "Character":
        with open(CHARACTERS_JSON_FILE, 'r') as file:
            parsed_data = json.load(file)
    else:
        with open(TILES_JSON_FILE, 'r') as file:
            parsed_data = json.load(file)
            
    found_noun= False
    found_interac = False

    for obj in parsed_data:
       
        if (obj["name"] == name) and (obj["state"] == state):
            found_noun = True
            
            for interac in obj["interactions"]:
                # if the interaction name matches, print its details...:
                if interac["name"] == interaction_key:
                    found_interac = True
                    return interac
    return None



    
























# def lookup_interaction_ret_object(interaction_key):
#     # Given arguments return a populate Interaction object for command processing
#     # Return None if not match
    
#     # get data from JSON files:

#     with open(OBJECTS_JSON_FILE, 'r') as file:
#         parsed_object_data = json.load(file)

#     with open(CHARACTERS_JSON_FILE, 'r') as file:
#         parsed_character_data = json.load(file)

#     with open(TILES_JSON_FILE, 'r') as file:
#         parsed_tile_data = json.load(file)


#     # setup interaction array:
#     interaction_key = interaction_key.strip()

#     if interaction_key == "":
#         return None

#     interaction_array = interaction_key.split(maxsplit=1)

#     if len(interaction_array) < 2:
#         return None

#     # 1) search Objects JSON, if found return

#     found_object = False
#     found_interac = False

#     # iterate through each object from the JSON file:
#     for obj in parsed_object_data:

#         # if the interaction has been found, then exit the loop.
#         if found_interac:
#             break

#         # if the object name matches, print its details...:
#         if obj["name"] == interaction_array[1]:

#             found_object = True

#             # print("Name:", obj["name"])
#             # print("state:", obj["state"])
            
#             # iterate through each interaction for the found object:
#             for interac in obj["interactions"]:

#                 # if the interaction name matches, print its details...:
#                 if interac["name"] == interaction_array[0]:

#                     found_interac = True
#                     # print("\tinteraction - name: ", interac["name"])

#                     # create an Interaction object
#                     inter_obj = Interaction.Interaction()
#                     inter_obj.set_entity_general_type("Object")
#                     inter_obj.set_entity_name(obj["name"])
#                     inter_obj.set_entity_state(obj["state"])
#                     # inter_obj.set_entity_type(obj["type"])
#                     inter_obj.set_interaction_data(interac)
                    
#                     return inter_obj




#     # 2) search Characters JSON, if found return
#     if found_interac == False:


#         found_char_elem = False
#         found_interac = False

#         # iterate through each object from the JSON file:
#         for char_elem in parsed_character_data:

#             # if the interaction has been found, then exit the loop.
#             if found_interac:
#                 break

#             # if the object name matches, print its details...:
#             if char_elem["name"] == interaction_array[1]:

#                 found_char_elem = True

#                 # print("Name:", obj["name"])
#                 # print("state:", obj["state"])
                
#                 # iterate through each interaction for the found object:
#                 for interac in char_elem["interactions"]:

#                     # if the interaction name matches, print its details...:
#                     if interac["name"] == interaction_array[0]:

#                         found_interac = True
#                         # print("\tinteraction - name: ", interac["name"])


#                         # create an Interaction object
#                         inter_obj = Interaction.Interaction()
#                         inter_obj.set_entity_general_type("Character")
#                         inter_obj.set_entity_name(char_elem["name"])
#                         inter_obj.set_entity_state(char_elem["state"])
#                         # inter_obj.set_entity_type(char_elem["type"])
#                         inter_obj.set_interaction_data(interac)
                        
#                         return inter_obj

#                         # return interac





#     # 3) search Tiles, if found return
#     if found_interac == False:


#         found_tile = False
#         found_interac = False

#         # iterate through each object from the JSON file:
#         for tile in parsed_tile_data:

#             # if the interaction has been found, then exit the loop.
#             if found_interac:
#                 break

#             # if the object name matches, print its details...:
#             if tile["name"] == interaction_array[1]:

#                 found_tile = True

#                 # print("Name:", obj["name"])
#                 # print("state:", obj["state"])
                
#                 # iterate through each interaction for the found object:

#                 # print("DEBUG: tile['interactions']", tile["interactions"])

#                 if tile["interactions"] is not None:

#                     for interac in tile["interactions"]:

#                         # if the interaction name matches, print its details...:
#                         if interac["name"] == interaction_array[0]:

#                             found_interac = True
#                             # print("\tinteraction - name: ", interac["name"])

#                             # create an Interaction object
#                             inter_obj = Interaction.Interaction()
#                             inter_obj.set_entity_general_type("Tile")
#                             inter_obj.set_entity_name(tile["name"])
#                             inter_obj.set_entity_state(tile["state"])
#                             # inter_obj.set_entity_type(tile["type"])
#                             inter_obj.set_interaction_data(interac)
                            
#                             return inter_obj

#                             # return interac
#                 else:
#                     return None


#     # 4) else return None
#     return None























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

                # print("DEBUG: tile['interactions']", tile["interactions"])

                if tile["interactions"] is not None:

                    for interac in tile["interactions"]:

                        # if the interaction name matches, print its details...:
                        if interac["name"] == interaction_array[0]:

                            found_interac = True
                            # print("\tinteraction - name: ", interac["name"])
                            
                            return interac
                else:
                    return None


    # 4) else return None
    return None

















def lookup_movable (tile_name,state):
    # Given a tile name and state, return the matching movable flag.
    # Return None if not match

    found_tile = False

    with open(TILES_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    for tile in parsed_tile_data:
        if (tile["name"] == tile_name) and (tile["state"] == state):
            found_tile = True
            return tile["movable"]

    if found_tile == False:
        return None
    

def lookup_tile_type (tile_name,state):
    # Given a tile name and state, return the matching movable flag.
    # Return None if not match

    found_tile = False

    with open(TILES_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    for tile in parsed_tile_data:
        if (tile["name"] == tile_name) and (tile["state"] == state):
            found_tile = True
            return tile["type"]

    if found_tile == False:
        return None










def lookup_gold_amt (name, state):
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













def load_world_map_status_csv(load_game):
    # loads the world map status CSV file into a 2D array and returns the array

    # create 2D array to store world_map_status data:

    if load_game == 'Y':
        file_to_load = LOAD_WORLD_MAP_STATUS_CSV_FILE
    else:
        file_to_load = WORLD_MAP_STATUS_CSV_FILE
        
    rows = WORLD_MAP_STATUS_ROWS
    cols = WORLD_MAP_STATUS_COLUMNS
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        matrix.append(row)


    # read from world_map_status CSV file
    with open(file_to_load, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        row_num = 0
        column_num = 0

        # Iterate over each row in the CSV file
        for row in csv_reader:
            column_num = 0

            # iterate over each column in the row
            for elem in row:
                elem_str = str(elem)

                matrix[row_num][column_num] = elem_str

                column_num = column_num + 1

            row_num = row_num + 1

    return matrix


















if __name__ == "__main__":


# ------------------------ Test: load_tile_JSON_data_file() function

# load_tile_JSON_data_file
    tile_data = load_tile_JSON_data_file()

    print()
    print("tile_data[0]: ")
    print(tile_data[0])

    print()
    print()


# ------------------------ Test: load_tileIDMapping_file() function

    tileIDMapping_data = load_tileIDMapping_file()

    print("tileIDMapping_data[0]: ")
    print(tileIDMapping_data[0])

    print()
    print()




# ------------------------ Test: load_character_status_file() function

    character_status_data = load_character_status_file()

    print("character_status_data[0]: ")
    print(character_status_data[0])

    print()
    print()






# ------------------------ Test: load_object_status_file() function

    object_status_data = load_object_status_file()

    print("object_status_data[0]: ")
    print(object_status_data[0])

    print()
    print()



# ------------------------ Test: lookup_interaction_key_only (interaction_key) function


    interaction_key = "open chicken coop"

    interaction_array = lookup_interaction_key_only (interaction_key)

    print("interaction_key = ", interaction_key)
    print(interaction_array)

    print()

    if interaction_array is not None:
        print("name = ", interaction_array["name"])
    else:
        print("No interactions found")

    print()



    interaction_key = "take ladder"

    interaction_array = lookup_interaction_key_only (interaction_key)

    print("interaction_key = ", interaction_key)
    print(interaction_array)

    print()

    if interaction_array is not None:
        print("name = ", interaction_array["name"])
    else:
        print("No interactions found")

    print()

    interaction_key = "heal farmhand"

    interaction_array = lookup_interaction_key_only (interaction_key)

    print("interaction_key = ", interaction_key)
    print(interaction_array)

    print()

    if interaction_array is not None:
        print("name = ", interaction_array["name"])
    else:
        print("No interactions found")


    print()
    print()

# ------------------------ Test: lookup_movable (tile_name,state) function
# Tile: 

    name = "chicken coop"
    state = "blocked"
    movable = lookup_movable(name, state)

    print("name = ", name)
    print("state = ", state)
    print("movable = ", movable)
    print()


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




# ------------------------ Test: load_world_map_status_csv() function
# 
    world_map_status_array = load_world_map_status_csv()
    
    print()
    print("world_map_status_array[0][0] = ", world_map_status_array[0][0])
    print()

# ------------------------ Test: lookup_interaction() function
# 

    print(lookup_interaction("Tiles","kitchen","closed","open"))