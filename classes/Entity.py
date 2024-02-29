import text_file_processor

class Entity:
  # class constructor:
  def __init__(self):

    # properties:
    self._name = ""
    self._general_type = ""
    self._type = ""
    self.__state = ""
    self._co_ord_x = 0
    self._co_ord_y = 0
    # # self.__inventory = []
    self._inventory = []
     


  # getter methods (Common):
  # --------------
  def get_name(self):
    return self._name

  def get_general_type(self):
    return self._general_type

  def get_type(self):
    return self._type

  def get_state(self):
    return self.__state

  def get_coords(self):
    return (self._co_ord_x, self._co_ord_y)

  def get_inventory(self):
    # returns a list of 'object' objects
    return self._inventory

  def get_desc(self, long_short,world_state):
    # use __general_type (Object/Character/Tile) for lookup:
    
    return text_file_processor.lookup_desc(long_short, self._general_type, self._name, self.__state,world_state)



  # setter methods (Common):
  # --------------

  def update_coords(self, new_coords):
    x_coord, y_coord = new_coords
    self._co_ord_x = x_coord
    self._co_ord_y = y_coord

  def set_name(self, new_name):
    self._name = new_name  

  def set_general_type(self, new_general_type):
    self._general_type = new_general_type

  def set_type(self, new_type):
    self._type = new_type

  def set_state(self, new_state):
    self.__state = new_state

  def update_inventory(self, add_remove, list_of_objects):
    # adds/removes 'objects' from the __inventory list, given a list
    #   of 'object' objects
    # add_remove should = "add" for add case

    if add_remove == "add":

      # check to make sure the inputted 'objects' argument is not empty
      if list_of_objects is not None:

        # for each inputted object, append to the inventory list
        for obj_elem in list_of_objects:
          self._inventory.append(obj_elem)
          # inventory.append(obj_elem)
          # self.inventory.append(obj_elem)
    else:

      # check to make sure the inputted 'objects' argument is not empty
      if list_of_objects is not None:

        # for each inputted object, remove from the inventory list, if it exists
        for obj_elem in list_of_objects:

          # check to make sure object is in inventory before calling .remove()
          if obj_elem in self._inventory:
            self._inventory.remove(obj_elem)













if __name__ == "__main__":

  


  pass

