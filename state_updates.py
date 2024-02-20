def basic_commands(world_state,charac,command):
    basic_commands = ["n","s","w","e","inventory"]
    
    if command=="inventory":
        object_string=""
        
        print("Inventory: ",end="")
        
        for obj in charac.get_inventory():
            # loop through each item in character's inventory
            
            object_string+=obj.get_name()
            
            # append x[quantity] after each item
            object_string+=" x"
            object_string+=str(obj.get_quantity())
            
            # append comma between items
            object_string+=", "
        
        # remove dangling comma added at end of last item
        object_string = object_string[:-2]
        
        print(object_string) # print inventory
        
    else:
        x,y = charac.get_coords()
        
        if command == "n":
            y-=1
        elif command == "s":
            y+=1
        elif command == "w":
            x-=1
        elif command == "e":
            x+=1

        max_cols = len(world_state.get_tiles()[0])-1
        max_rows = len(world_state.get_tiles())-1
        
        if x<=max_rows and x>= 0 and y>=0 and y<=max_cols:
            charac.update_coords((x,y))
        else:
            print("You cannot go there.") 
               
    return world_state