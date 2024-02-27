import textwrap

CONSOLE_OUTPUT_CHAR_WIDTH = 100


def print_minimap(world_state,coords,active_char):
    # Function handles printing one tile around the provided co-ord, assuming player is on co-ord.
    x,y = coords
        
    max_cols = len(world_state.get_tiles()[0])-1
    max_rows = len(world_state.get_tiles())-1
   
    if world_state.get_cheat_mode() == 'N':
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
        print ("\033[32m\033[1m X \033[0m",end="")
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
                    print ("\033[32m\033[1m X \033[0m",end="")
                else:
                    print (print_tile(tile, world_state.get_npc_chars_at_tile(coords)),end="")
                if x==max_rows:
                    print("") # reached end of row, prints new line
                
def print_tile (tile,characters):
    # given a provided tile or char, provide the character string to represent it as on mini-map
    if characters != []:
        # print C if theres any other char other than the player
        return " C "
    if tile.get_type() == "building":
        return " B "
    if tile.get_type() == "non-building" and tile.get_name() != "grasslands":
        return " ? "
    if tile.get_type() == "non-building":
        return " _ "
    
def wrap_text (input_str):
    wrapped_text = textwrap.fill(input_str, width=CONSOLE_OUTPUT_CHAR_WIDTH)
    return wrapped_text

def justify(text):
    words = text.split() # split input text into a list of words

    lines = []
    current_line = []
    current_length = 0

    for word in words:
        # check if the next word doesn't fit into the new line
        if current_line and current_length + len(word) + len(current_line) > CONSOLE_OUTPUT_CHAR_WIDTH:
            lines.append(full_justify(current_line)) # we reached the end of line, justify the current line
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)

    # Add the last line left-justified
    if current_line:
        lines.append(left_justify(current_line))
    
    return "\n".join(lines)

def left_justify(line_words):
        return ' '.join(line_words)
        
def full_justify(line_words):
    total_space_needed = CONSOLE_OUTPUT_CHAR_WIDTH - sum(len(word) for word in line_words)
    gaps = len(line_words) - 1
    space, extra = divmod(total_space_needed, gaps)
        
    justified_line = ''
    for i, word in enumerate(line_words[:-1]):
        justified_line += word + ' ' * (space + (1 if i < extra else 0))
    justified_line += line_words[-1]  # Add the last word without extra space
        
    return justified_line
