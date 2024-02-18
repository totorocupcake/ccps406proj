import Object
import Tile
import text_file_processor

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS







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
















def load_tile_2D_array_from_file():
  # returns a 2D array/list of tile objects

  # get 2D array of tile ID's from world_map_status_00.csv
  world_map_status_array = text_file_processor.load_world_map_status_csv()

  # get the JSON array of tile_id_mappings 
  tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  # get the JSON array of tiles
  tile_data = text_file_processor.load_tile_JSON_data_file()

  num_rows = WORLD_MAP_NUM_ROWS
  num_cols = WORLD_MAP_NUM_COLUMNS

  tile_2D_list = []

  for i in range(num_rows):
    inner_array = []
    for j in range(num_cols):
      tile_id = world_map_status_array[i][j]
      tl = lookup_tile_Mapping_by_ID(tile_id)
      
      inner_array.append(tl)

    tile_2D_list.append(inner_array)

  return tile_2D_list


















# if __name__ == "__main__":

if __name__ == "__main__":
  
# ------------------------ Test: load_tile_2D_array_from_file() function

  tile_2D_list = load_tile_2D_array_from_file()
  print()

  # print out some sample data:
  print("Some sample tiles: ")
  print()

  print("tile_2D_list[0][0] = ", tile_2D_list[0][0].get_name(), ",", \
        tile_2D_list[0][0].get_type(), ",", tile_2D_list[0][0].get_state(), ",", \
          tile_2D_list[0][0].get_movable() )
  print()

  print("tile_2D_list[3][6] = ", tile_2D_list[3][6].get_name(), ",", \
        tile_2D_list[3][6].get_type(), ",", tile_2D_list[3][6].get_state(), ",", \
          tile_2D_list[3][6].get_movable() )
  print()

  print("tile_2D_list[3][11] = ", tile_2D_list[3][11].get_name(), ",", \
        tile_2D_list[3][11].get_type(), ",", tile_2D_list[3][11].get_state(), ",", \
          tile_2D_list[3][11].get_movable() )
  print()


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

