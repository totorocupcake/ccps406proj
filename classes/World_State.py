import classes.Character as Character
import classes.Tile as Tile
import classes.Object as Object
import text_file_processor
import random
import npc_behaviors


# constants: (make sure they match values in load_status_data.py)

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS
INTEREST_RATE = 1.05
TURN_INCREMENT = 20
class World_State:

  # constructor:

  def __init__(self):
    
    random.seed(42) # select seed for reproducible random results for testing
    # Private properties (with default starting values)
    self.__turn_number = 0  
    self.__game_won = 'N'
    self.__rent_amount = 0
    self.__rent_due_date = 0
    self.__characters = []  # array/list of character objects
    self.__tiles = [[None] * WORLD_MAP_NUM_COLUMNS for _ in range(WORLD_MAP_NUM_ROWS)]

    self.__saved_tiles = []
    self.__cheat_mode = 'N'
    self.__graze = 'Y'

  # needed for lock/open
  def update_saved_tiles(self, add_remove, tile):
      # adds/removes 'tiles' from the .__saved_tiles list, given a 'tile' object
      # add_remove should = "add" for add case

      if add_remove == "add":
        self.__saved_tiles.append(tile)

      else:
        self.__saved_tiles.remove(tile)

  # needed for lock/open
  def get_saved_tile_by_name(self, tile_name):
    for tile_elem in self.__saved_tiles:
      if tile_elem.get_name() == tile_name:
        return tile_elem
    # else
    return None

  def increment_turn(self, amount=1):
    self.__turn_number += amount
    
    # check if player is late to pay rent, if so, add letter in their mailbox
    self = late_rent_checks(self)
    
    # turn counting checks for all chars
    for char in self.__characters:
        char.decrement_turn_count()
    
    # turn counting checks for all tiles    
    for row in self.__tiles:
      for tiles in row:
        tiles.decrement_turn_count()
    
    # monster/animal respawning checks
    self = spawn_monster_checks(self)
    
    return self
  
  def set_game_won(self, flag):
    self.__game_won = flag

  def update_rent_turn_due(self, increment):
    self.__rent_due_date += increment

  def update_rent_amount(self, increment):
    self.__rent_amount += increment

  def spawn_character(self, new_character):
    if new_character not in self.__characters:
      self.__characters.append(new_character)

  def remove_character(self, character):
    # check to make sure inputted character is in the __characters list
    if character in self.__characters:
      self.__characters.remove(character)

  def update_tile(self, coords, new_tile):
    x_coord, y_coord = coords
    self.__tiles[x_coord][y_coord] = new_tile

  def load_2D_Tiles_array(self, Tile_2D_array):
    self.__tiles = Tile_2D_array

  def get_tile_at_coords(self, coords):
    x_coord, y_coord = coords
    return self.__tiles[x_coord][y_coord]

  def get_tile_by_name(self, tile_name):

    num_rows = WORLD_MAP_NUM_ROWS
    num_cols = WORLD_MAP_NUM_COLUMNS

    for i in range(num_cols):
      inner_array = []
      for j in range(num_rows):
        # if tile_name == self.__tiles[j][i].get_name():
        if tile_name == self.__tiles[i][j].get_name():
          return self.__tiles[i][j]
    return None

  def get_npc_chars_at_tile(self, coords):
  # return a list of npc characters for a given tile, based on its coords

    # get all characters as a list
    npc_char_list = self.get_chars_at_tile(coords)

    # remove the player character from the list
    if npc_char_list is not None:
      for npc_elem in npc_char_list:
        # remove the 'player' character from the list
        if npc_elem.get_type() == "player":
          npc_char_list.remove(npc_elem)
          break

    return npc_char_list
    
  def get_chars_at_tile(self, coords):
  # return the character list for a given tile, based on its coords

    x_coord, y_coord = coords

    char_list = self.__characters

    current_char_list = []

    if char_list is not None:
      for char_elem in char_list:
        x_char, y_char = char_elem.get_coords()
        if (x_char == x_coord) and (y_char == y_coord):
          current_char_list.append(char_elem)

    return current_char_list

  def get_active_char(self):
    # Returns the Character with active player flaf set to Y
    for char in self.__characters:
      if char.get_active_player() == 'Y':
        return char

    return None

  def get_description(self, coords, visited):
  # returns a list/array of description strings for a given coords and 
  #   visited set (of tuples of (type, name, state))
    x_coord, y_coord = coords

    # get the tile at coords
    current_tl = self.__tiles[x_coord][y_coord]

    # get the current tile's inventory:
    current_tl_inv_list = []
    current_tl_inv_list = current_tl.get_inventory()

    # get a list of all npc's for the current coords
    current_npc_char_list = []
    current_npc_char_list = self.get_npc_chars_at_tile(coords)

    # intialize the description list of strings:
    desc_list = []

    # for each tile, character and object, check and see if in visited set
    #   if no, use "long" desc
    #   if yes, use "short" desc

    # start with Tile object:
    tile_tuple = (current_tl.get_general_type(), current_tl.get_name(), current_tl.get_state())

    if tile_tuple in visited:
      desc_list.append(current_tl.get_desc("short"))
    else:
      desc_list.append(current_tl.get_desc("long"))

    # add each character:
    if current_npc_char_list is not None:
      for char_elem in current_npc_char_list:
        char_tuple = (char_elem.get_general_type(), char_elem.get_name(), \
                      char_elem.get_state() )

        if char_tuple in visited:
          desc_list.append(char_elem.get_desc("short"))
        else:
          desc_list.append(char_elem.get_desc("long"))
        

    # add each object in the tile's inventory:
    if current_tl_inv_list is not None:
      for tl_inv_elem in current_tl_inv_list:
        inv_tuple = (tl_inv_elem.get_general_type(), tl_inv_elem.get_name(), \
                      tl_inv_elem.get_state() )
        if inv_tuple in visited:
          desc_list.append(tl_inv_elem.get_desc("short"))
        else:
          desc_list.append(tl_inv_elem.get_desc("long"))


    # ------------------------------------------------------
    # this code assembles the desc list into a single string
    #    called desc_detail and returns it:
    # ------------------------------------------------------
    desc_detail = ""
    desc_count = 0

    for desc_elem in desc_list:
      # print("desc((", x_coord, ",", y_coord, ")) = ", desc_elem)
      if desc_count == 0:  
        desc_detail = desc_detail + desc_elem 
      elif desc_count == 1:
        desc_detail =  desc_detail + "  You see " + desc_elem
      elif (desc_count > 1) and (desc_count < (len(desc_list)-1)):
        desc_detail = desc_detail + ", " + desc_elem
      else:
        desc_detail = desc_detail + " and " + desc_elem 
      desc_count += 1

    if desc_count > 1:
      desc_detail = desc_detail + "."


    return desc_detail

  def set_graze (self,flag):
    self.__graze=flag
    
  def get_graze(self):
    return self.__graze
  
  def set_cheat_mode(self,flag):
    self.__cheat_mode = flag

  def get_cheat_mode(self):
    return self.__cheat_mode

  def get_game_won(self):
    return self.__game_won

  def get_turn_number(self):
    return self.__turn_number
  
  def get_rent_amount(self):
    return self.__rent_amount
  
  def get_rent_due_date(self):
    return self.__rent_due_date
  
  def get_characters(self):
    return self.__characters
  
  def get_tiles(self):
    return self.__tiles

  def get_next_action (self, charac):
    # Function controls computer-controlled characters by providing their next command for console input
    
    # Aggressive thief behavior ########################################
    # steal gold from player if on same tile, otherwise roam the grass
    if charac.get_name() == "Thief" and charac.get_state() =="aggressive":
      for element in self.get_characters():
        # find the player character (note may not be the active player)
            if element.get_type() == "player":
              player = element
              break

      if player.get_coords() == charac.get_coords():
        # steal gold from player if on same tile
        player_name = player.get_name()
        next_command="steal "+ player_name
        print("Thief submitted command to steal",player_name)
        return next_command
        
    # Aggressive wolf behavior ################################################
    # kill chicken/cow if there is chicken/cow on same tile, otherwise it just moves randomly on grass
    elif charac.get_name() == "Wolf" and charac.get_state() =="aggressive":
      char_list = self.get_chars_at_tile(charac.get_coords())
      
      for char in char_list:
        if char.get_name() == "chicken":
          print("Wolf submitted command to kill chicken")
          return "kill chicken"
        elif char.get_name() == "cow":
          print("Wolf submitted command to kill cow")
          return "kill cow"

    # Wild cow behavior ###########################################################
    # cow is slower moving compared to chicken, it only moves once every 2 turns, roams grass
    elif charac.get_name() == "cow" and charac.get_state()=="wild":
      if self.get_graze() == 'Y':
        if (self.get_turn_number() % 2) == 0:
          next_command = npc_behaviors.graze(self,charac)
          return next_command
      return None
    
    # All other characters' behavior ######################################################
    else:
      # default do nothing if no behavior defined for character
      return None
    
    if self.__graze =="Y":
      # graze as default if no other action for thief,chicken,wolf
      next_command = npc_behaviors.graze(self,charac)
      return next_command
    else:
      return None


  def cheat_mode(self, command,charac):
    command = command.strip()
    words = command.split()
    
    if words[0] == "spawn":
      charac_name = words[1]
      charac_state = words[2]
      charac_coord = words[3]
      charac_coord = charac_coord.split(',')
      x = int(charac_coord[0])
      y = int(charac_coord[1]) 
      
      
      if charac_name in ("thief", "penny","jimmy","claire","wolf"):
        charac_name = charac_name[0].upper() + charac_name[1:]

      new_charac = Character.Character()
      new_charac.set_name(charac_name)
      new_charac.update_coords((x,y))
      new_charac.set_state(charac_state)
      new_charac.set_type(text_file_processor.lookup_type("Character",charac_name,charac_state))
      
      self.spawn_character(new_charac)
      print("Spawned character")
    elif command == "graze":
      if self.get_graze() == 'Y':
        self.set_graze('N')
        print("All monster graze movement paused.")
      elif self.get_graze() == 'N':
        self.set_graze('Y')
        print("All monster graze movement resumed.")
    elif words[0] == "get_desc":
      charac_coord = words[1]
      charac_coord = charac_coord.split(',')
      x = int(charac_coord[0])
      y = int(charac_coord[1])
      print (self.get_description((x,y),{}))
    elif words[0] == "teleport":
      charac_coord = words[1]
      charac_coord = charac_coord.split(',')
      x = int(charac_coord[0])
      y = int(charac_coord[1])
      charac.update_coords((x,y))
      print (f"Teleported to {x},{y}.")
    elif words[0] == "kill": #cheat kill thief 6,12
      charac_name_to_kill=words[1]
      charac_coord = words[2]
      charac_coord=charac_coord.split(',')
      x = int(charac_coord[0])
      y = int(charac_coord[1])
      for charac in self.get_chars_at_tile((x,y)):
        if charac.get_name().lower() == charac_name_to_kill:
           self.remove_character(charac)
           print("Removed character.")
           break
    return self

