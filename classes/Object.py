import classes.Entity as Entity

class Object(Entity.Entity):

    # CLASS CONSTRUCTOR
    def __init__(self):
        # call super class constructor: 
        super().__init__()
       
        self._inventory = []
        self._general_type = "Object"

        # sub-class specific properties:
        self.__qty = 0
        self.__gold_amt = 0

    # Sub-class specific methods:
    def update_qty(self, adjustment): 
        self.__qty = self.__qty + adjustment  #if want to subtract, just make adjustment negative

    def set_gold_amt(self, gold_amt):
        self.__gold_amt = gold_amt

    def get_quantity(self):
        return self.__qty

    def get_gold_amt(self):
        return self.__gold_amt
