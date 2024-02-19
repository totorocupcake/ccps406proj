import Turn_Based_Entity

class Character(Turn_Based_Entity.Turn_Based_Entity):

    # CLASS CONSTRUCTOR
    def __init__(self): 
        self.inventory = []
        self.__general_type = "Character"

        self.__current_hp = 0
        self.__max_hp = 0
        self.__current_gold = 0

        # should __visited by a set (of tuples) rather than a list?
        # was: self.__visited = []
        self.__visited = set()
        self.__active_player = ""
        self.__turn_counter = 0
        self.__turn_state = ""


    # GETTER METHODS
    def get_inventory(self):
        # returns a list of 'object' objects
        return self.inventory


    # char class specific methods:
    def get_current_hp (self): 
        return self.__current_hp
    
    def get_max_hp (self): 
        return self.__max_hp
    
    def get_current_gold (self): 
        return self.__current_gold
    
    def get_visited (self): 
        return self.__visited
    
    def get_active_player (self): 
        return self.__active_player
    
    def get_turn_counter (self): 
        return self.__turn_counter
    
    def get_turn_state (self): 
        return self.__turn_state        



    # SETTER METHODS

    # char class specific methods:
    def set_current_hp (self, new_current_hp): 
        self.__current_hp = new_current_hp
    
    def set_max_hp (self, new_max_hp): 
        self.__max_hp = new_max_hp
    
    def set_current_gold (self, new_current_gold): 
        self.__current_gold = new_current_gold

    def set_visited (self, new_visited): 
        self.__visited = new_visited

    def update_visited(self, type, name, state):
        # check if its already in the set, 
        #   if not, add the tuple to the set:
        if (type, name, state) not in self.__visited:
            self.__visited.add( (type, name, state) )


    def set_active_player (self, is_active): 
        if is_active == True: 
            self.__active_player = 'Y'
        else: 
            self.__active_player = 'N'
            

    """
    Handled in turn_based_entity superclass, commenting out for now
   
    def set_turn_counter (self): 
        self.__turn_counter = self.__turn_counter + 1
    
    def set_turn_state (self, new_turn_state): 
        self.__turn_state = new_turn_state

    """






if __name__ == "__main__": 

    charac = Character()
    charac.update_turn_counter(1, "null")

    pass