from enum import Enum

class command_type(Enum):
    BASIC = 1
    CHEAT = 2
    NORMAL = 3
    
class general_type(Enum):
    CHARACTER = 1
    OBJECT = 2
    TILE = 3
    
class character_type(Enum):
    player = 1
    npc = 2
    monster = 3
    animal = 4
    
class tile_type(Enum):
    building = 1
    non_building = 2
    road = 3
    blocked = 4
    