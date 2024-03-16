import game_initialization
import game_loop
import classes.Data as Data

STARTING_RENT_AMOUNT = 20
STARTING_RENT_DUE_DATE = 100

if __name__ == "__main__":
    
    # Initialize read-only files into data object which is a Singleton class.
    data = Data.Data()

    world_state = game_initialization.initialize(STARTING_RENT_AMOUNT, STARTING_RENT_DUE_DATE)

    world_state=game_loop.play_game(world_state)
    
    """
    Exit game loop
    """
    
    if (world_state.get_game_won() == 'Y'): 
        print("You win!")
    else: 
        # runs on manual exit
        print("Goodbye.")