def spawn_monster_checks(world_state):
  """
  This function checks for the specified characters in character_to_find within all characters
  in the provided world state. If there is not at least one of each character, it will spawn one
  respective character back into the world state. The spawned character is based off character_template.json
  """
  characters_to_find = ["wolf", "thief", "chicken","cow"]
  found_status = [0,0,0,0]
  
  # find all characters in world state, and update found_status. 
  # 0 = not found, 1= found
  for char in world_state.get_characters():
    for i in range(len(characters_to_find)):
      if char.get_name().lower() == characters_to_find[i]:
        found_status[i]=1
          
  template_char = text_file_processor.load_char_template_file()
  
  # for all characters not found (not_found=0), we find the template char status with matching name
  # And spawn that character from template into the world_state
  for i in range(len(characters_to_find)):
    if found_status[i]==0:
      for element in template_char:
        if element["name"].lower() == characters_to_find[i].lower():
          # we found the character in the template JSON. Time to spawn it.
          new_charac = Character.Character()
          new_charac.set_name(element["name"])
          new_charac.set_type(element["type"])
          new_charac.update_coords((element["co_ord_x"],element["co_ord_y"]))
          new_charac.set_state(element["state"])
            
          if element["inventory"] is not None:
            inv_list_of_obj = []
            for inv_elem in element["inventory"]:
              inv_obj = Object.Object()
              inv_obj.set_name(inv_elem["name"])
              inv_obj.update_qty(inv_elem["quantity"])
              inv_obj.set_state(inv_elem["state"])
              inv_list_of_obj.append(inv_obj)
            new_charac.update_inventory("add", inv_list_of_obj)

          new_charac.set_current_hp(element["current_hp"])
          new_charac.set_max_hp(element["max_hp"])
          new_charac.set_current_gold(element["current_gold"])
          new_charac.update_turn_counter(element["turn_counter"][0],element["turn_counter"][1])
            
          world_state.spawn_character(new_charac)
          #print(f"spawn {new_charac.get_name()}.")
          
  return world_state

