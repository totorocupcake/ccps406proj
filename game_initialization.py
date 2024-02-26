import classes.World_State as World_State
import load_Chars_and_Objs_temp as load_Chars_and_Objs
import classes.Object as Object
import classes.Tile as Tile
import text_file_processor

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS

def initialize(starting_rent_amount, starting_rent_due_date):
    # Needs to return 1 world state object instance
    # Instantiate all neccessary classes so we have a complete world state object to return for game loop

    # NOTE: we don't really need the above function parameters, only need:
    
    load_game=input("Would you like to load game, or create a new game? ")
    
    load_game=load_game.strip()
    
    if load_game =="load" or load_game == "load game":
        load_game = 'Y'
    else:
        load_game= 'N'
    
    world_state = load_World_State(starting_rent_amount, starting_rent_due_date,load_game)

    if load_game == 'N':
        # prompt for player name and display welcome message if new game
        world_state = initial_game_prompt(world_state)
    
    return world_state

def initial_game_prompt(world_state):
    # Any initial game prompts, or initial game updates need to be defined here before we enter main game loop
    
    # ****************************************************
    
    print("Welcome to our game!")
    player_name=input("Please enter the name of your character: ")
    player_name = player_name.strip()
    
    for charac in world_state.get_characters():
        # Find the player and update their name
        if charac.get_type()=="player":
            charac.set_name(player_name)
            break
        
    return world_state
    
def load_World_State(rent_amount, rent_due_date,load_game):
  # Create and return a fully loaded World_State object:

  ws = World_State.World_State()

  tile_2D_list = load_tile_2D_array_from_file(load_game)

  # load the 2D Tiles array:
  ws.load_2D_Tiles_array(tile_2D_list)

  # load the Characters list:
  char_list = load_Chars_and_Objs.load_characters_list_from_file(load_game)

  # for each character, add it to World_State characters list:
  if char_list is not None:
    for char_elem in char_list:
      ws.spawn_character(char_elem)

  # set all other attributes:
  # set turn to 1 to start (initialized to 0 in World_State constructor)
  ws.increment_turn(1)
  ws.set_game_won("N")
  ws.update_rent_amount(rent_amount)
  ws.update_rent_turn_due(rent_due_date)

  return ws

def get_object_list_by_tile_location(x_coord, y_coord,load_game):

  obj_list = load_Chars_and_Objs.load_objects_list_from_file(load_game)

  found = False

  found_obj_list = []

  for obj_elem in obj_list:
    obj_x, obj_y = obj_elem.get_coords()
    if (obj_x == x_coord) and (obj_y == y_coord):
      found = True
      found_obj_list.append(obj_elem)

  if found:
    return found_obj_list
  else:
    return None

def get_tile_by_name_and_state(name, state):
  # creates and returns a tile object from load_tile_JSON_data_file()
  #   based on a give tile 'name' and 'state'

  tile_data_list = text_file_processor.load_tile_JSON_data_file()
  
  found = False

  for tile_elem in tile_data_list:

    # if matching tile_id is found
    if (tile_elem["name"] == name) and (tile_elem["state"] == state):
      found = True
      # create and populate a tile object with the appropriate data
      tl = Tile.Tile()
      tl.set_general_type("Tile")
      tl.set_type( tile_elem["type"] )
      tl.set_name(tile_elem["name"])
      tl.set_state(tile_elem["state"])
      tl.set_movable(tile_elem["movable"])

  if found:
    return tl
  else:
    return None

def lookup_tile_Mapping_by_ID(tile_id):
  # returns a tile object from load_tile_JSON_data_file()
  #   based on a give tile_id

  # get the tile mapping data from the file:
  tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  # iterate through tileIDMapping_data list: 
  for tile_elem in tileIDMapping_data:

    # if matching tile_id is found
    if tile_elem["tile_id"] == tile_id:

      # get the corresponding tile object with the appropriate data
      tl = get_tile_by_name_and_state(tile_elem["name"], tile_elem["state"])

      # populate with other data:
      if tl is not None:
        tl.set_tile_id(tile_id)
        tl.set_state(tile_elem["state"])


      return tl

  # if no tile found, return None
  return None

def load_tile_2D_array_from_file(load_game):
  # returns a 2D array/list of tile objects

  # get 2D array of tile ID's from world_map_status_00.csv
  world_map_status_array = text_file_processor.load_world_map_status_csv(load_game)

  # get the JSON array of tile_id_mappings 
  # tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  # get the JSON array of tiles
  # tile_data = text_file_processor.load_tile_JSON_data_file()

  num_rows = WORLD_MAP_NUM_ROWS
  num_cols = WORLD_MAP_NUM_COLUMNS

  tile_2D_list = []

  for i in range(num_cols):
    inner_array = []
    for j in range(num_rows):
      tile_id = world_map_status_array[j][i]
      tl = lookup_tile_Mapping_by_ID(tile_id)

      # update_coords of tile:
      tl.update_coords((i, j))

      # update Tile inventory:
      obj_list = get_object_list_by_tile_location(i, j,load_game)

      # add objects to tile inventory if found:
      if obj_list is not None:
        tl.update_inventory("add", obj_list)

      inner_array.append(tl)

    tile_2D_list.append(inner_array)
    
  turn_count_data = text_file_processor.load_world_map_turn_status(load_game)
  
  for element in turn_count_data:
    # append turn count status to each tile in json file
    tile_2D_list[element["co_ord_x"]][element["co_ord_y"]].update_turn_counter(element["turn_count"],element["turn_state"])

  return tile_2D_list