import Character
import Tile
import Object
import text_file_processor


# constants: (make sure they match values in load_status_data.py)

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS


class World_State:

  # constructor:

  def __init__(self):

    # Private properties (with default starting values)
    self.__turn_number = 0  
    self.__game_won = "N"
    self.__rent_amount = 0
    self.__rent_due_date = 0
    self.__characters = []  # array/list of character objects

    # self.__tiles = (create and populate a 2D array/list of tile objects)
    # for testing, populate with None:
    self.__tiles = [[None] * WORLD_MAP_NUM_COLUMNS for _ in range(WORLD_MAP_NUM_ROWS)]


  # methods:

  def increment_turn(self, amount=1):
    self.__turn_number += amount    


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
    self.__tiles[y_coord][x_coord].update_tile(new_tile)






  def load_2D_Tiles_array(self, Tile_2D_array):
    self.__tiles = Tile_2D_array

    








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












  def get_description(self, coords):
    pass

  # # we need the long_short parameter to know which description to get:
  # def get_description(self, coords, long_short):
  #   x_coord, y_coord = coords

  #   current_tl = self.__tiles[x_coord][y_coord]

  #   current_char_list = self.get_chars_at_tile(coords)

  #   desc_list = []

  #   if current_tl is not None:
  #     tile_desc = current_tl.get_desc(long_short)

  #     desc_list.append(tile_desc)

  #     if len(current_char_list) > 0:
  #       for char_elem in current_char_list:
  #         if char_elem.get_desc(long_short) is not None:
  #           desc_list.append(char_elem.get_desc(long_short) )

  #   tile_inv = current_tl.get_inventory()
  #   if len(tile_inv) > 0:
  #     for inv_elem in tile_inv:
  #       if inv_elem.get_desc(long_short) is not None:
  #         desc_list.append(inv_elem.get_desc(long_short))

  #   return desc_list



  # def get_description_as_str(self, coords, long_short):
  #   x_coord, y_coord = coords
    
  #   desc_list = self.get_description((x_coord, y_coord), long_short)


  #   desc_detail = ""
  #   desc_count = 0

  #   for desc_elem in desc_list:
  #     # print("desc((", x_coord, ",", y_coord, ")) = ", desc_elem)
  #     if desc_count == 0:  
  #       desc_detail = desc_detail + desc_elem 
  #     elif desc_count == 1:
  #       desc_detail =  desc_detail + "  You see " + desc_elem
  #     elif (desc_count > 1) and (desc_count < (len(desc_list)-1)):
  #       desc_detail = desc_detail + ", " + desc_elem
  #     else:
  #       desc_detail = desc_detail + ", and " + desc_elem 
  #     desc_count += 1

  #   desc_detail = desc_detail + "."

  #   return desc_detail







  def get_game_won(self):
    return self.__game_won

  def get_turn_no(self):
    return self.__turn_number
  
  def get_rent_amount(self):
    return self.__rent_amount
  
  def get_rent_due_date(self):
    return self.__rent_due_date
  
  def get_characters(self):
    return self.__characters
  
  def get_tiles(self):
    return self.__tiles
















if __name__ == "__main__":

  # ------------------------------------------------ test some methods:
  ws = World_State()

  ws.increment_turn()

  ws.set_game_won("Y")  

  ws.update_rent_turn_due(25)

  ws.update_rent_amount(10)

  

  # desc = ws.get_description((1, 4), "short")
  desc = ws.get_description_as_str((1, 4), "short")
  

  print()
  if desc is not None:
    print("desc = ", desc)
  else:
    print("desc = None")
  print()




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


