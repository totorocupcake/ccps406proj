import Character
import Tile
import Object
import text_file_processor
import random
import npc_behaviors


# constants: (make sure they match values in load_status_data.py)

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS


class World_State:

  # constructor:

  def __init__(self):
    
    random.seed(42) # select seed for reproducible random results for testing
    
    # Private properties (with default starting values)
    self.__turn_number = 0  
    self.__game_won = 'N'
    self.__rent_amount = 0
    self.__rent_due_date = 0
    self.__characters = []  # array/list of character objects

    # self.__tiles = (create and populate a 2D array/list of tile objects)
    # for testing, populate with None:
    self.__tiles = [[None] * WORLD_MAP_NUM_COLUMNS for _ in range(WORLD_MAP_NUM_ROWS)]


  # methods:

  def increment_turn(self, amount=1):
    self.__turn_number += amount
    
    # turn counting checks for all chars
    for char in self.__characters:
        char.decrement_turn_count()
    
    # turn counting checks for all tiles    
    for row in self.__tiles:
      for tiles in row:
        tiles.decrement_turn_count()


  def set_game_won(self, flag):
    self.__game_won = flag


  def update_rent_turn_due(self, increment):
    self.__rent_due_date += increment

  
  def update_rent_amount(self, increment):
    self.__rent_amount += increment


  def spawn_character(self, new_character):
    if new_character not in self.__characters:
      self.__characters.append(new_character)


  def remove_character(self, character):
    # check to make sure inputted character is in the __characters list
    if character in self.__characters:
      self.__characters.remove(character)





  def update_tile(self, coords, new_tile):
    x_coord, y_coord = coords
    self.__tiles[x_coord][y_coord] = new_tile






  def load_2D_Tiles_array(self, Tile_2D_array):
    self.__tiles = Tile_2D_array

    
  def get_tile_at_coords(self, coords):
    x_coord, y_coord = coords
    return self.__tiles[x_coord][y_coord]












  def get_tile_by_name(self, tile_name):

    num_rows = WORLD_MAP_NUM_ROWS
    num_cols = WORLD_MAP_NUM_COLUMNS

    for i in range(num_cols):
      inner_array = []
      for j in range(num_rows):
        # if tile_name == self.__tiles[j][i].get_name():
        if tile_name == self.__tiles[i][j].get_name():
          return self.__tiles[i][j]
    
    return None















  def get_npc_chars_at_tile(self, coords):
  # return a list of npc characters for a given tile, based on its coords

    # get all characters as a list
    npc_char_list = self.get_chars_at_tile(coords)

    # remove the player character from the list
    if npc_char_list is not None:
      for npc_elem in npc_char_list:
        # remove the 'player' character from the list
        if npc_elem.get_type() == "player":
          npc_char_list.remove(npc_elem)
          break

    return npc_char_list
    




  def get_chars_at_tile(self, coords):
  # return the character list for a given tile, based on its coords

    x_coord, y_coord = coords

    char_list = self.__characters

    current_char_list = []

    if char_list is not None:
      for char_elem in char_list:
        x_char, y_char = char_elem.get_coords()
        if (x_char == x_coord) and (y_char == y_coord):
          current_char_list.append(char_elem)

    return current_char_list



  def get_active_char(self):
    # Returns the Character with active player flaf set to Y
    for char in self.__characters:
      if char.get_active_player() == 'Y':
        return char

    return None








  def get_description(self, coords, visited):
  # returns a list/array of description strings for a given coords and 
  #   visited set (of tuples of (type, name, state))
    x_coord, y_coord = coords

    # get the tile at coords
    current_tl = self.__tiles[x_coord][y_coord]

    # get the current tile's inventory:
    current_tl_inv_list = []
    current_tl_inv_list = current_tl.get_inventory()

    # get a list of all npc's for the current coords
    current_npc_char_list = []
    current_npc_char_list = self.get_npc_chars_at_tile(coords)

    # intialize the description list of strings:
    desc_list = []

    # for each tile, character and object, check and see if in visited set
    #   if no, use "long" desc
    #   if yes, use "short" desc

    # start with Tile object:
    tile_tuple = (current_tl.get_general_type(), current_tl.get_name(), current_tl.get_state())

    if tile_tuple in visited:
      desc_list.append(current_tl.get_desc("short"))
    else:
      desc_list.append(current_tl.get_desc("long"))

    # add each character:
    if current_npc_char_list is not None:
      for char_elem in current_npc_char_list:
        char_tuple = (char_elem.get_general_type(), char_elem.get_name(), \
                      char_elem.get_state() )

        if char_tuple in visited:
          desc_list.append(char_elem.get_desc("short"))
        else:
          desc_list.append(char_elem.get_desc("long"))
        

    # add each object in the tile's inventory:
    if current_tl_inv_list is not None:
      for tl_inv_elem in current_tl_inv_list:
        inv_tuple = (tl_inv_elem.get_general_type(), tl_inv_elem.get_name(), \
                      tl_inv_elem.get_state() )
        if inv_tuple in visited:
          desc_list.append(tl_inv_elem.get_desc("short"))
        else:
          desc_list.append(tl_inv_elem.get_desc("long"))


    # ------------------------------------------------------
    # this code assembles the desc list into a single string
    #    called desc_detail and returns it:
    # ------------------------------------------------------
    desc_detail = ""
    desc_count = 0

    for desc_elem in desc_list:
      # print("desc((", x_coord, ",", y_coord, ")) = ", desc_elem)
      if desc_count == 0:  
        desc_detail = desc_detail + desc_elem 
      elif desc_count == 1:
        desc_detail =  desc_detail + "  You see " + desc_elem
      elif (desc_count > 1) and (desc_count < (len(desc_list)-1)):
        desc_detail = desc_detail + ", " + desc_elem
      else:
        desc_detail = desc_detail + " and " + desc_elem 
      desc_count += 1

    if desc_count > 1:
      desc_detail = desc_detail + "."


    return desc_detail

    # return desc_list








  def get_game_won(self):
    return self.__game_won

  def get_turn_number(self):
    return self.__turn_number
  
  def get_rent_amount(self):
    return self.__rent_amount
  
  def get_rent_due_date(self):
    return self.__rent_due_date
  
  def get_characters(self):
    return self.__characters
  
  def get_tiles(self):
    return self.__tiles

  def get_next_action (self, charac):
    # Function controls computer-controlled characters by providing their next command for console input
    
    # Aggressive thief behavior ########################################
    # steal gold from player if on same tile, otherwise roam the grass
    if charac.name == "Thief" and charac.get_state() =="aggressive":
      for element in self.get_characters():
        # find the player character (note may not be the active player)
            if element.get_type() == "player":
              player = element
              break

      if player.get_coords() == charac.get_coords():
        # steal gold from player if on same tile
        player_name = player.name
        next_command="steal "+ player_name
        return next_command
      else:
        # just move around if no player on same tile
        next_command = npc_behaviors.graze(self,charac)
        return next_command
    
    # Aggressive wolf behavior ################################################
    # kill chicken/cow if there is chicken/cow on same tile, otherwise it just moves randomly on grass
    elif charac.name == "Wolf" and charac.get_state() =="aggressive":
      char_list = self.get_chars_at_tile(charac.get_coords())
      
      for char in char_list:
        if char.name == "chicken":
          return "kill chicken"
        elif char.name == "cow":
          return "kill cow"
      
      next_command = npc_behaviors.graze(self,charac)
      return next_command
    
    # Wild chicken behavior ######################################################
    # fast mover, it moves once every turn, roams grass randomly
    elif charac.name == "chicken" and charac.get_state() =="wild":
      next_command = npc_behaviors.graze(self,charac)
      return next_command
      

    # Wild cow behavior ###########################################################
    # cow is slower moving compared to chicken, it only moves once every 2 turns, roams grass
    elif charac.name == "cow" and charac.get_state()=="wild":
      if (self.get_turn_number() % 2) == 0:
        next_command = npc_behaviors.graze(self,charac)
        return next_command
      else:
        pass
    
    # All other characters' behavior ######################################################
    else:
      # default do nothing if no behavior defined for character
      pass

    
    
        





















