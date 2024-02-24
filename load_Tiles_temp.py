import Object
import Tile
import text_file_processor

import load_Chars_and_Objs_temp as load_Chars_and_Objs

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS



def get_object_list_by_tile_location(x_coord, y_coord,load_game):

  obj_list = load_Chars_and_Objs.load_objects_list_from_file(load_game)

  found = False

  found_obj_list = []

  for obj_elem in obj_list:
    obj_x, obj_y = obj_elem.get_coords()
    if (obj_x == x_coord) and (obj_y == y_coord):
      found = True
      found_obj_list.append(obj_elem)

  if found:
    return found_obj_list
  else:
    return None

  


def get_tile_by_name_and_state(name, state):
  # creates and returns a tile object from load_tile_JSON_data_file()
  #   based on a give tile 'name' and 'state'

  tile_data_list = text_file_processor.load_tile_JSON_data_file()
  
  found = False

  for tile_elem in tile_data_list:

    # if matching tile_id is found
    if (tile_elem["name"] == name) and (tile_elem["state"] == state):
      found = True
      # create and populate a tile object with the appropriate data
      tl = Tile.Tile()
      tl.set_general_type("Tile")
      tl.set_type( tile_elem["type"] )
      tl.set_name(tile_elem["name"])
      tl.set_state(tile_elem["state"])
      tl.set_movable(tile_elem["movable"])

  if found:
    return tl
  else:
    return None
  



















def lookup_tile_Mapping_by_ID(tile_id):
  # returns a tile object from load_tile_JSON_data_file()
  #   based on a give tile_id

  # get the tile mapping data from the file:
  tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  # iterate through tileIDMapping_data list: 
  for tile_elem in tileIDMapping_data:

    # if matching tile_id is found
    if tile_elem["tile_id"] == tile_id:

      # get the corresponding tile object with the appropriate data
      tl = get_tile_by_name_and_state(tile_elem["name"], tile_elem["state"])

      # populate with other data:
      if tl is not None:
        tl.set_tile_id(tile_id)
        tl.set_state(tile_elem["state"])


      return tl

  # if no tile found, return None
  return None
















def load_tile_2D_array_from_file(load_game):
  # returns a 2D array/list of tile objects

  # get 2D array of tile ID's from world_map_status_00.csv
  world_map_status_array = text_file_processor.load_world_map_status_csv(load_game)

  # get the JSON array of tile_id_mappings 
  # tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  # get the JSON array of tiles
  # tile_data = text_file_processor.load_tile_JSON_data_file()

  num_rows = WORLD_MAP_NUM_ROWS
  num_cols = WORLD_MAP_NUM_COLUMNS

  tile_2D_list = []

  for i in range(num_cols):
    inner_array = []
    for j in range(num_rows):
      tile_id = world_map_status_array[j][i]
      tl = lookup_tile_Mapping_by_ID(tile_id)

      # update_coords of tile:
      tl.update_coords((i, j))

      # update Tile inventory:
      obj_list = get_object_list_by_tile_location(i, j,load_game)

      # add objects to tile inventory if found:
      if obj_list is not None:
        tl.update_inventory("add", obj_list)

      inner_array.append(tl)

    tile_2D_list.append(inner_array)

  return tile_2D_list


















if __name__ == "__main__":
  
