class entity:
    # template for superclass of all other classes
    
class turn_count:
    # template for superclass of tile and characters
    # turn counting specific capabilities

class tile:  
    # template for tile
    
class object:
    # template for objects (items in the game)
class character:
    # template for characters (includes npcs, monsters, active player)
    
class world_state:
    # template of world_state

def initialize(object_status, character_status,world_map_status,tile_id_mapping):
    # Needs to return 1 world state object instance
    # Instantiate all neccessary classes so we have a complete world state object to return for game loop
    
    pass

def initial_game_prompt(world_state):
    # Any initial game prompts, or initial game updates need to be defined here before we enter main game loop
    pass