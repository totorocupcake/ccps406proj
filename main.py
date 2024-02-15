import json
import text_file_processor
import game_initialization

if __name__ == "__main__":
    
    """
    Text parsing
    """
    object_status = text_file_processor.load_object_status_file()
    character_status= text_file_processor.load_character_status_file()
    world_map_status = text_file_processor.load_world_map_status_csv()
    tile_id_mapping = text_file_processor.load_tileIDMapping_file()
    
    """
    Game initialization
    """
    game_initialization(object_status, character_status,world_map_status,tile_id_mapping)
    # This should return arrays of the created instantiated classes
    
    
    #game_loop()
    #exit_game_loop()
    #utility()