# ------------------------ Test: load_tile_2D_array_from_file() function

  tile_2D_list = load_tile_2D_array_from_file()
  print()

  # print out some sample data:
  print("Some sample tiles (with inventory if any): ")
  print("-----------------------------------------")
  print()

  print("tile_2D_list[8][7] = ", tile_2D_list[8][7].get_name(), ",", \
        tile_2D_list[8][7].get_type(), ",", tile_2D_list[8][7].get_state(), ",", \
          tile_2D_list[8][7].get_movable(), ", ", tile_2D_list[8][7].get_tile_id()  )

  inv_list = tile_2D_list[8][7].get_inventory()

  if inv_list is not None:
    for inv_elem in inv_list:
      print("\tItem: ", inv_elem.get_name())
  
 # Test update tile by id function, should update rest of tile's fields if provide it a new tile id
  tile_2D_list[8][7].update_tile_by_id("0C")
  print("tile_2D_list[8][7] = ", tile_2D_list[8][7].get_name(), ",", \
        tile_2D_list[8][7].get_type(), ",", tile_2D_list[8][7].get_state(), ",", \
          tile_2D_list[8][7].get_movable(), ", ", tile_2D_list[8][7].get_tile_id()  )

  inv_list = tile_2D_list[8][7].get_inventory()

  if inv_list is not None:
    for inv_elem in inv_list:
      print("\tItem: ", inv_elem.get_name())
  else:
    print("Inventory is None")
  
  print()
  print()

  print("More sample tiles (with inventory if any): ")
  print("-----------------------------------------")
  print()

  tile_2D_list = load_tile_2D_array_from_file()

  row_num = 0
  col_num = 0

  for row in tile_2D_list:
    col_num = 0
    for element in row:
      # grasslands
      if tile_2D_list[row_num][col_num] is not None:
        if tile_2D_list[row_num][col_num].get_name() != "grasslands":
          print("tile_2D_list[", row_num, "][", col_num, "] = ", \
                tile_2D_list[row_num][col_num].get_name(), ",", \
                tile_2D_list[row_num][col_num].get_tile_id(), ",", \
                tile_2D_list[row_num][col_num].get_state(), ",", \
                tile_2D_list[row_num][col_num].get_movable()    )

          tl_inv_list = tile_2D_list[row_num][col_num].get_inventory()
          # if tl_inv_list is not None:
          if len(tl_inv_list) > 0:
            for inv_elem in tl_inv_list:
              print("\titem = ", inv_elem.get_name())

      else:
        print("tile_2D_list[", row_num, "][", col_num, "] is None   ***********")
      col_num += 1
    row_num += 1

print()
print()




# animal_tl = lookup_tile_Mapping_by_ID("25")
# if animal_tl is not None:
#   print("animal_tl name = ", animal_tl.getName())
# else:
#   print("animal_tl is None")

# print()






# # Iterate over each row of the array
# for row in two_dim_array:
#     # Iterate over each element in the row
#     for element in row:
#         # Print the element followed by a tab (or any other separator)
#         print(element, end="\t")
#     # Print a newline to move to the next row
#     print()




# ------------------------ Test: get_object_by_tile_location() function


  # obj_list = get_object_list_by_tile_location(4, 12)

  # print()
  # print("obj_list[0] at (8, 7) = ", obj_list[0].get_name())

  # obj_list = get_object_list_by_tile_location(0, 0)

  # print()
  # if obj_list is not None:
  #   print("obj at (0, 0) = ", obj_list[0].get_name())
  # else:
  #   print("obj at (0, 0) = None")
  # print()
      #  "co_ord_x": 8,
      #   "co_ord_y": 7,


# get_object_by_tile_location


# ------------------------ Test: lookup_tile_Mapping_by_ID() function


  # tile_mapping = lookup_tile_Mapping_by_ID("01")
  # print()
  # print("tile id = '01' = ", tile_mapping.get_name(), ",", \
  #       tile_mapping.get_state(), ",", tile_mapping.get_movable())
  # print()

  # my_tile = get_tile_by_name_and_state("town square", "null")
  # # get_tile_by_name_and_state
  # print()
  # print("my_tile = ", my_tile.get_name(), ",", my_tile.get_state())
  # print()
















# ------------------------ Test: Tile methods:


  # ------------------- Tile object test:

  # tl = Tile.Tile()
  # tl.set_name("Home")
  # tl.set_type("Tile")
  # tl.set_state("null")
  # tl.set_movable("Y")
  
  # # for tile_id: use string instead of int (can still code it in hex though)
  # tl.set_tile_id("11")

  # tl.update_coords((1, 1))

  # print()
  # print("Tile info:")
  # print("name = ", tl.get_name())
  # print("type = ", tl.get_type())
  # print("state = ", tl.get_state())
  # print("coords = ", tl.get_coords())
  # print()




  # # ------------------- create/load 2D tile matrix:
  # tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  # print()
  # print("tileIDMapping_data[0]: ")
  # print(tileIDMapping_data[0])

  # print()  

  # tile_matrix_csv = text_file_processor.load_world_map_status_csv()

  # print("tile_matrix_csv[0][0] = ", tile_matrix_csv[0][0])
  # print()
  
  # # create the empty tile matrix:
  # rows = text_file_processor.WORLD_MAP_STATUS_ROWS
  # cols = text_file_processor.WORLD_MAP_STATUS_COLUMNS
  # matrix = []

  # row_num = 0
  # col_num = 0

  # for i in range(rows):
  #     col_num = 0
  #     row = []
  #     for j in range(cols):
  #       row.append(tile_matrix_csv[row_num][col_num])
  #       col_num = col_num + 1        

  #     matrix.append(row)
  #     # print("matrix = ", matrix[row_num])
  #     row_num = row_num + 1


