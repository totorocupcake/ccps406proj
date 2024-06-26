import classes.Entity as Entity
import sys

class Turn_Based_Entity(Entity.Entity):
    def __init__(self): 
        super().__init__()

        self._turn_count = 0
        self._turn_state = ""

    
    def get_turn_count(self):
        return self._turn_count
    
    def get_turn_state(self):
        return self._turn_state
    
    def set_turn_count(self,new_turn_count):
        
        if not isinstance(new_turn_count, int):
            sys.stderr.write("Error: Turn counter value is invalid\n")
            sys.exit(1)
        
        self._turn_count = new_turn_count
    
    def decrement_turn_count(self):
        if self._turn_state != "" and self._turn_state != "null":
            # check if there is a valid turn state in order to decrement turn counter
            self._turn_count -= 1
            
            if self._turn_count == 0:
                # we waited enough turns, now need to update the tile/character object based on new state in turn_state
                self.turn_count_reached()
        
    def update_turn_counter(self, turn_no, turn_state):
        
        if not isinstance(turn_no, int) and not isinstance(turn_state, str):
            sys.stderr.write("Error: Turn counter value is invalid\n")
            sys.exit(1)

        self._turn_count = turn_no
        self._turn_state = turn_state
    
    def turn_count_reached(self):
        # needs to be overridden in child classes (Tile and Character) to update the fields based on new state stored in turn_state
        pass