def late_rent_checks(world_state):
  if world_state.get_turn_number()>world_state.get_rent_due_date():
      # check if player is late to pay rent
      # update rent amount and turn due if so
      new_rent = round(world_state.get_rent_amount() * INTEREST_RATE)
      world_state.update_rent_amount(new_rent)
      world_state.update_rent_turn_due(TURN_INCREMENT)
        
      # add new letter to mailbox to notify the player
      for row in world_state.get_tiles():
        for tile in row:
          if tile.get_name() == "mail box":
            # find mail box on map and add a new letter from landlord to it
            interest_letter = Object.Object()
            interest_letter.set_name("letter from landlord")
            interest_letter.set_type("tool")
            interest_letter.set_state("null")
            interest_letter.set_gold_amt(0)
            interest_letter.update_qty(1)
            tile.update_inventory("add",[interest_letter])
            break
  return world_state

















if __name__ == "__main__":

  # ------------------------------------------------ test some methods:
  ws = World_State()

  ws.increment_turn()

  ws.set_game_won('Y')  

  ws.update_rent_turn_due(25)

  ws.update_rent_amount(10)

  print("Turn no: ",ws.get_turn_no())
  print("Game Won: ",ws.get_game_won())
  print("Rent turn due: ",ws.get_rent_due_date())
  print("Rent amount: ", ws.get_rent_amount())
  
  tl = Tile.Tile()
  tl.update_tile_by_id("01")
  ws.update_tile((1,4),tl)
  print("Tile name: ",ws.get_tiles()[1][4].get_name())
  print("Tile state: ",ws.get_tiles()[1][4].get_state())
  print("Tile general type: ",ws.get_tiles()[1][4].get_general_type())
  
  charac= Character.Character()
  charac.set_name("landlord")
  charac.set_state("unhappy")
  charac.update_coords((1,4))
  ws.spawn_character(charac)




  # # ------------ test World_State.get_description(coords, visited) function:

  # ws = load_World_State(10, 25)

  # empty_visited = set()

  # x_coord = 8
  # y_coord = 7

  # coord_tuple = (x_coord, y_coord)

  # desc_list = ws.get_description(coord_tuple, empty_visited)

  # print()
  # print("desc_list[0] = ", desc_list[0])
  # print()

  
  # print("Get Desc long: ",ws.get_description((1,4),"long"))
  # print("Get Desc short: ",ws.get_description((1,4),"short"))
  
  # print("Get Desc as str long: ",ws.get_description_as_str((1,4),"long"))
  # print("Get Desc as str short: ",ws.get_description_as_str((1,4),"short"))
  
  
  #desc = ws.get_description((1, 4), "short")
  #desc = ws.get_description_as_str((1, 4), "short")
  

  #print()
  #if desc is not None:
  #  print("desc = ", desc)
  #else:
  #  print("desc = None")
  #print()




  #----------------------------
  charac1 = Character.Character()

  charac1.set_name("first character")

  print("charac name = ", charac1.get_name())
  print()

  # test spawn_character() method
  ws.spawn_character(charac1)
  
  charac2 = Character.Character()

  charac2.set_name("second character")

  print("charac name = ", charac2.get_name())
  print()

  # test spawn_character() method
  ws.spawn_character(charac2)
  
  # test remove_character() method
  ws.remove_character(charac1)


