import Entity


class Turn_Based_Entity(Entity.Entity):
  # CLASS CONSTRUCTOR
  def __init__(self): 
      self.__turn_counter = 0
      self.__state = ""

      # self.__inventory = []

  # def set_name(self, new_name):
  #   self.name = new_name  

  def set_turn_counter(self, turn_no, turn_state):
      self.__turn_counter = turn_no
      self.__state = turn_state
