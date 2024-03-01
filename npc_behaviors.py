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

def thief_aggressive(world_state,charac):
    for element in world_state.get_characters():
        # find the player character (note may not be the active player)
        if element.get_type() == "player":
            player = element
            break

    if player.get_coords() == charac.get_coords():
    # steal gold from player if on same tile
        player_name = player.get_name()
        next_command="steal "+ player_name
        print("The thief stole gold from ",player_name)
        return next_command
    
    return check_graze(world_state,charac)

def wolf_aggressive(world_state,charac):
    char_list = world_state.get_chars_at_tile(charac.get_coords())
      
    for char in char_list:
        if char.get_name() == "chicken":
          #print("Wolf submitted command to kill chicken")
          return "kill chicken"
        elif char.get_name() == "cow":
          #print("Wolf submitted command to kill cow")
          return "kill cow"

    return check_graze(world_state,charac)
    
def cow_wild(world_state,charac):
    if world_state.get_graze() == 'Y':
        if (world_state.get_turn_number() % 2) == 0:
          next_command = graze(world_state,charac)
          return next_command
    return None

def check_graze(world_state,charac):
    if world_state.get_graze() =="Y":
      # graze as default if no other action for thief,chicken,wolf
      next_command = graze(world_state,charac)
      return next_command
    else:
      return None