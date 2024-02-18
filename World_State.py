import Character
import text_file_processor


# constants: (make sure they match values in load_status_data.py)

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS


class World_State:

  # constructor:

  def __init__(self):

    # Private properties (with default starting values)
    self.__turn_number = 1  
    self.__game_won = "N"
    self.__rent_amount = 20
    self.__rent_due_date = 25
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
    self.__characters.append(new_character)

    # debug:
    print("DEBUG: spawn_char() len(characters) = ", len(self.__characters))


  def remove_character(self, character):
    # check to make sure inputted character is in the __characters list
    if character in self.__characters:
      self.__characters.remove(character)
      # debug:
      print("DEBUG: rem_char() len(characters) = ", len(self.__characters))



  def update_tile(self, coords, new_tile):
    pass


  def get_desc(self, coords):
    x_coord, y_coord = coords

    # or should it be self.__tiles[y_coord][x_coord] ????
    return self.__tiles[x_coord][y_coord]


      












if __name__ == "__main__":

  # test some methods:
  ws = World_State()

  ws.increment_turn()

  ws.set_game_won("Y")  

  ws.update_rent_turn_due(10)

  desc = ws.get_desc((0, 0))

  print()
  if desc is not None:
    print("desc = ", desc)
  else:
    print("desc = None")
  print()

  #----------------------------
  charac1 = charClass.Character()

  charac1.set_name("first character")

  print("charac name = ", charac1.get_name())
  print()

  # test spawn_character() method
  ws.spawn_character(charac1)
  
  charac2 = charClass.Character()

  charac2.set_name("second character")

  print("charac name = ", charac2.get_name())
  print()

  # test spawn_character() method
  ws.spawn_character(charac2)
  
  # test remove_character() method
  ws.remove_character(charac1)


