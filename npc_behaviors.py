import random

def graze(world_state,charac):
      # get_next_action sub function to define a generic "Grazing" behavior for monsters/animals
      # should move randomly n,w,e,w if there is grassland available for them
    random.seed(42)
    
    available_directions = [] 
    current_x,current_y = charac.get_coords()
        
    max_cols = len(world_state.get_tiles()[0])-1
    max_rows = len(world_state.get_tiles())-1
        
    # check if n,s,e,w is available to move to and is a grassland
    if current_y-1 >= 0 and current_y-1 <= max_cols and world_state.get_tiles()[current_x][current_y-1].get_name() == "grasslands":
        available_directions.append("n")
    if current_y+1 >= 0 and current_y+1 <= max_cols and world_state.get_tiles()[current_x][current_y+1].get_name() == "grasslands":
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
        if element.get_type() == "player":
            player = element
            break

    if player.get_coords() == charac.get_coords():
    # steal gold from player if on same tile
        player_name = player.get_name()
        next_command="steal "+ player_name
        if player.get_active_player():
            print("The thief stole gold from ",player_name)
        return next_command
    
    # thief steals gold if players room is open and has gold in it
    for row in world_state.get_tiles():
        for tile in row:
            if tile.get_name() == "bedroom":
                if tile.get_state() == "open" and tile.get_current_gold()>0:
                    bedroom_coord = tile.get_coords()
                    current_coord = charac.get_coords()
                    
                    if bedroom_coord != current_coord:
                        return navigate_to_coord(bedroom_coord,current_coord)
                    else:
                        print("A wild roaming thief stole gold from your unlocked house!")
                        return "take gold"
                else:
                    break
        
    return check_graze(world_state,charac)

def wolf_aggressive(world_state,charac):
    char_list = world_state.get_chars_at_tile(charac.get_coords())
    current_coord= charac.get_coords()
    x,y = current_coord
    current_tl = world_state.get_tiles()[x][y]
    
    if current_tl.get_movable():
        for char in char_list:
            if char.get_type() == "player":
                if char.get_active_player():
                    print(f"The wolf hit {char.get_name()} for 2 hp.")
                return "hit " +char.get_name()
            
            if char.get_name() == "chicken":
                return "kill chicken"
            
            elif char.get_name() == "cow":
                return "kill cow"
        
    for row in world_state.get_tiles():
        for tile in row:
            if tile.get_name() == "barn" and tile.get_state()=="open":
                for char in world_state.get_chars_at_tile(tile.get_coords()):
                    if char.get_name()=="cow":
                        return navigate_to_coord(tile.get_coords(),charac.get_coords())
            if tile.get_name() == "chicken coop" and tile.get_state()=="open":
                for char in world_state.get_chars_at_tile(tile.get_coords()):
                    if char.get_name()=="chicken":
                        return navigate_to_coord(tile.get_coords(),charac.get_coords())

    return check_graze(world_state,charac)
    
def cow_wild(world_state,charac):
    if world_state.get_graze() == 'Y':
        if (world_state.get_turn_number() % 3) == 0:
          next_command = graze(world_state,charac)
          return next_command
    return None

def check_graze(world_state,charac):
    if world_state.get_graze() =="Y":
        if (world_state.get_turn_number() % 2) == 0:
            next_command = graze(world_state,charac)
            return next_command
        else:
            return None
    else:
      return None

def navigate_to_coord (target_coord,current_coord):
    if target_coord[0]>current_coord[0]:
        return "e"
    elif target_coord[0]<current_coord[0]:
        return "w"
    elif target_coord[1]>current_coord[1]:
        return "s"
    else:
        return "n"