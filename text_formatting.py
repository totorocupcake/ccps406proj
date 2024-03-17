import re

CONSOLE_OUTPUT_CHAR_WIDTH = 100


def print_minimap(world_state,coords,active_char):
    # Function handles printing one tile around the provided co-ord, assuming player is on co-ord.
    x,y = coords
        
    max_cols = len(world_state.get_tiles()[0])-1
    max_rows = len(world_state.get_tiles())-1
   
    if not world_state.get_cheat_mode():
        # print only 1 tile around active player with no cheat mode
        
        # first row ######################################################################################################
        if y-1 >=0:
            if x-1 >=0:
                print(print_tile (world_state.get_tiles()[x-1][y-1],world_state.get_npc_chars_at_tile((x-1,y-1))),end="")
            print(print_tile (world_state.get_tiles()[x][y-1],world_state.get_npc_chars_at_tile((x,y-1))),end="")
            if x+1 <= max_rows:
                print(print_tile (world_state.get_tiles()[x+1][y-1],world_state.get_npc_chars_at_tile((x+1,y-1))))
            else:
                print("") # reached end of row, prints new line
        
        # second row ######################################################################################################
        if x-1 >=0:
            print(print_tile (world_state.get_tiles()[x-1][y],world_state.get_npc_chars_at_tile((x-1,y))),end="")
        # active player is represented as a green X on the minimap:
        print ("\033[32m\033[1m O \033[0m",end="")
        if x+1 <= max_rows:
            print(print_tile (world_state.get_tiles()[x+1][y],world_state.get_npc_chars_at_tile((x+1,y))))
        else:
            print("") # reached end of row, prints new line
            
        # third row ######################################################################################################
        if y+1 <= max_cols:
            if x-1 >=0:
                print(print_tile (world_state.get_tiles()[x-1][y+1],world_state.get_npc_chars_at_tile((x-1,y+1))),end="")
            print(print_tile (world_state.get_tiles()[x][y+1],world_state.get_npc_chars_at_tile((x,y+1))),end="")
            if x+1<= max_rows:
                print(print_tile (world_state.get_tiles()[x+1][y+1],world_state.get_npc_chars_at_tile((x+1,y+1))))
            else:
                print("") # reached end of row, prints new line
    else:
        # cheat mode is activated, so we display the entire world map
        transposed_world_map= [list(row) for row in zip(*world_state.get_tiles())]

        for row in transposed_world_map:
            for tile in row:
                coords = tile.get_coords()
                x,y = coords
                
                if active_char.get_coords() == coords:
                    print ("\033[32m\033[1m O \033[0m",end="")
                else:
                    print (print_tile(tile, world_state.get_npc_chars_at_tile(coords)),end="")
                if x==max_rows:
                    print("") # reached end of row, prints new line
                
def print_tile (tile,characters):
    # given a provided tile or char, provide the character string to represent it as on mini-map
    
    if tile.get_type() == "building":
        return " B "
    
    if tile.get_block():
        return " X "
    
    if characters != []:
        for character in characters:
            if character.get_type().lower() == "monster" or character.get_type().lower()=="animal":
                return " M "
        return " C "
    
    if tile.get_type() == "road":
        return " - "
    
    if tile.get_type() == "non-building" and tile.get_name() != "grasslands":
        return " ? "
    
    if tile.get_type() == "non-building":
        return " _ "

def justify(text):
    """
    This function fully justify aligns a given text string, width determined by CONSOLE_OUTPUT_CHAR_WIDTH.
    Returns back justified string.
    """
    words = text.split()

    lines = []
    current_line = []
    current_length = 0

    for word in words:
        # check if the next word doesn't fit into the new line
        if current_line and current_length + len(word) + len(current_line) > CONSOLE_OUTPUT_CHAR_WIDTH:
            lines.append(full_justify(current_line)) # we reached the end of line, justify the current line
            current_line = [word]   # put the word that doesnt fit into the next line
            current_length = len(word)
        else:
            # adds word to current line
            current_line.append(word)
            current_length += len(word)

    # Add the last line left-justified if there's still a line left over
    if current_line:
        lines.append(' '.join(current_line))
    
    return "\n".join(lines)

def full_justify(line_words):
    # compute the amount of total spaces needed in the line
    total_space_needed = CONSOLE_OUTPUT_CHAR_WIDTH - sum(len(word) for word in line_words)
    gaps = len(line_words) - 1  # computes the number of gaps between words in line
    space, extra = divmod(total_space_needed, gaps) 
    # space is the number of spaces we need between each word
    # extra is the remainder, of how many extra spaces we still need to add
        
    justified_line = ''
    for i, word in enumerate(line_words[:-1]):
        # adds number of space between each word, +1 extra for i < extra
        justified_line += word + ' ' * (space + (1 if i < extra else 0))
        
    justified_line += line_words[-1]  # Add the last word without extra space
    return justified_line

def dynamic_variable_processor(world_state,get_desc_string):
    # Given a sentence string (from get_description()) replace any dynamic variables within our text files
    # with the relevant variable value from memory
    
    pattern = r'%([^%]+)%'
    
    get_desc_string = re.sub(pattern, lambda match: dynamic_variable_logic(world_state,match.group(1)), get_desc_string)
    
    return get_desc_string
    
def dynamic_variable_logic(world_state,keyword):
    # Given the keyword string, replace it with a value and return that value back
        
        if keyword == "player_name":
            for charac in world_state.get_characters():
                if charac.get_type() == "player":
                    return charac.get_name()
        elif keyword == "rent_amount":
            return str(world_state.get_rent_amount())
        elif keyword == "rent_due_days_away":
            return str(world_state.get_rent_due_date())
        elif keyword=="gold":
            for charac in world_state.get_characters():
                if charac.get_type() == "player":
                    return str(charac.get_current_gold())