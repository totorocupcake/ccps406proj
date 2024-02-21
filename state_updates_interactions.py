import text_file_processor



def interaction_commands(world_state,charac,command):
    # lookup command (iteraction: ACTION ENTITY)
    # old way: interac = text_file_processor.lookup_interaction_key_only(command)
    # new way: using Interaction object:
    interac_obj = text_file_processor.lookup_interaction_ret_object(command)

    if interac_obj is None:
        print("I don't understand that command")
    else:
        
        # for now, just debugging info

        print("DEBUG: (advanced_commands()): interac_obj.get_entity_name(): ", \
                interac_obj.get_entity_name() )
        print("DEBUG: (advanced_commands()): interac_obj.get_entity_general_type(): ", \
                interac_obj.get_entity_general_type())
        print("DEBUG: (advanced_commands()): interac_obj.get_entity_state(): ", \
                interac_obj.get_entity_state())
        print("DEBUG: (advanced_commands()) -------------")
        print("DEBUG: (advanced_commands()): interac_obj.get_interaction_data(): ", \
                interac_obj.get_interaction_data())
        print("DEBUG: (state_updates_interactions.advanced_commands()): ")
        
        interac_JSON_data = interac_obj.get_interaction_data()

        print("\tchange_state_to: ", interac_JSON_data["change_state_to"])

        int_requirements = interac_JSON_data["requirement"]

        if len(int_requirements) > 0:
           for req_elem in int_requirements:
                print("\trequirement: ", \
                        req_elem["type"], ",", req_elem["name"], ",", \
                        req_elem["state"], ",", req_elem["qty"], ",", \
                        req_elem["remove_obj"] )
                

        

    return world_state


