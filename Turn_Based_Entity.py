import Entity


class Turn_Based_Entity(Entity.Entity):
  # CLASS CONSTRUCTOR
  def __init__(self): 
      self.__turn_count = 0
      self.__state = ""


  # this method doesn't work for some reason, so I created update_turn_counter(), 
  #     was getting strange errors when accessing it in other code.
  def set_turn_counter(self, turn_no, turn_state):
      self.__turn_count = turn_no
      self.__state = turn_state

  def update_turn_counter(self, turn_no, turn_state):
      self.__turn_count = turn_no
      self.__state = turn_state

