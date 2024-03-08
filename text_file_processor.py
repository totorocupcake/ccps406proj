import json
import csv
import text_formatting
import classes.Data as Data

# need to get player variable from World_State

CHARACTERS_JSON_FILE = "data_files/Characters_02b.json"
OBJECTS_JSON_FILE = "data_files/objects_02n.json"
TILES_JSON_FILE = "data_files/tiles_01.json"

OBJECTS_STATUS_JSON_FILE = "data_files/object_status.json"
CHARACTER_STATUS_JSON_FILE = "data_files/character_status.json"
CHARACTER_TEMPLATE_JSON_FILE = "data_files/character_template.json"

TILE_ID_MAPPING_JSON_FILE = "data_files/tileIDMapping_01.json"

WORLD_MAP_TURN_STATUS_JSON_FILE = "data_files/world_map_turn_status.json"
WORLD_MAP_STATUS_CSV_FILE = "data_files/world_map_status_00.csv"
# WORLD_MAP_STATUS_ROWS = 25
WORLD_MAP_STATUS_ROWS = 22
WORLD_MAP_STATUS_COLUMNS = 14

LOAD_WORLD_MAP_STATUS_CSV_FILE = "save_files/world_map_status_save.csv"
LOAD_OBJECTS_JSON_FILE = "save_files/objects_status_save.json"
LOAD_CHARACTER_STATUS_JSON_FILE = "save_files/char_status_save.json"
LOAD_WORLD_MAP_TURN_STATUS_JSON_FILE = "save_files/world_map_turn_status.json"


# Functions to load static data files #####################################################################

