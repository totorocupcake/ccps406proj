import Character
import Tile
import Object
import World_State

import load_World_State_temp as load_World_State

# not sure if we need these, but we can import anyway:
import text_file_processor
import Entity
import Turn_Based_Entity


# def initialize(object_status, character_status,world_map_status,tile_id_mapping):

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
    
    world_state = load_World_State.load_World_State(starting_rent_amount, starting_rent_due_date,load_game)

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
    

if __name__ == "__main__":

    pass 

