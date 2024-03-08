import classes.Turn_Based_Entity as Turn_Based_Entity
import text_file_processor
import classes.Object as Object

class Character(Turn_Based_Entity.Turn_Based_Entity):

    # CLASS CONSTRUCTOR
    def __init__(self, name = None, state = None, coords = None): 
        # call super class constructor:
        super().__init__()

        self.set_name(name)
        self.set_state(state)
        self._general_type = "Character"
        self.__visited = set()
        self.__active_player = ""
        
        if name is not None and state is not None:
        
            template_char = text_file_processor.load_char_template_file()
            
            for element in template_char:
                if element["name"].lower() == name.lower() and element["state"].lower()==state.lower():
                    self.set_type(element["type"])
                    self.set_current_hp(element["current_hp"])
                    self.set_max_hp(element["max_hp"])
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



    def increment_current_gold(self, increment_gold_amount):
        # increment amount can be positive or negative
        self.__current_gold += increment_gold_amount
        


    def set_active_player (self, is_active): 
        if is_active == True: 
            self.__active_player = 'Y'
        else: 
            self.__active_player = 'N'
    
    def turn_count_reached(self,data):
        # sets new state based on turn state, then resets the turn counter
        
        self.set_state(self.get_turn_state())
        self.update_turn_counter (0, "")





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