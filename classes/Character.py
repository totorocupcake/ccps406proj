import classes.Turn_Based_Entity as Turn_Based_Entity
import text_file_processor
import classes.Object as Object
import text_formatting

class Character(Turn_Based_Entity.Turn_Based_Entity):

    # CLASS CONSTRUCTOR
    def __init__(self, name = None, state = None, coords = None): 
        # call super class constructor:
        super().__init__()

        self.set_name(name)
        self.set_state(state)
        self._general_type = "Character"
        self.__visited = set()
        self.__active_player = "N"
        self.__max_hp = 0
        self.__current_hp = 0
        
        if name is not None and state is not None:
        
            template_char = text_file_processor.load_char_template_file()
            
            for element in template_char:
                if element["name"].lower() == name.lower() and element["state"].lower()==state.lower():
                    self.set_type(element["type"])
                    self.set_max_hp(element["max_hp"])
                    self.set_current_hp(element["current_hp"])
                    self.set_current_gold(element["current_gold"])
                    self.update_turn_counter(element["turn_counter"][0],element["turn_counter"][1])
                    if element["inventory"] is not None:
                        inv_list_of_obj = []
                        for inv_elem in element["inventory"]:
                            inv_obj = Object.Object()
                            inv_obj.set_name(inv_elem["name"])
                            inv_obj.update_qty(inv_elem["quantity"])
                            inv_obj.set_state(inv_elem["state"])
                            inv_list_of_obj.append(inv_obj)
                        self.update_inventory("add", inv_list_of_obj)
                    if coords is None:
                        self.update_coords((element["co_ord_x"],element["co_ord_y"]))
                    else:
                        x,y = coords
                        self.update_coords((x,y))
                    break
        
        # should __visited by a set (of tuples) rather than a list?
        # was: self.__visited = []
        
    

    # GETTER METHODS

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


    # SETTER METHODS

    # char class specific methods:
    def set_current_hp (self, new_current_hp,world_state=None):
        if new_current_hp > 0 and new_current_hp <= self.get_max_hp():
            self.__current_hp = new_current_hp
            
        elif new_current_hp > self.get_max_hp():
            self.__current_hp = self.get_max_hp()
            
        else:
            process_dead_char(self,world_state)        

        return world_state
    
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



    def increment_current_gold(self, increment_gold_amount):
        # increment amount can be positive or negative
        self.__current_gold += increment_gold_amount
        


    def set_active_player (self, is_active): 
        if is_active == True: 
            self.__active_player = 'Y'
        else: 
            self.__active_player = 'N'
    
    def turn_count_reached(self):
        # sets new state based on turn state, then resets the turn counter
        
        self.set_state(self.get_turn_state())
        self.update_turn_counter (0, "")


def process_dead_char(charac,world_state):
    if charac.get_type() == "player":
        charac.set_current_hp(charac.get_max_hp())
        charac.set_current_gold(0)
        
        for row in world_state.get_tiles():
            for tile in row:
                if tile.get_name().lower() == "bedroom":
                    x,y = tile.get_coords()
                    charac.update_coords((x,y))
                    break
                
        if charac.get_active_player()=='Y':
            print(text_formatting.justify("You wake up in your bedroom, someone managed to rescue you from the farmlands after they saw you heavily injured outside. You lost all your gold on hand."))
    
    else:
        world_state.remove_character(charac)
    
    return world_state


if __name__ == "__main__": 

    charac = Character()
    charac.set_name("cow")
    charac.set_state("tamed_not_hungry")
    charac.update_turn_counter(1, "tamed_ready")

    print("Name: ", charac.name)
    print("State: ", charac.get_state())
    print("Turn count: ", charac.get_turn_count())
    print("Turn State: ", charac.get_turn_state())
    
    charac.decrement_turn_count()
    print("Name: ", charac.name)
    print("State: ", charac.get_state())
    print("Turn count: ", charac.get_turn_count())
    print("Turn State: ", charac.get_turn_state())
    pass