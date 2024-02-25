import random

def graze(world_state,charac):
      # get_next_action sub function to define a generic "Grazing" behavior for wild cow/chicken
      # should move randomly n,w,e,w if there is grassland available for them
        
    available_directions = [] 
    current_x,current_y = charac.get_coords()
        
    max_cols = len(world_state.get_tiles()[0])-1
    max_rows = len(world_state.get_tiles())-1
        
    # check if n,s,e,w is available to move to and is a grassland
    if current_y+1 >= 0 and current_y+1 <= max_cols and world_state.get_tiles()[current_x][current_y+1].get_name() == "grasslands":
        available_directions.append("n")
    if current_y-1 >= 0 and current_y-1 <= max_cols and world_state.get_tiles()[current_x][current_y-1].get_name() == "grasslands":
        available_directions.append("s")
    if current_x+1 >= 0 and current_x+1 <= max_rows and world_state.get_tiles()[current_x+1][current_y].get_name() == "grasslands":
        available_directions.append("e")
    if current_x-1 >= 0 and current_x-1 <= max_rows and world_state.get_tiles()[current_x-1][current_y].get_name() == "grasslands":
        available_directions.append("w")
        
    # returns random direction from available_directions list
    next_command_graze = random.choice(available_directions)
    return next_command_graze
  