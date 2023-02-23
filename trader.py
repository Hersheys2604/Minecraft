from __future__ import annotations

from abc import abstractmethod, ABC
from material import Material
from random_gen import RandomGen
from avl import AVLTree
from node import AVLTreeNode
from hash_table import LinearProbeTable

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]


class Trader(ABC):
    """
    Trader class is the parent class that contains the base attributes for the follownig classes:
    RandomTrader
    RangeTrader
    HardTrader
    """

    def __init__(self, name: str) -> None:
        '''
        Defines all the variables present in a Trader instance. 
        Best case and worst case complexity = O(1)
        '''
        self.name = name
        self.all_materials = None
        self.buying_price = None
        self.all_mining_rates = []
        self.material = None
        self.buying_price = None
        self.currently_selling = False
        self.ratio = None

    @classmethod
    def random_trader(cls):
        """
        Grebrates and returns a random trader
        Best and worst case complexity: O(1)
        """
        return RandomTrader(TRADER_NAMES[RandomGen.randint(0, len(TRADER_NAMES)-1)])
    
    @abstractmethod
    def set_all_materials(self, mats: list[Material]) -> None:
        pass

    @abstractmethod
    def add_material(self, mat: Material) -> None:
        pass

    def is_currently_selling(self) -> bool:
        """
        Returns if the trader has generated a deal and is currently selling (bool).
        Best and worst case complexity: O(1)
        """
        return self.currently_selling

    def current_deal(self) -> tuple[Material, float]:
        """
        Returns a tuble consiting of the material the trader is buying and the buying price of the material
        Best and worst case complexity: O(1)
        """
        if self.material is None:
            raise ValueError("No Current Deal")
        else:
            return (self.material, self.buying_price)

    @abstractmethod
    def generate_deal(self) -> None:
        pass

    def stop_deal(self) -> None:
        """
        Sets the currently selling varibale into False.
        Best and worst case complexity: O(1)
        """
        self.currently_selling = False

    @abstractmethod
    def __str__(self) -> str:
        pass


class RandomTrader(Trader):
    """
    RandomTrader trades randomly traded deals.
    """

    def __init__(self, name: str) -> None:
        '''
        Defines all the variables present in a Random Trader instance. 
        Best case and worst case complexity = O(1)
        '''
        Trader.__init__(self, name)
        self.all_materials = []

    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Sets all the materials available to this trader as a list
        best and worst case complexity: O(m)
        """
        self.all_materials.clear()
        for material in mats:
            self.all_materials.append(material)
    
    def add_material(self, mat: Material) -> None:
        """
        Adds materials onto this trader's inventory list
        best and worst case complexity: O(1)
        """
        self.all_materials.append(mat)

    def generate_deal(self) -> None:
        """
        Generates a deal by randomly selecting an item from the trader's inventory and setting a buying prrice for that item 
        best and worst case complexity: O(1)
        """
        self.material = self.all_materials[RandomGen.randint(0, len(self.all_materials) - 1)]
        self.buying_price = round(2+8*RandomGen.random_float(), 2)
        self.currently_selling = True
        self.ratio = self.material.mining_rate / self.buying_price

    def __str__(self) -> str:
        """
        String Representation of Random Trader
        best and worst complexity: O(1)
        """
        if self.material is not None:
            return f"<RandomTrader: {self.name} buying [{self.material.name}: {self.material.mining_rate}🍗/💎] for {self.buying_price}💰>"
        else:
            return f"<RandomTrader: {self.name}>"

class RangeTrader(Trader):
    
    """
    RangeTrader offers a deal based on a radnom deal inside range of the mining rate
    """

    def __init__(self, name: str) -> None:
        """
        Defines all the variables present in a Range Trader instance. 
        best and worst case complexity: O(1)
        """
        Trader.__init__(self, name)
        self.all_materials = AVLTree()

    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Sets all the materials available to this trader as a AVL Tree
        Worst case complexity: O(mlog(m))
        """
        self.all_materials = AVLTree()
        for material in mats:
            self.all_materials[material.mining_rate] = material
    
    def add_material(self, mat: Material) -> None:
        """
        Adds materials onto this trader's inventory list
        best and worst case complexity: O(log(m))
        """
        self.all_materials[mat.mining_rate] = mat

    def generate_deal(self) -> None:
        """
        Generates a deal by randomly selecting a range. Then pulling out all the items in that range then randomly choosing
        an item from the trader's range and setting a buying prrice for that item 
        Best Case = worst case complexity = O(j - i + log(m))
        """
        i = RandomGen.randint(0, len(self.all_materials) - 1) 
        j = RandomGen.randint(i, len(self.all_materials) - 1)

        lst_i_j = self.materials_between(i,j) #Return random material (within conditions)
        
        ran_num = RandomGen.randint(0, len(lst_i_j) - 1)
        self.material = lst_i_j[ran_num]
        self.buying_price = round(2+8*RandomGen.random_float(), 2) #Generate random price 
        self.currently_selling = True

        self.ratio = self.material.mining_rate / self.buying_price

    def materials_between(self, i: int, j: int) -> list[Material]:
        """
        Function to get Materials inbetween for generate deal.
        best case: O(1)
        worst case complexity: O(j - i + log(m))
        """
        return self.all_materials.range_between(i, j)
        
    def __str__(self) -> str:
        """
        String Representation of Random Trader
        best and worst case: O(1)
        """
        if self.material is not None:
            return f"<RangeTrader: {self.name} buying [{self.material.name}: {self.material.mining_rate}🍗/💎] for {self.buying_price}💰>"
        else:
            return f"<RangeTrader: {self.name}>"


