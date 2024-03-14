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
LOAD_RENT_INFO_JSON_FILE = "save_files/rent_info.json"

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

def load_rent_data():
    file_to_load = LOAD_RENT_INFO_JSON_FILE

    with open(file_to_load, 'r') as file:
        parsed_rent_info_data = json.load(file)

    return parsed_rent_info_data 

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