if __name__ == "__main__":

  # ------------------------------------------------ test some methods:
  ws = World_State()

  ws.increment_turn()

  ws.set_game_won('Y')  

  ws.update_rent_turn_due(25)

  ws.update_rent_amount(10)

  print("Turn no: ",ws.get_turn_no())
  print("Game Won: ",ws.get_game_won())
  print("Rent turn due: ",ws.get_rent_due_date())
  print("Rent amount: ", ws.get_rent_amount())
  
  tl = Tile.Tile()
  tl.update_tile_by_id("01")
  ws.update_tile((1,4),tl)
  print("Tile name: ",ws.get_tiles()[1][4].name)
  print("Tile state: ",ws.get_tiles()[1][4].get_state())
  print("Tile general type: ",ws.get_tiles()[1][4].get_general_type())
  
  charac= Character.Character()
  charac.set_name("landlord")
  charac.set_state("unhappy")
  charac.update_coords((1,4))
  ws.spawn_character(charac)




  # # ------------ test World_State.get_description(coords, visited) function:

  # ws = load_World_State(10, 25)

  # empty_visited = set()

  # x_coord = 8
  # y_coord = 7

  # coord_tuple = (x_coord, y_coord)

  # desc_list = ws.get_description(coord_tuple, empty_visited)

  # print()
  # print("desc_list[0] = ", desc_list[0])
  # print()

  
  # print("Get Desc long: ",ws.get_description((1,4),"long"))
  # print("Get Desc short: ",ws.get_description((1,4),"short"))
  
  # print("Get Desc as str long: ",ws.get_description_as_str((1,4),"long"))
  # print("Get Desc as str short: ",ws.get_description_as_str((1,4),"short"))
  
  
  #desc = ws.get_description((1, 4), "short")
  #desc = ws.get_description_as_str((1, 4), "short")
  

  #print()
  #if desc is not None:
  #  print("desc = ", desc)
  #else:
  #  print("desc = None")
  #print()




  #----------------------------
  charac1 = Character.Character()

  charac1.set_name("first character")

  print("charac name = ", charac1.get_name())
  print()

  # test spawn_character() method
  ws.spawn_character(charac1)
  
  charac2 = Character.Character()

  charac2.set_name("second character")

  print("charac name = ", charac2.get_name())
  print()

  # test spawn_character() method
  ws.spawn_character(charac2)
  
  # test remove_character() method
  ws.remove_character(charac1)


