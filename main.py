import game_initialization
import game_loop
import classes.Data as Data

STARTING_RENT_AMOUNT = 20
STARTING_RENT_DUE_DATE = 100

if __name__ == "__main__":
    
    """
    Text parsing
    """
    # Initialize read-only files into data object which is a Singleton class.
    data = Data.Data()
    
    """
    Game initialization
    """
    world_state = game_initialization.initialize(STARTING_RENT_AMOUNT, STARTING_RENT_DUE_DATE)
    
    # This should return one object which is an instance of the world_state class.
    # Within this world_state class, it contains all the tiles/characters and objects within their inventory
    # which we will manipulate and lookup within game loop.
    
    """
    Game Loop
    """
    world_state=game_loop.play_game(world_state)
    
    """
    Exit game loop
    """
    if (world_state.get_game_won() == 'Y'): 
        print("You win!")
    else: 
        # runs on manual exit
        print("Goodbye.")
