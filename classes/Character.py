import classes.Turn_Based_Entity as Turn_Based_Entity
import text_file_processor
import classes.Object as Object
import text_formatting
import sys
import classes.enums as Enum
import classes.external_files as external_files

class Character(Turn_Based_Entity.Turn_Based_Entity):

    def __new__(cls, *args, **kwargs):
        if args:
            name = args[0] 
            state = args[1] 
        else:
            name,state=None,None
       
        if name is not None and state is not None and not external_files.read_external_files().check_exists(Enum.general_type.CHARACTER,name,state):
            # invalid character, so do not instantiate
            return None
        else:
            return super().__new__(cls)
    
    def __init__(self, name = None, state = None, coords = None): 
        super().__init__()

        self.set_name(name)
        self.set_state(state)
        self._general_type = Enum.general_type.CHARACTER
        self.__visited = set()
        self.__active_player = False
        self.__max_hp = 0
        self.__current_hp = 0
        
        if name is not None and state is not None:
        # Creates a new character from template file based on supplied name and state of char
        
            template_char = text_file_processor.load_char_template_file()
            
            for element in template_char:
                if element["name"].lower() == name.lower() and element["state"].lower()==state.lower():
                    self.set_type(Enum.character_type[element["type"]])
                    self.set_max_hp(element["max_hp"])
                    self.set_current_hp(element["current_hp"])
                    self.set_current_gold(element["current_gold"])
                    self.update_turn_counter(element["turn_counter"][0],element["turn_counter"][1])
                    
                    if element["inventory"] is not None:
                        inv_list_of_obj = []
                        for inv_elem in element["inventory"]:
                            inv_obj = Object.Object(inv_elem["name"],inv_elem["state"],inv_elem["quantity"])
                            inv_list_of_obj.append(inv_obj)
                        self.update_inventory("add", inv_list_of_obj)
                        
                    if coords is None:
                        self.update_coords((element["co_ord_x"],element["co_ord_y"]))
                    else:
                        x,y = coords
                        self.update_coords((x,y))
                    break

    # GETTER METHODS
    
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

    def set_current_hp (self, new_current_hp,world_state=None):
        
        if not isinstance(new_current_hp, int):
            sys.stderr.write("Error: HP value is invalid\n")
            sys.exit(1)
        
        if new_current_hp > 0 and new_current_hp <= self.get_max_hp():
            self.__current_hp = new_current_hp
            
        elif new_current_hp > self.get_max_hp():
            self.__current_hp = self.get_max_hp()
            
        else:
            process_dead_char(self,world_state)        

        return world_state
    
    def set_max_hp (self, new_max_hp): 
        if not isinstance(new_max_hp, int):
            sys.stderr.write("Error: Max HP value is invalid\n")
            sys.exit(1)
        
        self.__max_hp = new_max_hp
    
    def set_current_gold (self, new_current_gold): 
        
        if not isinstance(new_current_gold, int):
            sys.stderr.write("Error: Gold value is invalid\n")
            sys.exit(1)
            
        self.__current_gold = new_current_gold

    def set_visited (self, new_visited): 
        
        if not isinstance(new_visited, set):
            sys.stderr.write("Error: Visited value is invalid\n")
            sys.exit(1)
            
        self.__visited = new_visited

    def update_visited(self, type, name, state):
        if not isinstance(type, str) and not isinstance(name, str) and not isinstance(state, str):
            sys.stderr.write("Error: Visited value is invalid\n")
            sys.exit(1)
    
        self.__visited.add( (type, name, state) )

    def increment_current_gold(self, increment_gold_amount):
        # increment amount can be positive or negative
        
        if not isinstance(increment_gold_amount, int):
            sys.stderr.write("Error: Gold value is invalid\n")
            sys.exit(1)
        
        self.__current_gold += increment_gold_amount
    
    def set_type(self, new_type):
    
        if new_type is not None and not isinstance(new_type,Enum.character_type):
            sys.stderr.write("Error: Character type value is invalid\n")
            sys.exit(1)
    
        self._type = new_type


    def set_active_player (self, is_active): 
        
        if not isinstance(is_active, bool):
            sys.stderr.write("Error: Active player value is invalid\n")
            sys.exit(1)
        
        self.__active_player =  is_active
       
    def turn_count_reached(self):
        # sets new state based on turn state, then resets the turn counter
        
        self.set_state(self.get_turn_state())
        self.update_turn_counter (0, "")


def process_dead_char(charac,world_state):
    
    if charac.get_type() == Enum.character_type.player:
        charac.set_current_hp(charac.get_max_hp())
        charac.set_current_gold(0)
        
        for row in world_state.get_tiles():
            for tile in row:
                if tile.get_name().lower() == "bedroom":
                    if tile.get_state() != "open":
                        tile.update_tile_by_state("open")
                    x,y = tile.get_coords()
                    charac.update_coords((x,y))
                    break
                
        if charac.get_active_player():
            print(text_formatting.justify("You wake up in your bedroom, someone managed to rescue you from the farmlands after they saw you heavily injured outside. You lost all your gold on hand."))
    
    else:
        world_state.remove_character(charac)
    
    return world_state
