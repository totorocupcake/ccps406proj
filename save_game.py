import csv
import json
import functools

CHARACTER_STATUS_PATH = "save_files/char_status_save.json"
OBJ_STATUS_PATH = "save_files/objects_status_save.json"
WORLD_CSV_PATH = "save_files/world_map_status_save.csv"
WORLD_TURN_STATUS_PATH = "save_files/world_map_turn_status.json"
WORLD_GLOBAL_INFO_PATH = "save_files/rent_info.json"

def save_game(world_state):
    
    if( save_world_status(world_state) and save_world_status_turn_counter(world_state) \
        and save_character_status(world_state) and save_obj_status(world_state) \
        and save_rent_info(world_state)):
        print ("Game saved to save_files subfolder.")
    else:
        print("An error occurred while trying to save the game.")
    
def error_handler(func):
    # Error handler to wrap around each save function to detect errors in attempt to write to save files
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Attempt to call the function
        except PermissionError:
            return False
        except OSError as e:
            return False
        except Exception as e:
            return False
    return wrapper

# Helper functions to convert objects into dictionary first before converting to text files ##################################### 

def serialize_tile_object(tile):
    current_x,current_y = tile.get_coords()
    return {"co_ord_x":current_x, 
            "co_ord_y":current_y, 
            "turn_count": tile.get_turn_count(), 
            "turn_state":tile.get_turn_state(),
            "gold": tile.get_current_gold()}

def serialize_item(item):
    return {
        "name": item.get_name(),  
        "quantity": item.get_quantity(),  
        "state": item.get_state()  
    }
    
def serialize_visited(visited_set):
    return {
        "type": visited_set[0],
        "name":visited_set[1],
        "state":visited_set[2]  
    }

def serialize_character (charac):
    current_x,current_y = charac.get_coords()

    inventory_serialized = [serialize_item(item) for item in charac.get_inventory()]
    visited_serialized = [serialize_visited(item) for item in charac.get_visited()]
    turn_counter_serialized = [charac.get_turn_count(), charac.get_turn_state()]

    if inventory_serialized == []:
        inventory_serialized = None
    
    if visited_serialized == []:
        visited_serialized = None
    
    if turn_counter_serialized == []:
        turn_counter_serialized = None

    return{"type":charac.get_type().name,
           "name": charac.get_name(),
           "co_ord_x":current_x,
           "co_ord_y":current_y,
           "state": charac.get_state(),
           "inventory": inventory_serialized,
           "current_hp":charac.get_current_hp(),
           "max_hp":charac.get_max_hp(),
           "current_gold": charac.get_current_gold(),
           "visited":visited_serialized,
            "turn_counter": turn_counter_serialized
           }
        
def serialize_object(item):
    current_x,current_y = item.get_coords()
    inventory_serialized = [serialize_item(obj) for obj in item.get_inventory()]
    if inventory_serialized == []:
        inventory_serialized =None

    return {
        "type": item.get_type().name,
        "name": item.get_name(),  
        "state": item.get_state(),
        "quantity": item.get_quantity(),  
        "co_ord_x":current_x,
        "co_ord_y":current_y,
        "inventory": inventory_serialized
        }        

# Functions to save each file ######################################################################################

@error_handler
def save_character_status (world_state):
    characters = world_state.get_characters()
    characters_list = []
    
    for charac in characters:
        characters_list.append(serialize_character(charac))
    
    with open(CHARACTER_STATUS_PATH, 'w') as file:
        json.dump(characters_list, file, indent=4)
        
    return True

@error_handler
def save_obj_status (world_state):
    world_map = world_state.get_tiles()
    objects=[]
    objects_list = []
    
    for row in world_map:
        for tile in row:
            if tile.get_inventory() !=[]:
                objects.extend(tile.get_inventory())
    
    for obj in objects:
        objects_list.append(serialize_object(obj))
    
    with open(OBJ_STATUS_PATH, 'w') as file:
        json.dump(objects_list, file, indent=4)
    
    return True

@error_handler
def save_world_status (world_state):
    # save csv of tile id from given world state
    
    world_map = world_state.get_tiles()
    transposed_world_map= [list(row) for row in zip(*world_map)]

    with open(WORLD_CSV_PATH,"w", newline = '') as file:
        writer = csv.writer(file)
        
        for row in transposed_world_map:
            row_data = [element.get_tile_id() for element in row]
            writer.writerow(row_data)
    
    return True

@error_handler
def save_world_status_turn_counter (world_state):
    world_map = world_state.get_tiles()
    turn_counter_list =[]
    
    for row in world_map:
        for element in row:
            if (element.get_turn_state() != "") or (element.get_current_gold() != 0) :
                turn_counter_list.append(serialize_tile_object(element))
                
    with open(WORLD_TURN_STATUS_PATH, 'w') as file:
        json.dump(turn_counter_list, file, indent=4)
    
    return True

@error_handler
def save_rent_info (world_state):
    dict = {
        "rent_amount": world_state.get_rent_amount(),
        "rent_due_date": world_state.get_rent_due_date(),
        "turn_number": world_state.get_turn_number(),
        "game_won": world_state.get_game_won()
        }  
    
    with open(WORLD_GLOBAL_INFO_PATH, 'w') as file:
        json.dump(dict, file, indent=4)
    
    return True
    
