import csv
import json

def save_world_status (world_state):
    # save csv of tile id from given world state
    
    world_map = world_state.get_tiles()
    transposed_world_map= [list(row) for row in zip(*world_map)]

    with open("save_files/world_map_status_save.csv","w", newline = '') as file:
        writer = csv.writer(file)
        
        for row in transposed_world_map:
            row_data = [element.get_tile_id() for element in row]
            writer.writerow(row_data)
            
def serialize_tile_object(tile):
    current_x,current_y = tile.get_coords()
    return {"co_ord_x":current_x, "co_ord_y":current_y, "turn_count": tile.get_turn_count(), "turn_state":tile.get_turn_state()}

       
def save_world_status_turn_counter (world_state):
    world_map = world_state.get_tiles()
    turn_counter_list =[]
    
    for row in world_map:
        for element in row:
            if element.get_turn_state() != "":
                turn_counter_list.append(serialize_tile_object(element))
                
    with open('save_files/world_map_turn_status.json', 'w') as file:
        json.dump(turn_counter_list, file, indent=4)

def serialize_item(item):

    return {
        "name": item.name,  
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

    return{"type":charac.get_type(),
           "name": charac.name,
           "co_ord_x":current_x,
           "co_ord_y":current_y,
           "state": charac.get_state(),
           "inventory": inventory_serialized,
           "current_hp":charac.get_current_hp(),
           "max_hp":charac.get_max_hp(),
           "current_gold": charac.get_current_gold(),
           "visited":visited_serialized,
            "turn counter": turn_counter_serialized
           
           }
        
def save_character_status (world_state):
    characters = world_state.get_characters()
    characters_list = []
    
    for charac in characters:
        characters_list.append(serialize_character(charac))
    
    with open('save_files/char_status_save.json', 'w') as file:
        json.dump(characters_list, file, indent=4)
        
def serialize_object(item):
    current_x,current_y = item.get_coords()
    inventory_serialized = [serialize_item(obj) for obj in item.get_inventory()]
    if inventory_serialized == []:
        inventory_serialized =None

    return {
        "type": item.get_type(),
        "name": item.name,  
        "state": item.get_state(),
        "quantity": item.get_quantity(),  
        "co_ord_x":current_x,
        "co_ord_y":current_y,
        "inventory": inventory_serialized
        
    }        
        
def save_obj_status (world_state):
    world_map = world_state.get_tiles()
    objects=[]
    objects_list = []
    
    for row in world_map:
        for tile in row:
            if tile.get_inventory() !=[]:
                objects.extend(tile.get_inventory())
    print(objects)
    
    for obj in objects:
        objects_list.append(serialize_object(obj))
    
    with open('save_files/objects_status_save.json', 'w') as file:
        json.dump(objects_list, file, indent=4)