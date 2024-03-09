import classes.World_State as World_State
import classes.Object as Object
import classes.Tile as Tile
import text_file_processor
import classes.Character as Character
import classes.Data as Data

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
  char_list = load_characters_list_from_file(load_game)

  # for each character, add it to World_State characters list:
  if char_list is not None:
    for char_elem in char_list:
      ws.spawn_character(char_elem)

  # set all other attributes:
  # set turn to 1 to start (initialized to 0 in World_State constructor)
  
  
  if load_game == 'Y':
    data = text_file_processor.load_rent_data()
    ws.set_game_won(data["game_won"])
    ws.set_turn_number(data["turn_number"])
    ws.update_rent_amount(data["rent_amount"])
    ws.update_rent_turn_due(data["rent_due_date"])
  else:
    ws.set_game_won("N")
    ws.update_rent_amount(rent_amount)
    ws.update_rent_turn_due(rent_due_date)
    ws.increment_turn(1)
  
  return ws

def get_object_list_by_tile_location(x_coord, y_coord,load_game):

  obj_list = load_objects_list_from_file(load_game)

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
  # creates and returns a tile object from load_tile_JSON_data_file() based on a given tile 'name' and 'state'
  # NOTE: refactored to be shorter by utilizing class methods of tile class

  tl = Tile.Tile()
  tl.set_name(name)
  tl.update_tile_by_state(state)
  return tl

  # tile_data_list = text_file_processor.load_tile_JSON_data_file()
  
  # found = False

  # for tile_elem in tile_data_list:

  #   # if matching tile_id is found
  #   if (tile_elem["name"] == name) and (tile_elem["state"] == state):
  #     found = True
  #     # create and populate a tile object with the appropriate data
  #     tl = Tile.Tile()
  #     tl.set_general_type("Tile")
  #     tl.set_type( tile_elem["type"] )
  #     tl.set_name(tile_elem["name"])
  #     tl.set_state(tile_elem["state"])
  #     tl.set_movable(tile_elem["movable"])

  # if found:
  #   return tl
  # else:
  #   return None

def lookup_tile_Mapping_by_ID(tile_id):
  # returns a tile object from load_tile_JSON_data_file() based on a given tile_id
  # NOTE: refactored to be shorter by utilizing class methods of tile class

  tl = Tile.Tile()
  tl.update_tile_by_id(tile_id)
  return tl

  # get the tile mapping data from the file:
  # tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  # # iterate through tileIDMapping_data list: 
  # for tile_elem in tileIDMapping_data:

  #   # if matching tile_id is found
  #   if tile_elem["tile_id"] == tile_id:

  #     # get the corresponding tile object with the appropriate data
  #     tl = get_tile_by_name_and_state(tile_elem["name"], tile_elem["state"])

  #     # populate with other data:
  #     if tl is not None:
  #       tl.set_tile_id(tile_id)
  #       tl.set_state(tile_elem["state"])


  #     return tl

  # if no tile found, return None
  # return None

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
    # append turn count status and current gold to each tile in json file 
    tile_2D_list[element["co_ord_x"]][element["co_ord_y"]].update_turn_counter(element["turn_count"],element["turn_state"])
    tile_2D_list[element["co_ord_x"]][element["co_ord_y"]].increment_current_gold(element["gold"])

  return tile_2D_list

def load_objects_list_from_file(load_game):
  # returns a list of 'object' objects that have been populated with 
  # data from the objects status JSON file via text_file_processor.py


  # get JSON object status data from file via text_file_processor.py
  object_status_data = text_file_processor.load_object_status_file(load_game)
  
  # Create an empty list to store objects
  objects = []
  
  # iterate through object status JSON data and create/populate a 'Object' 
  #    object for each one, then append each to the list 'objects'
  
  for obj_elem in object_status_data:
    obj = Object.Object()

    # set all 'Object' object attributes
    obj.set_name(obj_elem["name"])

    # need a general_type for looking up descriptions in text_file_processor.py
    obj.set_general_type("Object")

    obj.set_type(obj_elem["type"])
    obj.set_state(obj_elem["state"])


    # *********
    #   All other attributes of the 'Object' class
    #   from object_status_data (JSON data):
    # *********

    obj.update_qty(obj_elem["quantity"])
    obj.update_coords((obj_elem["co_ord_x"], obj_elem["co_ord_y"]))
    
    # need to add gold_amt, look-up from 'objects_02n.json' via 'text_file_processor'
    obj.set_gold_amt = Data.Data().lookup_gold_amt(obj.get_name(), obj.get_state())

    # for each item in 'inventory' create an 'Object' object, and add it to inventory:
    if obj_elem["inventory"] is not None:

      # update_inventory, if its not empty
      for inv_elem in obj_elem["inventory"]:

        inv_obj = Object.Object()
        inv_obj.set_name = inv_elem["name"]
        inv_obj.update_qty(inv_elem["quantity"])
        inv_obj.set_state(inv_elem["state"])

        obj.update_inventory("add", inv_obj)


    # append the 'Object' object to the 'objects' list of objects
    objects.append(obj)

  # return objects list
  return objects

def load_characters_list_from_file(load_game):
  # returns a list of character objects that have been populated with 
  # data from the character status JSON file via text_file_processor.py


  # get JSON characters status data from file via text_file_processor.py
  character_status_data = text_file_processor.load_character_status_file(load_game)

  # Create an empty list to store characters
  characters = []
  
  # iterate through chacter status JSON data and create/populate a Character 
  #    object for each one, then append each to the list 'characters'
  for char_elem in character_status_data:
    charac = Character.Character()

    # set all character object attributes
    charac.set_name(char_elem["name"])

    charac.set_general_type("Character")

    charac.set_type(char_elem["type"])
    charac.set_state(char_elem["state"])

    # if player type is "player", set to active player:
    if char_elem["type"] == "player":
      charac.set_active_player(True)
    else:
      charac.set_active_player(False)


    charac.update_coords((char_elem["co_ord_x"] , char_elem["co_ord_y"]))

    # update_inventory, if its not empty
    if char_elem["inventory"] is not None:
      inv_list_of_ojb = []
      for inv_elem in char_elem["inventory"]:

        inv_obj = Object.Object()

        inv_obj.set_name(inv_elem["name"])

        inv_obj.update_qty(inv_elem["quantity"])
        inv_obj.set_state(inv_elem["state"])

        inv_list_of_ojb.append(inv_obj)
       
      charac.update_inventory("add", inv_list_of_ojb)

    charac.set_current_hp(char_elem["current_hp"])
    charac.set_max_hp(char_elem["max_hp"])
    charac.set_current_gold(char_elem["current_gold"])

    # add to visited, if any:
    if char_elem["visited"] is not None:
      for visit_elem in char_elem["visited"]:
        charac.update_visited(visit_elem["type"], visit_elem["name"], visit_elem["state"])

    # set/update the turn counter:
    charac.update_turn_counter( char_elem["turn_counter"][0], char_elem["turn_counter"][1] )

    # append the character object to the 'characters' list of objects
    characters.append(charac)

  # return characters list
  return characters

