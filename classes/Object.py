import classes.Entity as Entity
import sys
import classes.enums as Enum
import classes.Data as Data

class Object(Entity.Entity):

    def __init__(self, name=None,state=None,quantity=None):
        super().__init__()
       
        self._inventory = []
        self._general_type = Enum.general_type.OBJECT

        # sub-class specific properties:
        self.__qty = 0
        self.__gold_amt = 0
        
        if name is not None and state is not None and quantity is not None:
            self.set_name(name)
            self.update_qty(quantity)
            self.set_state(state)
            self.set_type(Enum.obj_type[Data.Data().lookup_type(self.get_general_type(),name,state)])
            self.set_gold_amt(Data.Data().lookup_gold_amt(name,state))
        
    def get_quantity(self):
        return self.__qty

    def get_gold_amt(self):
        return self.__gold_amt

    # Sub-class specific methods:
    def update_qty(self, adjustment): 
        
        if not isinstance(adjustment, int):
            sys.stderr.write("Error: Item quantity is invalid\n")
            sys.exit(1)
        
        self.__qty = self.__qty + adjustment  #if want to subtract, just make adjustment negative

    def set_gold_amt(self, gold_amt):
        
        if not isinstance(gold_amt, int):
            sys.stderr.write("Error: Gold value is invalid\n")
            sys.exit(1)
            
        self.__gold_amt = gold_amt

    def set_type(self, new_type):
    
        if new_type is not None and not isinstance(new_type,Enum.obj_type):
            sys.stderr.write("Error: Obj type value is invalid\n")
            sys.exit(1)
        
        self._type = new_type
