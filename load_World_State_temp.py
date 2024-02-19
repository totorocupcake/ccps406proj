import Object
import Tile
import Character
import World_State
import text_file_processor

import load_Tiles_temp as load_Tiles
import load_Chars_and_Objs_temp as load_Chars_and_Objs


def load_World_State(rent_amount, rent_due_date):
  # Create and return a fully loaded World_State object:

  ws = World_State.World_State()

  tile_2D_list = load_Tiles.load_tile_2D_array_from_file()

  # load the 2D Tiles array:
  ws.load_2D_Tiles_array(tile_2D_list)

  # load the Characters list:
  char_list = load_Chars_and_Objs.load_characters_list_from_file()

  # for each character, add it to World_State characters list:
  if char_list is not None:
    for char_elem in char_list:
      ws.spawn_character(char_elem)


  # set all other attributes:
  
  # set turn to 1 to start (initialized to 0 in World_State constructor)
  ws.increment_turn(1)
  ws.set_game_won("N")
  ws.update_rent_amount(rent_amount)
  ws.update_rent_turn_due(rent_due_date)

  return ws
  














if __name__ == "__main__":
  
  
# ------------------------ Test load_World_State() function: 



# ----------------------------------------------------------
# can use this code to assemble the descriptions 
# (moved into World_State class get_description_as_str() method already )

  ws = load_World_State(10, 25)

  x_coord = 8
  y_coord = 7


  # call World_State.get_description_as_str() to return a formatted desc string

  # desc_str = ws.get_description_as_str((x_coord, y_coord), "long" )
  # print("desc((", x_coord, ",", y_coord, ")): ")
  # print(desc_str)
  # print()



  # # call World_State.get_description() to get a list/array of strings:
  # desc_list = ws.get_description((x_coord, y_coord), "short" )


  # desc_detail = ""
  # desc_count = 0

  # for desc_elem in desc_list:
  #   # print("desc((", x_coord, ",", y_coord, ")) = ", desc_elem)
  #   if desc_count == 0:  
  #     desc_detail = desc_detail + desc_elem 
  #   elif desc_count == 1:
  #     desc_detail =  desc_detail + "  You see " + desc_elem
  #   elif (desc_count > 1) and (desc_count < (len(desc_list)-1)):
  #     desc_detail = desc_detail + ", " + desc_elem
  #   else:
  #     desc_detail = desc_detail + ", and " + desc_elem + "."
  #   desc_count += 1

  # print()

  # print("desc((", x_coord, ",", y_coord, ")) = ", desc_detail)

  # print()


