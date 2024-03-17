import classes.World_State as World_State
import classes.Object as Object
import classes.Tile as Tile
import classes.enums as Enum
import text_file_processor
import classes.Character as Character
import classes.Data as Data
import sys

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS

def initialize(starting_rent_amount, starting_rent_due_date):
    
    load_game=input("Would you like to load game, or create a new game? ")
    
    load_game=load_game.strip()
    
    if load_game =="load" or load_game == "load game":
        load_game = True 
    else:
        load_game= False
    
    
    world_state = load_World_State(starting_rent_amount, starting_rent_due_date,load_game)

    check_status = check_world_state(world_state)
    
    if check_status == False:
      sys.stderr.write("Error: Files used to create the game is invalid.\n")
      sys.exit(1)
    
    if not load_game:
        # prompt for player name and display welcome message if new game
        world_state = initial_game_prompt(world_state)
    
    return world_state

def initial_game_prompt(world_state):

    print("Welcome to Farm Quest!")
    player_name=input("Please enter the name of your character: ")
    player_name = player_name.strip()
    
    for charac in world_state.get_characters():
        # Find the player and update their name
        if charac.get_type()==Enum.character_type.player:
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
  
  
  if load_game:
    data = text_file_processor.load_rent_data()
    ws.set_game_won(data["game_won"])
    ws.set_turn_number(data["turn_number"])
    ws.update_rent_amount(data["rent_amount"])
    ws.update_rent_turn_due(data["rent_due_date"])
  else:
    ws.set_game_won(False)
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

  tl = Tile.Tile()
  tl.set_name(name)
  tl.update_tile_by_state(state)
  return tl

def lookup_tile_Mapping_by_ID(tile_id):
  # returns a tile object from load_tile_JSON_data_file() based on a given tile_id

  tl = Tile.Tile()
  tl.update_tile_by_id(tile_id)
  return tl

def load_tile_2D_array_from_file(load_game):
  # returns a 2D array/list of tile objects
  
  # get 2D array of tile ID's from world_map_status_00.csv
  world_map_status_array = text_file_processor.load_world_map_status_csv(load_game)

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

  object_status_data = text_file_processor.load_object_status_file(load_game)
  objects = []
  
  # iterate through object status JSON data and create/populate a 'Object' 
  # object for each one, then append each to the list 'objects'
  
  for obj_elem in object_status_data:
    obj = Object.Object()

    # set all 'Object' object attributes
    obj.set_name(obj_elem["name"])
    obj.set_general_type(Enum.general_type.OBJECT)
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

    objects.append(obj)

  return objects

def load_characters_list_from_file(load_game):
  # returns a list of character objects that have been populated with 
  # data from the character status JSON file via text_file_processor.py

  character_status_data = text_file_processor.load_character_status_file(load_game)
  characters = []
  
  # iterate through character status JSON data and create/populate a Character 
  # object for each one, then append each to the list 'characters'
  for char_elem in character_status_data:
    charac = Character.Character()

    # set all character object attributes
    charac.set_name(char_elem["name"])
    charac.set_general_type(Enum.general_type.CHARACTER)
    charac.set_type(Enum.character_type[char_elem["type"]])
    charac.set_state(char_elem["state"])

    # if player type is "player", set to active player:
    if charac.get_type() == Enum.character_type.player:
      charac.set_active_player(True)
    else:
      charac.set_active_player(False)

    charac.update_coords((char_elem["co_ord_x"] , char_elem["co_ord_y"]))

    if char_elem["inventory"] is not None:
      inv_list_of_ojb = []
      for inv_elem in char_elem["inventory"]:
        inv_obj = Object.Object()
        inv_obj.set_name(inv_elem["name"])
        inv_obj.update_qty(inv_elem["quantity"])
        inv_obj.set_state(inv_elem["state"])
        inv_list_of_ojb.append(inv_obj)
      charac.update_inventory("add", inv_list_of_ojb)
      
    charac.set_max_hp(char_elem["max_hp"])
    charac.set_current_hp(char_elem["current_hp"])
    charac.set_current_gold(char_elem["current_gold"])


    if char_elem["visited"] is not None:
      for visit_elem in char_elem["visited"]:
        charac.update_visited(visit_elem["type"], visit_elem["name"], visit_elem["state"])

    charac.update_turn_counter( char_elem["turn_counter"][0], char_elem["turn_counter"][1] )
    characters.append(charac)
    
  return characters

def check_world_state(world_state):
  if world_state.get_active_char() is None:
    return False
  