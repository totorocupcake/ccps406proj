import Entity


class Turn_Based_Entity(Entity.Entity):
  # CLASS CONSTRUCTOR
    def __init__(self): 
        super().__init__()

        self._turn_count = 0
        self._turn_state = ""

    
    def get_turn_count(self):
        return self._turn_count
    
    def set_turn_count(self,new_turn_count):
        self._turn_count = new_turn_count
    
    def decrement_turn_count(self):
        if self._turn_state != "":
            # check if there is a valid turn state in order to decrement turn counter
            self._turn_count -= 1
            
            if self._turn_count == 0:
                # we waited enough turns, now need to update the tile/character object based on new state in turn_state
                self.turn_count_reached()
        
    def get_turn_state(self):
        return self._turn_state

    def update_turn_counter(self, turn_no, turn_state):
        self._turn_count = turn_no
        self._turn_state = turn_state
    
    def turn_count_reached(self):
        # needs to be overridden in child classes (Tile and Character) to update the fields based on new state stored in turn_state
        pass
    
"""
Some test scripts below

test = Turn_Based_Entity()
test.set_turn_counter(5, "ready")
print(test.get_turn_count())
print(test.get_turn_state())

"""