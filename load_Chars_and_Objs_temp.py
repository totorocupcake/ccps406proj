import text_file_processor
import Character
import Object


def load_objects_list_from_file():
  # returns a list of 'object' objects that have been populated with 
  # data from the objects status JSON file via text_file_processor.py


  # get JSON object status data from file via text_file_processor.py
  object_status_data = text_file_processor.load_object_status_file()
  
  # Create an empty list to store objects
  objects = []
  
  # iterate through object status JSON data and create/populate a 'Object' 
  #    object for each one, then append each to the list 'objects'
  
  for obj_elem in object_status_data:
    obj = Object.Object()

    # set all 'Object' object attributes
    obj.set_name(obj_elem["name"])

    # need a general_type for looking up descriptions in text_file_processor.py
    obj.set_general_type("Object")

    obj.set_type(obj_elem["type"])
    obj.set_state(obj_elem["state"])


    # *********
    #   All other attributes of the 'Object' class
    #   from object_status_data (JSON data):
    # *********

    obj.update_qty(obj_elem["quantity"])
    obj.update_coords((obj_elem["co_ord_x"], obj_elem["co_ord_y"]))
    
    # need to add gold_amt, look-up from 'objects_02n.json' via 'text_file_processor'
    obj.set_gold_amt = text_file_processor.lookup_gold_amt(obj.get_name(), obj.get_state())


    # for each item in 'inventory' create an 'Object' object, and add it to inventory:
    if obj_elem["inventory"] is not None:

      # update_inventory, if its not empty
      for inv_elem in obj_elem["inventory"]:

        inv_obj = Object.Object()
        inv_obj.set_name = inv_elem["name"]
        inv_obj.update_qty(inv_elem["quantity"])
        inv_obj.set_state(inv_elem["state"])

        obj.update_inventory("add", inv_obj)


    # append the 'Object' object to the 'objects' list of objects
    objects.append(obj)

  # return objects list
  return objects


















def load_characters_list_from_file():
  # returns a list of character objects that have been populated with 
  # data from the character status JSON file via text_file_processor.py


  # get JSON characters status data from file via text_file_processor.py
  character_status_data = text_file_processor.load_character_status_file()

  # Create an empty list to store characters
  characters = []
  
  # iterate through chacter status JSON data and create/populate a Character 
  #    object for each one, then append each to the list 'characters'
  for char_elem in character_status_data:
    charac = Character.Character()

    # set all character object attributes
    charac.set_name(char_elem["name"])

    charac.set_general_type("Character")

    charac.set_type(char_elem["type"])
    charac.set_state(char_elem["state"])

    charac.update_coords((char_elem["co_ord_x"] , char_elem["co_ord_y"]))

    # update_inventory, if its not empty
    if char_elem["inventory"] is not None:
      inv_list_of_ojb = []
      for inv_elem in char_elem["inventory"]:

        inv_obj = Object.Object()

        inv_obj.set_name(inv_elem["name"])

        inv_obj.update_qty(inv_elem["quantity"])
        inv_obj.set_state(inv_elem["state"])

        inv_list_of_ojb.append(inv_obj)
       
      charac.update_inventory("add", inv_list_of_ojb)

    charac.set_current_hp(char_elem["current_hp"])
    charac.set_max_hp(char_elem["max_hp"])
    charac.set_current_gold(char_elem["current_gold"])

    # add to visited, if any:
    if char_elem["visited"] is not None:
      for visit_elem in char_elem["visited"]:
        charac.update_visited((visit_elem["type"], visit_elem["name"], visit_elem["state"]))

    # set/update the turn counter:
    charac.update_turn_counter( char_elem["turn_counter"][0], char_elem["turn_counter"][1] )

    # append the character object to the 'characters' list of objects
    characters.append(charac)

  # return characters list
  return characters




























if __name__ == "__main__":

# ------------------------------------------------------------ 
# TEST: this can be removed from working program, only here 
#       to test function is working 

  # object_status_data = text_file_processor.load_object_status_file()


  # print("object_status_data[0]: ")
  # print(object_status_data[0])

  # print()


# ------------------------------------------------------------ 
# TEST: this code tests to make sure objects list was loaded 
#       correctly, ie, prints results:

  # load a list of 'object' objects
  objects_list = load_objects_list_from_file()

  print()
  print("List of 'object' Objects:")
  print("---------------------------")
  print()


  # iterate through list of 'object' objects, print a few attributes of each
  for obj_elem in objects_list:
    str_obj = obj_elem.get_name() + "," + obj_elem.get_general_type() + "," + \
      obj_elem.get_type() + "," + obj_elem.get_state() + "," + \
      str(obj_elem.get_coords())

    print(str_obj)
  print()






  
# ------------------------------------------------------------ 
# TEST: this can be removed from working program, only here 
#       to test function is working 

  # character_status_data = text_file_processor.load_character_status_file()

  # print("character_status_data[0]: ")
  # print(character_status_data[0])

  # print()




# ------------------------------------------------------------ 
# TEST: this code tests to make sure characters list was loaded 
#       correctly, ie, prints results:

  # load a list of character objects
  characs = load_characters_list_from_file()

  print("List of 'character' Objects (with their inventory items, if any):")
  print("---------------------------------------------------------------")
  print()

  # iterate through list of character objects, print a few attributes of each
  for char_elem in characs:
    char_str = char_elem.get_name() + "," + char_elem.get_general_type() + "," + \
      char_elem.get_type() + "," + char_elem.get_state() + str(char_elem.get_coords())
    print(char_str)
    print()

    # for 'characters' that have non-empty inventory, print the contents:
    inv_list = char_elem.get_inventory()
    if len(inv_list) > 0:
      # print("len(inv_list) = ", len(inv_list))
      for inv_item in inv_list:
        
        print("inventory item name = ", inv_item.get_name())
        print("inventory item state = ", inv_item.get_state())
        print("inventory item quantity = ", inv_item.get_quantity())

    print()

  print()

