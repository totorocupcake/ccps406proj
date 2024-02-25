import Entity

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

    def get_inventory(self):
        # returns a list of 'object' objects
        return self._inventory

    # Sub-class specific methods:
    def update_qty(self, adjustment): 
        self.__qty = self.__qty + adjustment  #if want to subtract, just make adjustment negative

    def set_gold_amt(self, gold_amt):
        self.__gold_amt = gold_amt

    def get_quantity(self):
        return self.__qty

    # def get_name(self):
    #     return self.name

    def get_gold_amt(self):
        return self.__gold_amt


if __name__ == "__main__": 

    # tl = Tile()
  
    # tl.set_name("town square")
    # tl.set_type("Tile")
    # tl.set_state("null")

    obj = Object()
    obj.set_name("watering can")
    obj.set_general_type("Object")
    obj.set_type("tool")
    obj.set_state("empty")
    
    short_desc = obj.get_desc("short")
    long_desc = obj.get_desc("long")

    print()
    print("name = ", obj.get_name())
    print("type = ", obj.get_type())
    print("state = ", obj.get_state())
    
    print()
    print("short_desc = ", short_desc)
    print("long_desc = ", long_desc)
