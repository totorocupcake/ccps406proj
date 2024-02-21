class Interaction:
  # class constructor:
  def __init__(self):

    # properties:
    self._entity_name = ""
    self._entity_general_type = ""
    self._entity_state = ""
    # store JSON interaction data in '_interaction_data' property:
    self._interaction_data = []
 
 # getter methods:
  # --------------
  def get_entity_name(self):
    return self._entity_name

  def get_entity_general_type(self):
    return self._entity_general_type

  def get_entity_state(self):
    return self._entity_state
  
  def get_interaction_data(self):
    return self._interaction_data 
  

  # setter methods:
  # --------------
  def set_entity_name(self, new_name):
    self._entity_name = new_name  

  def set_entity_general_type(self, new_general_type):
    self._entity_general_type = new_general_type

  def set_entity_state(self, new_state):
    self._entity_state = new_state

  def set_interaction_data(self, new_interaction_data):
    self._interaction_data = new_interaction_data
