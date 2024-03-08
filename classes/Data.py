import text_file_processor
import text_formatting

class Data():
    def __init__(self):
        self._tile_data = text_file_processor.load_tile_JSON_data_file()
        self._tile_id_mapping = text_file_processor.load_tileIDMapping_file()
        self._char_data = text_file_processor.load_characters_JSON_data_file()
        self._char_template = text_file_processor.load_char_template_file()
        self._objects_data = text_file_processor.load_objects_JSON_data_file()
    
    def get_tile_data(self):
        return self._tile_data
    
    def get_tile_id_mapping(self):
        return self._tile_id_mapping    
    
    def get_char_data(self):
        return self._char_data
    
    def get_char_template(self):
        return self._char_template
    
    def get_objects_data(self):
        return self._objects_data
    
    def lookup_tileID_by_name_state(self, tile_name,state):
    # given a tile name and state, find corresponding tile ID:

        parsed_tile_data = self.get_tile_id_mapping()

        for tile in parsed_tile_data:
            if (tile["name"].lower() == tile_name.lower()) and (tile["state"].lower() == state.lower()):
                return tile["tile_id"]
        return "Not Found"
    
    def lookup_desc (self, long_short, type, name, state, world_state):
    # Given arguments find, return the matching description from in-game text files
    # Returns None if not match
    # long_short determines whether to return long_desc vs short_desc
    # type determines if lookup is tile , character, object

        if type == "Object":
            parsed_data = self.get_objects_data()
        elif type == "Character":
            parsed_data = self.get_char_data()
        else:
            parsed_data = self.get_tile_data()
            
        for element in parsed_data:
            name_formatted = text_formatting.dynamic_variable_processor(world_state,element["name"])
            if (name_formatted.lower() == name.lower()) and (element["state"].lower() == state.lower()):
                if long_short == "long":
                    return element["description"]["long_desc"]
                else:
                    return element["description"]["short_desc"]
        return ""
    
    def lookup_interaction (self, type, name, state, interaction_key):
    # Given the name of a noun and its state, and its interaction word (verb) return it's interaction data
    # Return None if not match

        if type == "Object":
            parsed_data = self.get_objects_data()
        elif type == "Character":
            parsed_data = self.get_char_data()
        else:
            parsed_data = self.get_tile_data()

        for obj in parsed_data:
            if (obj["name"].lower() == name.lower()) and (obj["state"].lower() == state.lower()):
                if obj["interactions"] is not None:
                    for interac in obj["interactions"]:
                        if interac["name"].lower() == interaction_key.lower():
                            return interac
        return None
    
    def lookup_movable (self, tile_name, state):
    # Given a tile name and state, return the matching movable flag.
    # Return None if not match

        parsed_tile_data = self.get_tile_data()

        for tile in parsed_tile_data:
            if (tile["name"].lower() == tile_name.lower()) and (tile["state"].lower() == state.lower()):
                return tile["movable"]
        return None
    
    def lookup_current_hp(self, name,state):
        char_template = self.get_char_template()
        
        for char in char_template:
            if name.lower() == char["name"].lower() and state.lower() == char["state"]:
                return char["current_hp"]
    
    def lookup_max_hp(self,name,state):
        char_template = self.get_char_template()
        
        for char in char_template:
            if name.lower() == char["name"].lower() and state.lower() == char["state"]:
                return char["max_hp"]  
    
    def lookup_inventory(self,name,state):
        char_template = self.get_char_template()
    
        for char in char_template:
            if name.lower() == char["name"].lower() and state.lower() == char["state"]:
                return char["inventory"]  
    
    def lookup_char_gold(self,name,state):
        char_template = self.get_char_template()
        
        for char in char_template:
            if name.lower() == char["name"].lower() and state.lower() == char["state"]:
                return char["current_gold"]  
            
    def lookup_tile_type (self,tile_name,state):
    # Given a tile name and state, return the matching movable flag.
    # Return None if not match

        parsed_tile_data = self.get_tile_data()

        for tile in parsed_tile_data:
            if (tile["name"].lower() == tile_name.lower()) and (tile["state"].lower() == state.lower()):
                return tile["type"]

        return None
    
    def lookup_gold_amt (self,name, state):
    # Given an object name and state, return the matching gold_amt.
    # Return None if not match

        parsed_object_data = self.get_objects_data()

        for obj in parsed_object_data:
            if (obj["name"].lower() == name.lower()) and (obj["state"].lower() == state.lower()):
                return obj["gold_amt"]        
        return None
    
    def lookup_type (self,general_type,name, state):
    # returns the type value given a name and state and general type matched from JSON 
    
        if general_type == "Object":
                parsed_data = self.get_objects_data()
        elif general_type == "Character":
                parsed_data = self.get_char_data()
        else:
                parsed_data = self.get_tile_data()
                
        for obj in parsed_data:
            if (obj["name"].lower() == name.lower()) and (obj["state"].lower() == state.lower()):
                return obj["type"]
        return None

