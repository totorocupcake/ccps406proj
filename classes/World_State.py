import classes.Character as Character
import classes.Object as Object
import classes.Tile as Tile
import classes.enums as Enum
import text_file_processor
import random
import npc_behaviors
import sys

# constants: (make sure they match values in load_status_data.py)

WORLD_MAP_NUM_ROWS = text_file_processor.WORLD_MAP_STATUS_ROWS
WORLD_MAP_NUM_COLUMNS = text_file_processor.WORLD_MAP_STATUS_COLUMNS
INTEREST_RATE = 0.15
TURN_INCREMENT = 20

class World_State:

  _instance = None
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(World_State, cls).__new__(cls)
    return cls._instance

  def __init__(self):
    
    random.seed(42) # select seed for reproducible random results for testing

    self.__turn_number = 0  
    self.__game_won = False
    self.__rent_amount = 0
    self.__rent_due_date = 0
    self.__characters = []  # array/list of character objects
    self.__tiles = [[None] * WORLD_MAP_NUM_COLUMNS for _ in range(WORLD_MAP_NUM_ROWS)]
    self.__cheat_mode = False
    self.__graze = True
    

  def set_turn_number (self, num):
    
    if not isinstance(num, int):
      sys.stderr.write("Error: Turn number value is invalid\n")
      sys.exit(1)
    
    self.__turn_number = num
    
  def increment_turn(self,amount=1):
    
    if not isinstance(amount, int):
      sys.stderr.write("Error: Turn number value is invalid\n")
      sys.exit(1)
    
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
    
    self = spawn_monster_checks(self)
    
    return self
  
  def set_game_won(self, flag):
    
    if not isinstance(flag, bool):
      sys.stderr.write("Error: Game won value is invalid\n")
      sys.exit(1)
      
    self.__game_won = flag

  def update_rent_turn_due(self, increment):
    
    if not isinstance(increment, int):
      sys.stderr.write("Error: Rent due value is invalid\n")
      sys.exit(1)
      
    self.__rent_due_date += increment
    
  def set_rent_turn_due(self,new_rent_turn_due):
    
    if not isinstance(new_rent_turn_due, int):
      sys.stderr.write("Error: Rent due value is invalid\n")
      sys.exit(1)
    
    self.__rent_due_date = new_rent_turn_due

  def update_rent_amount(self, increment):
    
    if not isinstance(increment, int):
      sys.stderr.write("Error: Rent value is invalid\n")
      sys.exit(1)
    
    self.__rent_amount += increment
    
  def set_rent_amount(self,new_rent_amount):
    
    if not isinstance(new_rent_amount, int):
      sys.stderr.write("Error: Rent value is invalid\n")
      sys.exit(1)
      
    self.__rent_amount = new_rent_amount

  def spawn_character(self, new_character):
    
    if not isinstance(new_character, Character.Character):
      sys.stderr.write("Error: Spawn character value is invalid\n")
      sys.exit(1)
      
    if new_character not in self.__characters:
      self.__characters.append(new_character)

  def remove_character(self, character):
    
    if not isinstance(character, Character.Character):
      sys.stderr.write("Error: Remove character value is invalid\n")
      sys.exit(1)

    # check to make sure inputted character is in the __characters list
    if character in self.__characters:
      if character.get_active_player():
        print(f"The controlled character was killed. Switching back to original player's perspective.")
        
        for charac in self.get_characters():
          if charac.get_type() == Enum.character_type.player:
            charac.set_active_player(True)
            
      self.__characters.remove(character)
    return self

  def update_tile(self, coords, new_tile):
    
    if not isinstance(new_tile, Tile.Tile) and not isinstance(coords, tuple):
      sys.stderr.write("Error: Update tile value is invalid\n")
      sys.exit(1)
    
    x_coord, y_coord = coords
    
    if not isinstance(x_coord, int) and not isinstance(y_coord, int):
      sys.stderr.write("Error: Update tile value is invalid\n")
      sys.exit(1)
    
    self.__tiles[x_coord][y_coord] = new_tile

  def load_2D_Tiles_array(self, Tile_2D_array):
    self.__tiles = Tile_2D_array

  def get_tile_at_coords(self, coords):
    
    if not isinstance(coords, tuple):
      sys.stderr.write("Error: Coordinate value is invalid\n")
      sys.exit(1)
    
    x_coord, y_coord = coords
    
    if not isinstance(x_coord, int) and not isinstance(y_coord, int):
      sys.stderr.write("Error: Coordinate value is invalid\n")
      sys.exit(1)
    
    return self.__tiles[x_coord][y_coord]

  def get_tile_by_name(self, tile_name):

    if not isinstance(tile_name, str):
      sys.stderr.write("Error: Tile name value is invalid\n")
      sys.exit(1)
    
    num_rows = WORLD_MAP_NUM_ROWS
    num_cols = WORLD_MAP_NUM_COLUMNS

    for i in range(num_cols):
      for j in range(num_rows):
        if tile_name == self.__tiles[i][j].get_name():
          return self.__tiles[i][j]
    return None

  def get_npc_chars_at_tile(self, coords):
  # return a list of npc characters for a given tile, based on its coords

    if not isinstance(coords, tuple):
      sys.stderr.write("Error: Coordinate value is invalid\n")
      sys.exit(1)
    
    # get all characters as a list
    npc_char_list = self.get_chars_at_tile(coords)

    # remove the player character from the list
    if npc_char_list is not None:
      for npc_elem in npc_char_list:
        if npc_elem.get_active_player():
          npc_char_list.remove(npc_elem)
          break

    return npc_char_list
    
  def get_chars_at_tile(self, coords):
  # return the character list for a given tile, based on its coords

    if not isinstance(coords, tuple):
      sys.stderr.write("Error: Coordinate value is invalid\n")
      sys.exit(1)
    
    x_coord, y_coord = coords
    
    if not isinstance(x_coord, int) and not isinstance(y_coord, int):
      sys.stderr.write("Error: Coordinate value is invalid\n")
      sys.exit(1)
    

    char_list = self.__characters

    current_char_list = []

    if char_list is not None:
      for char_elem in char_list:
        x_char, y_char = char_elem.get_coords()
        if (x_char == x_coord) and (y_char == y_coord):
          current_char_list.append(char_elem)

    return current_char_list

  def get_active_char(self):
    # Returns the Character with active player flag set to Y
    
    for char in self.__characters:
      if char.get_active_player():
        return char

    return None

  def get_description(self, coords, visited):
  # returns a list/array of description strings for a given coords and 
  # visited set (of tuples of (type, name, state))
  
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
      desc_list.append(current_tl.get_desc(False,self))
    else:
      desc_list.append(current_tl.get_desc(True,self))

    # add each character:
    if current_npc_char_list is not None and current_tl.get_movable():
      for char_elem in current_npc_char_list:
        char_tuple = (char_elem.get_general_type(), char_elem.get_name(), \
                      char_elem.get_state() )

        if char_tuple in visited:
          desc_list.append(char_elem.get_desc(False,self))
        else:
          desc_list.append(char_elem.get_desc(True,self))
        

    # add each object in the tile's inventory:
    if current_tl.get_movable():
      if current_tl_inv_list is not None:
        for tl_inv_elem in current_tl_inv_list:
          inv_tuple = (tl_inv_elem.get_general_type(), tl_inv_elem.get_name(), \
                        tl_inv_elem.get_state() )
          if inv_tuple in visited:
            desc_list.append(tl_inv_elem.get_desc(False,self))
          else:
            desc_list.append(tl_inv_elem.get_desc(True,self))


    # ------------------------------------------------------
    # this code assembles the desc list into a single string
    #    called desc_detail and returns it:
    # ------------------------------------------------------
    desc_detail = ""
    desc_count = 0

    for desc_elem in desc_list:
      
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
    
    if not isinstance(flag, bool):
      sys.stderr.write("Error: Graze value is invalid\n")
      sys.exit(1)
    
    self.__graze=flag
    
  def get_graze(self):
    return self.__graze
  
  def set_cheat_mode(self,flag):
    
    if not isinstance(flag, bool):
      sys.stderr.write("Error: Cheat mode value is invalid\n")
      sys.exit(1)
      
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
    
    # steal gold from player if on same tile, otherwise roam the grass
    if charac.get_name() == "Thief" and charac.get_state() =="aggressive":
      next_command = npc_behaviors.thief_aggressive(self,charac)
        
    # kill chicken/cow if there is chicken/cow on same tile, otherwise it just moves randomly on grass
    elif charac.get_name() == "Wolf" and charac.get_state() =="aggressive":
      next_command = npc_behaviors.wolf_aggressive(self,charac)

    # cow is slower moving compared to chicken, it only moves once every 3 turns, roams grass
    elif charac.get_name() == "cow" and charac.get_state()=="wild":
      next_command=npc_behaviors.cow_wild(self,charac)

    elif charac.get_name() == "chicken" and charac.get_state()=="wild":
      next_command=npc_behaviors.check_graze(self,charac)
    
    else:
      # default do nothing if no behavior defined for character
      return None
    
    return next_command
  
  def cheat_mode(self, command,charac):
    
    command = command.strip()
    words = command.split()
    
    try:
      if words[0] == "spawn":
        charac_name = words[1]
        charac_state = words[2]
        charac_coord = words[3]
        charac_coord = charac_coord.split(',')
        x = int(charac_coord[0])
        y = int(charac_coord[1]) 
        
        if charac_name in ("thief", "penny","jimmy","claire","wolf"):
          charac_name = charac_name[0].upper() + charac_name[1:]

        new_charac = Character.Character(charac_name,charac_state,(x,y))
        self.spawn_character(new_charac)
        print("Spawned character")
      elif command == "graze":
        if self.get_graze():
          self.set_graze(False)
          print("All monster graze movement paused.")
        else:
          self.set_graze(True)
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
            self = self.remove_character(charac)
            print("Removed character.")
            break
      elif words[0]=="swap": #cheat swap penny
        charac_to_swap=words[1]
        for charac in self.get_characters():
          if charac.get_name().lower() == charac_to_swap:
            current_active_char = self.get_active_char()
            current_active_char.set_active_player(False)
            charac.set_active_player(True)
      elif words[0] == "create": #cheat create state gun
        name = " ".join(words[2:])
        obj = Object.Object(name,words[1],1)
        charac.update_inventory("add",[obj])
        print(f"Added {name} into your inventory.")
      elif words[0] == "gold": #cheat gold 500
        new_gold = int(words[1])
        charac.set_current_gold(new_gold)
        print(f"Gold updated to {new_gold}")
      elif words[0] == "rent_amount": #cheat rent_amount 500
        new_rent_amount = int(words[1])
        self.set_rent_amount(new_rent_amount)
      elif words[0]=="rent_due": #cheat rent_due 50
        new_turn_due = int(words[1])
        self.set_rent_turn_due(new_turn_due)
    
      else:
        print("Cheat command not recognized.")
      
      return self
    except (ValueError,IndexError): 
      print("Invalid cheat mode command format.")
      
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
        
  for item in world_state.get_active_char().get_inventory():
    for i in range(len(characters_to_find)):
      if item.get_name().lower()== characters_to_find[i]:
        found_status[i]=1
  
          
  template_char = text_file_processor.load_char_template_file()
  
  # for all characters not found (not_found=0), we find the template char status with matching name
  # And spawn that character from template into the world_state
  for i in range(len(characters_to_find)):
    if found_status[i]==0:
      for element in template_char:
        if element["name"].lower() == characters_to_find[i].lower():
          # we found the character in the template JSON. Time to spawn it.
          new_charac = Character.Character(element["name"],element["state"])   
          world_state.spawn_character(new_charac)
          #print(f"Spawned {new_charac.get_name()}.")
          
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
            x,y = tile.get_coords()
            interest_letter = Object.Object("letter from landlord","null",1)
            interest_letter.update_coords((x,y))
            tile.update_inventory("add",[interest_letter])
            break
  return world_state
