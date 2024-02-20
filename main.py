import text_file_processor
import game_initialization
import game_loop

STARTING_RENT_AMOUNT = 10
STARTING_RENT_DUE_DATE = 25

if __name__ == "__main__":
    
    """
    Text parsing
    """
    # NOTE: below are not needed, loading is done in respective loader files, ie, 
    #    load_World_State_temp.py etc. 
    #    and called in game_initialization.initialize() function

    # object_status = text_file_processor.load_object_status_file()
    # character_status= text_file_processor.load_character_status_file()
    # world_map_status = text_file_processor.load_world_map_status_csv()
    # tile_id_mapping = text_file_processor.load_tileIDMapping_file()
    
    """
    Game initialization
    """
    # world_state = game_initialization.intialize(object_status, character_status,world_map_status,tile_id_mapping)
    
    # updated the initialize function in game_initialization.py:
    world_state = game_initialization.initialize(STARTING_RENT_AMOUNT, STARTING_RENT_DUE_DATE)
    world_state = game_initialization.initial_game_prompt(world_state)
    
    # This should return one object which is an instance of the world_state class.
    # Within this world_state class, it contains all the tiles/characters and objects within their inventory
    # which we will manipulate and lookup within game loop.
    
    """
    Game Loop
    """
    world_state=game_loop.play_game(world_state)
    
    
    #exit_game_loop()
    #utility()