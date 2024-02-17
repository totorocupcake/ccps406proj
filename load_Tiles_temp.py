# import Interface
import Object
import Tile
import text_file_processor


def lookup_tile_by_ID(tile_id):


  
  pass




if __name__ == "__main__":

  # ------------------- Tile object test:

  tl = Tile.Tile()
  tl.set_name("Home")
  tl.set_type("Tile")
  tl.set_state("null")
  tl.set_movable("Y")
  
  # for tile_id: use string instead of int (can still code it in hex though)
  tl.set_tile_id("11")

  tl.update_coords((1, 1))

  print()
  print("Tile info:")
  print("name = ", tl.get_name())
  print("type = ", tl.get_type())
  print("state = ", tl.get_state())
  print("coords = ", tl.get_coords())
  print()




  # ------------------- create/load 2D tile matrix:
  tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  print()
  print("tileIDMapping_data[0]: ")
  print(tileIDMapping_data[0])

  print()  

  tile_matrix_csv = text_file_processor.load_world_map_status_csv()

  print("tile_matrix_csv[0][0] = ", tile_matrix_csv[0][0])
  print()
  
  # create the empty tile matrix:
  rows = text_file_processor.WORLD_MAP_STATUS_ROWS
  cols = text_file_processor.WORLD_MAP_STATUS_COLUMNS
  matrix = []

  row_num = 0
  col_num = 0

  for i in range(rows):
      col_num = 0
      row = []
      for j in range(cols):
        row.append(tile_matrix_csv[row_num][col_num])
        col_num = col_num + 1        

      matrix.append(row)
      # print("matrix = ", matrix[row_num])
      row_num = row_num + 1


