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
            
def serialize_object(obj):
    current_x,current_y = obj.get_coords()
    return {"co_ord_x":current_x, "co_ord_y":current_y, "turn_count": obj.get_turn_count(), "turn_state":obj.get_turn_state()}

       
def save_world_status_turn_counter (world_state):
    world_map = world_state.get_tiles()
    turn_counter_list =[]
    
    for row in world_map:
        for element in row:
            if element.get_turn_state() != "":
                turn_counter_list.append(serialize_object(element))
                
    with open('save_files/world_map_turn_status.json', 'w') as file:
        json.dump(turn_counter_list, file, indent=4)