from enum import Enum

class command_type(Enum):
    BASIC = 1
    CHEAT = 2
    NORMAL = 3
    
class general_type(Enum):
    CHARACTER = 1
    OBJECT = 2
    TILE = 3