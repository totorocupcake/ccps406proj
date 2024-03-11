# import Entity
import classes.Turn_Based_Entity as Turn_Based_Entity
import classes.Data as Data
import classes.Character as Character
import classes.Object as Object

# Implement the interface in a class
class Tile(Turn_Based_Entity.Turn_Based_Entity):
  
  # class constructor:
  def __init__(self):
    super().__init__()
    # # properties from Entity:
     # NOTE: must declare the inventory property again, else get weird error
    self._inventory = []

    # Tile-specific properties:
    self.__movable = "N"
    self.__block = "N"
    
    # for tile_id: use string instead of int (can still code it in hex though)
    self.__tile_id = "00"
    self._general_type = "Tile"
    self._turn_counter = 0
    self._turn_state = ""
    self.__current_gold = 0 # added for mechanic to store gold in home
    

  # getter methods (tile specific):
  # --------------
  
  def get_tile_id(self):
    return self.__tile_id

  def get_movable(self):
    return self.__movable

  def get_block(self):
    return self.__block
  
  def get_current_gold (self): 
        return self.__current_gold

  # setter methods (tile specific):
  # --------------

  def set_tile_id(self, new_id):
    self.__tile_id = new_id

  def set_movable(self, flag):
    self.__movable = flag
    
  def set_block(self, flag):
    self.__block = flag

  def update_tile_by_id(self, new_tile_id):
    # update tile_id to new tile_id. 
    # other tile's fields (name, type, state, movable) will be synced to new tile_id provided 
    
    self.__tile_id = new_tile_id
    
    # update rest of tile fields to account for new tile_id
    tileIDMapping_data = Data.Data().get_tile_id_mapping()

    for tile_elem in tileIDMapping_data:

    # if matching tile_id is found
      if tile_elem["tile_id"] == self.__tile_id :
        # set new state and name based on tile id mapping file
        self.set_state(tile_elem["state"])
        self.set_name(tile_elem["name"])
  
        # update other fields based on text parser lookup functions (from tile in-game text files)
        self.set_movable(Data.Data().lookup_movable(self.get_name(),self.get_state()))
        self.set_block(Data.Data().lookup_block(self.get_name(),self.get_state()))
        self.set_type(Data.Data().lookup_tile_type(self.get_name(),self.get_state()))

    
  def update_tile_by_state(self, new_state):
    # update tile to new state and also update tile_id and movable fields to account for new state
    
    self.set_state(new_state)
    
    # update rest of tile fields to account for new tile_id
    tileIDMapping_data =  Data.Data().get_tile_id_mapping()
    tile_json = Data.Data().get_tile_data()

    for tile_elem in tileIDMapping_data:
      if tile_elem["name"] == self.get_name() and tile_elem["state"] == self.get_state():
        # set new tile_id based on tile id mapping file
        self.__tile_id = tile_elem["tile_id"]
        
    for tile_elem in tile_json:
    # if match tile name and state within tile id mapping file
      if tile_elem["name"] == self.get_name() and tile_elem["state"] == self.get_state():
        self.set_type(tile_elem["type"])
        self.set_movable(tile_elem["movable"])
        self.set_block(tile_elem["block"])
      
  def turn_count_reached(self):
    # updates tile based on new state, then resets turn counter to no turn count
    self.update_tile_by_state(self.get_turn_state())
    self.update_turn_counter (0, "")

  def increment_current_gold(self, increment_gold_amount):
        # increment amount can be positive or negative
        self.__current_gold += increment_gold_amount
