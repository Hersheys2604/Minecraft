from __future__ import annotations
from avl import *

from cave import Cave
from material import Material
from trader import Trader
from food import Food
from random_gen import RandomGen
from hash_table import LinearProbeTable

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]

class Player():
    """
    Player class is a player that will be used to play the game. It will have the Material, Cave, Traders, Foods classes attached
    to the player class so that the player can choose within. 
    """

    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        """
        Inititialises all variables of a Player Instance
        Best and worst case complexity: O(50)
        """
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.traders = []
        self.foods = []
        self.materials = LinearProbeTable(50)
        self.caves = AVLTreeCave()
        

        

    def set_traders(self, traders_list: list[Trader]) -> None:
        """
        Sets all the traders accessible to a player
        Best and worst case complexity: O(1)
        """
        self.traders = traders_list

    def set_foods(self, foods_list: list[Food]) -> None:
        """
        sets all the foods accessible to the player
        Best and worst case complexity: O(1)
        """
        self.foods = foods_list

    @classmethod
    def random_player(self) -> Player:
        """
        Creates and Returns a Randomly generated player.
        Best and worst case complexity: O(1)
        """
        return Player(PLAYER_NAMES[RandomGen.randint(0, len(PLAYER_NAMES) - 1)], self.DEFAULT_EMERALDS)

    def set_materials(self, materials_list: list[Material]) -> None:
        """
        Sets all the Materials accessible to the player to a Hash Table
        Best and worst case complexity: O(M)
        """
        for material in materials_list:
            self.materials.insert(material.name, material)

    def set_caves(self, caves_list: list[Cave]) -> None:
        """
        Sets all the Caves accessible to the player in form of an AVL Tree
        Best and worst case complexity: O(log(C))
        """
        for cave in caves_list:
            self.caves[cave.material.mining_rate] = cave

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        '''
                                              ---- PROCESS EXPLANATION -----
        select_food_and_caves overall process idea was that the player would loop through all the available foods and then would visit
        the caves which would return the highest emerald return value for the given hunger bars to mine the material. The emerald 
        return value is calculated through (mining rate of material / trader's buying price). Initially in the trader class, each trader,
        after they generate a deal, have a variable called self.ratio, which is calculated through [mining rate of material sold by trader / trader's buying price].
        Then in select_food_and_caves, each trader is inserted into an avl tree using their self.ratio as they key. In the avl tree, the traders
        are arranged from having the lowest ratio to the largest ratio (as it is still a bst). Then we would now select the minimal value in the tree, 
        teh trader with the lowest ratio. This trader's material has the lowest mining rate to buying ratio. This means that we can get more emeralds mining 
        this material, but use up lower hungers bars in the mining process. This is all relative to the other materials and buying prices of traders. Then
        all the caves containing this material was plundered, until we run out of hunger bars and the materials mined is sold to the respective trader chosen at the start.
        This process of choosing a trader and mining the cave is repeated until the player runs out of hunger bars. After this point the final emerald balance (the highest possible) 
        from this material is compared to the overall highest possible emerald balance and if the emerald balance from this matrial is higher, then the food, the final emerald balance,
        and a list of all the caves plundered in this journey is stored. The cycle then moves onto the next possible food.

                                                     ---- EXAMPLE ----
        MATERIALS (MINING RATE):
        Gold (10)             Netherite (7)         Fishing Rod (4)        Ender Pearl (12)       Prismarine (2)

        CAVES
        Boulderfall                 Castle            Glacial         Orothheim                Red Eagle
        10 Prismarine              4 Nethherite       3 Gold          6 Fishing Rods         3 Fishing Rods

        TRADERS (BUYING PRICE)
        Waldo                             Orson             Lea                       Ruby                     Mable 
        Fishing Rod (7.57)              Gold (4.87)         Prismarine (5.65)        Netherite (8.54)        Gold (6.7)

        FOOD
        Fried Rice, 24 emeralds for 129 hunger bars,
        Cooked Chiken Cuts, 19 emeralds for 424 hunger bars.

                                                ---- EXPLANATION OF EXAMPLE ----
        Firstly, all the traders will be arranhged based on their (mining rate of material / trader's buying price) ratio in an avl tree.
        For the purpose of this explanation, the list below shows the ordering of the traders from low to high ratio:
        [Lea, Ruby, Waldo, Mable, Orson]
        Firstly, the program will chose Fried Rice and spend 24 emaralds and recieve 129 Hunger bars. The emerald BALANCE now is (50-24) = 26.
        Then the program selects Lea and finds out the material Lea is buying is Prismarine Crystal. The program then searchhes for the cave containing prismarine
        and finds out that the cave is Boulderfall. Upon visiting the cave, if the cave hasn't already been mined in respect to the current food, then the program
        checks if thhere is enough hunger balance to mine all the materials in this cave. Since there is, all the Prismarine in Boulderfall will be mined and sold to Lea, increasing
        the emerald Balance to 82.5. The player's hunger balance also reduces to around 14 as hunger bars were used to mine prismarine.
        Then the Program selects Ruby (2nd in list), and finds out that Ruby is buying Netherite. Then the program selects the cave containing neterite, in this case Castle and mines
        only 0.677 nethherite as the player can only mine that much with the amount of present hunger bars. The player then sellss the mined netherite to Ruby and increases his emerald balance to 88.7.
        Since this is theh first food tested, this emerald balance is stored as the final emerald balnce (to be returned in a tuple), 
        this food is stored as the final food (to be returned in a tuple). And all the caves this player pundred just now and the quantity they mined is stored as a list and set as theh final list(to be returned in a tuple).

        THIS procedure then continues with Cooked CChicken Cuts.
        At the end of the loop for cooked chicken cuts (when the player runs out of hunger), it is found tha tthe total emerald balance is aroung 185. Since this emerald balance is higher than the 
        balance from Fried Rice, this emerald balance is stored as the final emerald balance. Thsi food is stored as teh final food, and this caves plundered list is stored as the final lits. 
        This will be returned as a form of a tuple in the end.

        
                
                                                ---- COMPLEXITY ----
        Complexity worst case = best case: O(T * log(t) + F * (log(t) * log(C) * C1))
        where T is Traders, F is Food, C is Caves and C1 is a a special case where more than one cave has the same material in them.
        The Complexity provided here is less than that of the one given as this complexity does not take into account M. 
        We beleive that it is more than highly likely for M to be around the same as T (+-100). In this assumption, t*log(t) will have a lower time complexity
        compared to M + T if M and T are around the same values (+-100).
        '''
        trader_ratio = AVLTree()

        hunger_bars_balance = 0
        emerald_balance = 0
        caves_plundered_list = None
        final_emerald_balance = 0
        final_food = None

        for trader in self.traders:                     # O(T * log(t)), T is the number of traders, t is the amount of traders in the AVL tree
                try:
                    trader_ratio[trader.ratio] = trader        # O(height of tree) = O(log(traders in tree))
                except:
                    continue
        
        for food in self.foods: #O(F)
            caves_plundered_elements = []
            emerald_balance = self.balance - food.price
            hunger_bars_balance = food.hunger_bars
            count = 0

            while hunger_bars_balance > 0: #O(1)#O(1)
                try:
                    trader_to_sell = trader_ratio.range_between(count, count)   # O(log(t))
                except:
                    break
                try:
                    material_to_mine = trader_to_sell[0].material #Get Material to mine #O(1)
                except IndexError:
                    break

                try:
                    cave_to_mine = self.caves[material_to_mine.mining_rate] #Found Cave O(log(C))
                except KeyError: #No cave containing given material
                    count += 1 #O(1)
                    continue
                if type(cave_to_mine) == list:  
                    for cave in cave_to_mine:               #O(C1) Special case where two caves have the same material
                        if hunger_bars_balance > 0: #O(1)
                            if cave.if_visited(food): #O(1)
                                continue

                            quantity_mined = hunger_bars_balance / cave.material.mining_rate        # #O(1)
                            if quantity_mined > cave.quantity:
                                quantity_mined = cave.quantity
                            
                            caves_plundered_elements.append((cave, quantity_mined))
                            
                            hunger_bars_balance = hunger_bars_balance - cave.material.mining_rate * quantity_mined      #O(1)
                            emerald_balance += quantity_mined * trader_to_sell[0].buying_price          #O(1) we already know the position to index
                        else:
                            break

                else:
                    if cave_to_mine.if_visited(food): #O(1)
                        count += 1
                        continue
                                        
                    quantity_mined = hunger_bars_balance / cave_to_mine.material.mining_rate        #O(1)
                    if quantity_mined > cave_to_mine.quantity:
                        quantity_mined = cave_to_mine.quantity          #O(1)

                    caves_plundered_elements.append((cave_to_mine, quantity_mined))
                    
                    hunger_bars_balance = hunger_bars_balance - cave_to_mine.material.mining_rate * quantity_mined      #O(1)
                    emerald_balance += quantity_mined * trader_to_sell[0].buying_price      #O(1)

                
                count += 1
            if emerald_balance > self.balance: #O(1)
                if emerald_balance > final_emerald_balance: #O(1)
                    final_emerald_balance = emerald_balance #O(1)
                    final_food = food #O(1)
                    caves_plundered_list = caves_plundered_elements #O(1)
            else:
                if final_emerald_balance > self.balance: #O(1)
                    continue
                else:
                    final_food = None #O(1)
                    final_emerald_balance = self.balance #O(1)
                    caves_plundered_list = [] #O(1)

        

        return (final_food, final_emerald_balance, caves_plundered_list)
                
    def __str__(self) -> str:
        return f"Name: {self.name}, Emeralds: {self.balance}"

if __name__ == "__main__":
    print(Player("Steve"))
    print(Player("Alex", emeralds=1000))
