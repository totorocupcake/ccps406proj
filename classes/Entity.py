import classes.external_files as external_files
import classes.enums as Enum
import sys

class Entity:
  def __init__(self):
    
    self._name = ""
    self._general_type = ""
    self._type = ""
    self.__state = ""
    self._co_ord_x = 0
    self._co_ord_y = 0
    self._inventory = []
     
  # getter methods (Common):

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

  def get_desc(self, long,world_state):
    return external_files.read_external_files().lookup_desc(long, self._general_type, self._name, self.__state,world_state)


  # setter methods (Common):

  def update_coords(self, new_coords):
    
    if not isinstance(new_coords,tuple):
      sys.stderr.write("Error: Coordinate value is invalid\n")
      sys.exit(1)
      
    x_coord, y_coord = new_coords
    
    if not isinstance(x_coord,int) and not isinstance(y_coord,int):
      sys.stderr.write("Error: Coordinate value is invalid\n")
      sys.exit(1)
    
    self._co_ord_x = x_coord
    self._co_ord_y = y_coord

  def set_name(self, new_name):
    
    if new_name is not None and not isinstance(new_name,str):
      sys.stderr.write(f"Error: Name value {new_name} is invalid\n")
      sys.exit(1)
      
    self._name = new_name  

  def set_general_type(self, new_general_type):
    
    if not isinstance(new_general_type,Enum.general_type):
      sys.stderr.write("Error: General type value is invalid\n")
      sys.exit(1)
    
    self._general_type = new_general_type

  def set_type(self, new_type):
    
    if new_type is not None and not isinstance(new_type,str):
      sys.stderr.write("Error: Type value is invalid\n")
      sys.exit(1)
  
    self._type = new_type

  def set_state(self, new_state):
    
    if new_state is not None and not isinstance(new_state,str):
      sys.stderr.write("Error: State value is invalid\n")
      sys.exit(1)
    
    self.__state = new_state

  def update_inventory(self, add_remove, list_of_objects):
    # adds/removes 'objects' from the __inventory list, given a list
    # of 'object' objects
    # add_remove should = "add" for add case

    if not isinstance(list_of_objects,list):
      sys.stderr.write("Error: Inventory value is invalid\n")
      sys.exit(1)
    
    if list_of_objects is not None:
      
      if add_remove == "add":
        # for each inputted object, append to the inventory list
        for obj_elem in list_of_objects:
          
          found = False
          for inv_elem in self.get_inventory():
            
            if inv_elem.get_name() == obj_elem.get_name() and inv_elem.get_state() == obj_elem.get_state():
              inv_elem.update_qty(obj_elem.get_quantity())
              found=True
              break
          if found == False:
            self._inventory.append(obj_elem)
            
      elif add_remove == "delete":
        # for each inputted object, remove from the inventory list, if it exists
        for obj_elem in list_of_objects:
          
          for inv_elem in self.get_inventory():
             if inv_elem.get_name() == obj_elem.get_name() and inv_elem.get_state() == obj_elem.get_state():
                if inv_elem.get_quantity()> obj_elem.get_quantity():
                  inv_elem.update_qty(obj_elem.get_quantity()*-1)
                elif inv_elem.get_quantity() == obj_elem.get_quantity():
                  self._inventory.remove(obj_elem)
                else:
                  print(f"Error, cannot remove item {obj_elem.get_name()}.")
      else: #decrement
         for obj_elem in list_of_objects:
          for inv_elem in self.get_inventory():
             if inv_elem.get_name() == obj_elem.get_name() and inv_elem.get_state() == obj_elem.get_state():
                if inv_elem.get_quantity()>1:
                  inv_elem.update_qty(-1)
                else:
                  self._inventory.remove(obj_elem)
        


