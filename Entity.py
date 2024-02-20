import text_file_processor

class Entity:
  # class constructor:
  def __init__(self):

    # properties:
    self.name = ""
    self._general_type = ""
    self.__type = ""
    self.__state = ""
    self.__co_ord_x = 0
    self.__co_ord_y = 0
    # # self.__inventory = []
    self.inventory = []
     


  # getter methods (Common):
  # --------------
  def get_name(self):
    return self.name

  def get_general_type(self):
    return self._general_type

  def get_type(self):
    return self.__type

  def get_state(self):
    return self.__state

  def get_coords(self):
    return (self.__co_ord_x, self.__co_ord_y)

  def get_inventory(self):
    # returns a list of 'object' objects
    return self.inventory

  def get_desc(self, long_short):
    # use __general_type (Object/Character/Tile) for lookup:
    return text_file_processor.lookup_desc(long_short, self._general_type, self.name, self.__state)



  # setter methods (Common):
  # --------------

  def update_coords(self, new_coords):
    x_coord, y_coord = new_coords
    self.__co_ord_x = x_coord
    self.__co_ord_y = y_coord

  def set_name(self, new_name):
    self.name = new_name  

  def set_general_type(self, new_general_type):
    self._general_type = new_general_type

  def set_type(self, new_type):
    self.__type = new_type

  def set_state(self, new_state):
    self.__state = new_state

  def update_inventory(self, add_remove, objects):
    # adds/removes 'objects' from the __inventory list, given a list
    #   of 'object' objects
    # add_remove should = "add" for add case

    if add_remove == "add":

      # check to make sure the inputted 'objects' argument is not empty
      if objects is not None:

        # for each inputted object, append to the inventory list
        for obj_elem in objects:
          self.inventory.append(obj_elem)
          # inventory.append(obj_elem)
          # self.inventory.append(obj_elem)
    else:

      # check to make sure the inputted 'objects' argument is not empty
      if objects is not None:

        # for each inputted object, remove from the inventory list, if it exists
        for obj_elem in objects:

          # check to make sure object is in inventory before calling .remove()
          if obj_elem in self.inventory:
            self.inventory.remove(obj_elem)













if __name__ == "__main__":

  


  pass