class HardTrader(Trader):
    """
    HardTrader will trade the hardest to mine to mine material
    """
    
    def __init__(self, name: str) -> None:
        '''
        Defines all the variables present in a Hard Trader instance. 
        Best=Worst Case Complexity = O(50)
        '''
        Trader.__init__(self, name)
        self.all_materials = LinearProbeTable(50)
    
    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Sets all the materials available to this trader in a Hash Table
        best an worst case complexity: O(M)
        """
        self.all_materials = LinearProbeTable(len(list))
        for material in mats:
            self.all_materials.insert(material.name, material)

    
    def add_material(self, mat: Material) -> None:
        """
        Adds materials onto this trader's inventory list
        best and worst case complexity: O(1)
        """
        self.all_materials.insert(mat.name,mat)

    def generate_deal(self) -> None:
        """
        Generates a deal by selecting the harderst to mine item from the trader's inventory and setting a buying prrice for that item 
        best and worst case: O(M)
        """
        all_materials_list = self.all_materials.values()        # O(M)
        hardest_material_name = None
        hardest_mining_rate = 0
        for material in all_materials_list:                         # O(M)
            if material.mining_rate > hardest_mining_rate:
                hardest_material_name = material.name
                hardest_mining_rate = material.mining_rate

        self.material = self.all_materials[hardest_material_name]
        del self.all_materials[hardest_material_name]               # assumning hashtable functions dont have clusters and thus O(1)
        self.buying_price = round(2+8*RandomGen.random_float(), 2)
        self.currently_selling = True

        self.ratio = self.material.mining_rate / self.buying_price
    
    def __str__(self) -> str:
        """
        String Representation of Random Trader
        best and worst case complexity:O(1)
        """
        if self.material is not None:
            return f"<HardTrader: {self.name} buying [{self.material.name}: {self.material.mining_rate}🍗/💎] for {self.buying_price}💰>"
        else:
            return f"<HardTrader: {self.name}>"

        


if __name__ == "__main__":
    trader = RangeTrader("Jackson")
    print(trader)
    trader.set_all_materials([
        Material("Coal", 4.5),
        Material("Diamonds", 3),
        Material("Redstone", 20),
    ])
    trader.generate_deal()
    print(trader)
    trader.stop_deal()
    print(trader)