def load_tile_JSON_data_file():
    # returns a JSON array of tile data 
    # from the JSON tiles_01 file
    
    with open(TILES_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    return parsed_tile_data

def load_objects_JSON_data_file():
    # returns a JSON array of tile data 
    # from the JSON tiles_01 file
    
    with open(OBJECTS_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    return parsed_tile_data

def load_characters_JSON_data_file():
    # returns a JSON array of tile data 
    # from the JSON tiles_01 file
    
    with open(CHARACTERS_JSON_FILE, 'r') as file:
        parsed_tile_data = json.load(file)

    return parsed_tile_data

def load_tileIDMapping_file():
    # returns a JSON array of tile-id-mappings data
    # from the JSON tileIDMapping file
    
    with open(TILE_ID_MAPPING_JSON_FILE, 'r') as file:
        tile_mapping_id_data = json.load(file)

    return tile_mapping_id_data

def load_char_template_file():
    # returns a JSON array of template characters data 
    # from the JSON character_template file
       
    file_to_load = CHARACTER_TEMPLATE_JSON_FILE
    
    with open(file_to_load, 'r') as file:
        parsed_object_status_data = json.load(file)

    return parsed_object_status_data

# Functions to load status files ################################################################

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
def load_world_map_turn_status(load_game):
    if load_game == 'Y':
        file_to_load = LOAD_WORLD_MAP_TURN_STATUS_JSON_FILE
    else:
        file_to_load = WORLD_MAP_TURN_STATUS_JSON_FILE

    with open(file_to_load, 'r') as file:
        parsed_world_map_turn_status_data = json.load(file)

    return parsed_world_map_turn_status_data

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

# Functions for looking up data from loaded data files ###############################################

# def lookup_tileID_by_name_state(tile_name,state):
#     # given a tile name and state, find corresponding tile ID:

#     found_tile = False

#     with open(TILE_ID_MAPPING_JSON_FILE, 'r') as file:
#         parsed_tile_data = json.load(file)

#     for tile in parsed_tile_data:
#         if (tile["name"].lower() == tile_name.lower()) and (tile["state"].lower() == state.lower()):
#             found_tile = True
#             return tile["tile_id"]

#     if not found_tile:
#         return "Not Found"

# def lookup_desc (long_short , type, name, state,world_state):
#     # Given arguments find, return the matching description from in-game text files
#     # Returns None if not match
#     # long_short determines whether to return long_desc vs short_desc
#     # type determines if lookup is tile , character, object
    
#     # cheap and dirty solution to get started, 
#     # but will have to wrap in a class eventually
#     # because we don't want to be open and loading from the JSON file
#     # on every function call - too slow

#     if type == "Object":
#         with open(OBJECTS_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
#     elif type == "Character":
#         with open(CHARACTERS_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
#     else:
#         with open(TILES_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
    
#     found_noun = False
        
#     for element in parsed_data:
#         name_formatted = text_formatting.dynamic_variable_processor(world_state,element["name"])
#         if (name_formatted.lower() == name.lower()) and (element["state"].lower() == state.lower()):
#             found_noun = True
#             if long_short == "long":
#                 return element["description"]["long_desc"]
#             else:
#                 return element["description"]["short_desc"]

#     if found_noun == False:
#         return ""
#         # return None

# def lookup_interaction (type, name, state, interaction_key):
#     # Given the name of a noun and its state, and its interaction word (verb) return it's interaction data
#     # Return None if not match

#     if type == "Object":
#         with open(OBJECTS_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
#     elif type == "Character":
#         with open(CHARACTERS_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
#     else:
#         with open(TILES_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)

#     for obj in parsed_data:
#         if (obj["name"].lower() == name.lower()) and (obj["state"].lower() == state.lower()):
#             if obj["interactions"] is not None:
#                 for interac in obj["interactions"]:
#                     # if the interaction name matches, print its details...:
#                     if interac["name"].lower() == interaction_key.lower():
#                         return interac
#     return None

# def lookup_movable (tile_name,state):
#     # Given a tile name and state, return the matching movable flag.
#     # Return None if not match

#     found_tile = False

#     with open(TILES_JSON_FILE, 'r') as file:
#         parsed_tile_data = json.load(file)

#     for tile in parsed_tile_data:
#         if (tile["name"].lower() == tile_name.lower()) and (tile["state"].lower() == state.lower()):
#             found_tile = True
#             return tile["movable"]

#     if found_tile == False:
#         return None
    
# def lookup_current_hp(name,state):
#     with open(CHARACTER_TEMPLATE_JSON_FILE, 'r') as file:
#         char_template = json.load(file)
    
#     for char in char_template:
#         if name.lower() == char["name"].lower() and state.lower() == char["state"]:
#             return char["current_hp"]

# def lookup_max_hp(name,state):
#     with open(CHARACTER_TEMPLATE_JSON_FILE, 'r') as file:
#         char_template = json.load(file)
    
#     for char in char_template:
#         if name.lower() == char["name"].lower() and state.lower() == char["state"]:
#             return char["max_hp"]  

# def lookup_inventory(name,state):
#     with open(CHARACTER_TEMPLATE_JSON_FILE, 'r') as file:
#         char_template = json.load(file)
    
#     for char in char_template:
#         if name.lower() == char["name"].lower() and state.lower() == char["state"]:
#             return char["inventory"]  

# def lookup_char_gold(name,state):
#     with open(CHARACTER_TEMPLATE_JSON_FILE, 'r') as file:
#         char_template = json.load(file)
    
#     for char in char_template:
#         if name.lower() == char["name"].lower() and state.lower() == char["state"]:
#             return char["current_gold"]  


# def lookup_tile_type (tile_name,state):
#     # Given a tile name and state, return the matching movable flag.
#     # Return None if not match

#     found_tile = False

#     with open(TILES_JSON_FILE, 'r') as file:
#         parsed_tile_data = json.load(file)

#     for tile in parsed_tile_data:
#         if (tile["name"].lower() == tile_name.lower()) and (tile["state"].lower() == state.lower()):
#             found_tile = True
#             return tile["type"]

#     if found_tile == False:
#         return None
    
# def lookup_gold_amt (name, state):
#     # Given an object name and state, return the matching gold_amt.
#     # Return None if not match


#     with open(OBJECTS_JSON_FILE, 'r') as file:
#         parsed_object_data = json.load(file)


#         found_object = False

#         for obj in parsed_object_data:

#             if (obj["name"].lower() == name.lower()) and (obj["state"].lower() == state.lower()):

#                 # print("DEBUG: found_object: ", found_object)

#                 found_object = True                
#                 return obj["gold_amt"]
                
#         if found_object == False:
#             return None
        
# def lookup_type (general_type,name, state):
#     # returns the type value given a name and state and general type matched from JSON 
    
#     if general_type == "Object":
#         with open(OBJECTS_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
#     elif general_type == "Character":
#         with open(CHARACTERS_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
#     else:
#         with open(TILES_JSON_FILE, 'r') as file:
#             parsed_data = json.load(file)
            
#     for obj in parsed_data:
#         if (obj["name"].lower() == name.lower()) and (obj["state"].lower() == state.lower()):
#             return obj["type"]
#     return None

