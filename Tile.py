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
    # self.name = ""
    # self.__type = ""
    # self.__state = ""
    # self.__long_desc = ""
    # self.__short_desc = ""
    # self.__co_ord_x = 0
    # self.__co_ord_y = 0

    # NOTE: must declare the inventory property again, else get weird error
    self.inventory = []

    # Tile-specific properties:
    self.__movable = "N"
    self.__turn_counter = 0

    # for tile_id: use string instead of int (can still code it in hex though)
    self.__tile_id = "00"
    

  # getter methods (Common):
  # --------------
  # def get_name(self):
  #   return self.name

  # def get_type(self):
  #   return self.__type

  # def get_state(self):
  #   return self.__state

  # def get_coords(self):
  #   return (self.__co_ord_x, self.__co_ord_y)

  # def get_inventory(self):
  #   # returns a list of 'object' objects
  #   return self.inventory

  # def get_desc(self, long_short):
  #   if long_short == "long":
  #     return self.__long_desc
  #   else:
  #     return self.__short_desc



    # *********
    # Need to add all other getter methods of the 'Tile' class:
    # *********




  # setter methods (Common):
  # --------------
  # def set_name(self, new_name):
  #   self.name = new_name  

  # def set_type(self, new_type):
  #   self.__type = new_type

  # def set_state(self, new_state):
  #   self.__state = new_state
      
  # def set_desc(self, long_short, new_desc):
  #   if long_short == "long":
  #     self.__long_desc = new_desc
  #   else:
  #     self.__short_desc = new_desc

  # def update_coords(self, new_coords):
  #   x_coord, y_coord = new_coords
  #   self.__co_ord_x = x_coord
  #   self.__co_ord_y = y_coord


  # def update_inventory(self, add_remove, objects):
  #   super().update_inventory(add_remove, objects)
    # adds/removes 'objects' from the __inventory list, given a list
    #   of 'object' objects
    # add_remove should = "add" for add case

    # if add_remove == "add":

    #   # check to make sure the inputted 'objects' argument is not empty
    #   if objects is not None:

    #     # for each inputted object, append to the inventory list
    #     for obj_elem in objects:
    #       self.inventory.append(obj_elem)
    # else:

    #   # check to make sure the inputted 'objects' argument is not empty
    #   if objects is not None:

    #     # for each inputted object, remove from the inventory list, if it exists
    #     for obj_elem in objects:

    #       # check to make sure object is in inventory before calling .remove()
    #       if obj_elem in self.inventory:
    #         self.inventory.remove(obj_elem)





    # *********
    # Need to add all other setter methods of the 'Tile' class:
    # *********

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

  # print()
  # print("Object info:")
  # print("name = ", obj1.get_name())
  # print("type = ", obj1.get_type())
  # print("state = ", obj1.get_state())

  obj2 = Object.Object()
  obj2.set_name("Gift")
  obj2.set_type("item")
  obj2.set_state("null")

  list_of_obj.append(obj1)
  list_of_obj.append(obj2)

  tl.update_inventory("add", list_of_obj)
  
  new_list = tl.get_inventory()

  print("len(new_list) = ", len(new_list))

  print()
  print("inventory:")
  # if new_list is not None:
  if len(new_list) > 0:
    for obj_elem in new_list:
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