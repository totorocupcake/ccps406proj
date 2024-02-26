import World_State
import load_Tiles_temp as load_Tiles
import load_Chars_and_Objs_temp as load_Chars_and_Objs

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

  tile_2D_list = load_Tiles.load_tile_2D_array_from_file(load_game)

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