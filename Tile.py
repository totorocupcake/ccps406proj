# import Entity
import Turn_Based_Entity

import Character
import Object as Object
import text_file_processor

# Implement the interface in a class
class Tile(Turn_Based_Entity.Turn_Based_Entity):
  
  # class constructor:
  def __init__(self):
    # # properties from Entity:
     # NOTE: must declare the inventory property again, else get weird error
    self.inventory = []

    # Tile-specific properties:
    self.__movable = "N"

    # for tile_id: use string instead of int (can still code it in hex though)
    self.__tile_id = "00"
    

  # getter methods (tile specific):
  # --------------
  
  def get_tile_id(self):
    return self.__tile_id

  def get_movable(self):
    return self.__movable


  # setter methods (tile specific):
  # --------------

  def set_tile_id(self, new_id):
    self.__tile_id = new_id

  def set_movable(self, flag):
    self.__movable = flag

  def update_tile(new_tile_id):
    self.__tile_id = new_tile_id



    # *********
    # Need to add all other miscellaneous methods of the 'Tile' class:
    # *********



























if __name__ == "__main__":

  # some test cases:
  # ---------------
  tl = Tile()
  
  tl.set_name("town square")
  tl.set_general_type("Tile")
  tl.set_type("non-building")
  tl.set_state("null")
  tl.set_movable("Y")

  print()
  print("name = ", tl.get_name())
  print("state = ", tl.get_state())
  print("get_desc('short') = ", tl.get_desc("short") )
  print("get_desc('long') = ", tl.get_desc("long") )
  print()


  tl.set_name("road")
  tl.set_general_type("Tile")
  tl.set_type("non-building")
  tl.set_state("null")


  print()
  print("name = ", tl.get_name())
  print("state = ", tl.get_state())
  print("get_desc('short') = ", tl.get_desc("short") )
  print("get_desc('long') = ", tl.get_desc("long") )
  print()


  # for tile_id: use string instead of int (can still code it in hex though)
  tl.set_tile_id("11")

  tl.update_coords((1, 1))

  print()
  print("Tile info:")
  print("name = ", tl.get_name())
  print("type = ", tl.get_type())
  print("state = ", tl.get_state())
  print("coords = ", tl.get_coords())


  
  # create two 'object' objects and add to Tile inventory

  list_of_obj = []

  obj1 = Object.Object()
  obj1.set_name("Easter egg")
  obj1.set_type("item")
  obj1.set_state("null")

  obj2 = Object.Object()
  obj2.set_name("Gift")
  obj2.set_type("item")
  obj2.set_state("null")

  list_of_obj.append(obj1)
  list_of_obj.append(obj2)

  tl.update_inventory("add", list_of_obj)
  
  inventory_list = tl.get_inventory()

  print()
  print("len(inventory_list) = ", len(inventory_list))

  print()
  print("inventory:")
  # if inventory_list is not None:
  if len(inventory_list) > 0:
    for obj_elem in inventory_list:
      print("name = ", obj_elem.get_name())
      print("type = ", obj_elem.get_type())
      print("state = ", obj_elem.get_state())
      print()
  else:
    print("List is empty")
      

  tileIDMapping_data = text_file_processor.load_tileIDMapping_file()

  print()
  print("tileIDMapping_data[0]: ")
  print(tileIDMapping_data[0])

  print()  