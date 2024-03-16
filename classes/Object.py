import classes.Entity as Entity
import sys
import classes.enums as Enum

class Object(Entity.Entity):

    def __init__(self):
        super().__init__()
       
        self._inventory = []
        self._general_type = Enum.general_type.OBJECT

        # sub-class specific properties:
        self.__qty = 0
        self.__gold_amt = 0
        
        
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

    