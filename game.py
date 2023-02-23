from __future__ import annotations
from constants import EPSILON

from player import Player
from trader import Trader
from material import Material
from cave import Cave
from food import *
from random_gen import RandomGen
from aset import *
from hash_table import *
from avl import *

class Game:
    """
    Game class simulates a game. The game class contains the Food, Trader, Cave, Material, Player objects for the game to run.
    This is a parent class for Sologame and MultiplayerGame 
    """

    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5

    def __init__(self) -> None:
        """
        Intialises variables that we will be using later in the class methods.
        """
        self.materials = []
        self.caves = []
        self.traders = []
        self.material_check = ASet(100)
        self.material_check2 = ASet(100)
        self.cave_check = ASet(100)
        self.trader_check = ASet(100)

    def initialise_game(self) -> None:
        """
        Initialise all game objects: Materials, Caves, Traders with random inputs.
        Best and worst case complexity: O(M + C + T)
        """
        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        print("Materials:\n\t", end="")
        print("\n\t".join(map(str, self.get_materials())))
        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        print("Caves:\n\t", end="")
        print("\n\t".join(map(str, self.get_caves())))
        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        print("Traders:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]):
        """
        Intialises all game objects: Materials, Caves, Traders with GIVEN inputs.
        Best and worst case complexity: O(1)
        """
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)

    def set_materials(self, mats: list[Material]) -> None:
        """
        Intialises materials via a given list of materials.
        Best and worst case complexity: O(1)
        """
        self.materials = mats

    def set_caves(self, caves: list[Cave]) -> None:
        """
        Intialises caves via a given list of caves.
        Best and worst case complexity: O(1)
        """
        self.caves  = caves

    def set_traders(self, traders: list[Trader]) -> None:
        """
        Intialises traders via a given list of traders.
        Best and worst case complexity: O(1)
        """
        self.traders = traders

    def get_materials(self) -> list[Material]:
        """
        Return all of the materials in a list.
        Best and worst case complexity: O(1)
        """
        return self.materials

    def get_caves(self) -> list[Cave]:
        """
        Return all of the caves in a list.
        Best and worst case complexity: O(1)
        """
        return self.caves

    def get_traders(self) -> list[Trader]:
        """
        Return all of the traders in a list.
        Best and worst case complexity: O(1)
        """
        return self.traders

    def generate_random_materials(self, amount):
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)

        Best and worst case complexity: O(M + A*M1*M1)
        """
        for material in self.materials:
            self.material_check.add(material.mining_rate)
            self.material_check2.add(material.name)

        mat_amount = 0
        while mat_amount < amount: 
            mat = Material.random_material()

            if mat.mining_rate not in self.material_check and mat.name not in self.material_check2:
                self.material_check.add(mat.mining_rate)
                self.material_check2.add(mat.name)
                self.materials.append(mat)
                mat_amount += 1

    def generate_random_caves(self, amount):
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)

        Best and worst case complexity: O(C + A*C1)
        """
        for cave in self.caves:
            self.cave_check.add(cave.name)
        
        cave_amount = 0
        while cave_amount < amount:
            cave = Cave.random_cave(self.materials)

            if cave.name not in self.cave_check: 
                self.cave_check.add(cave.name)
                self.caves.append(cave)
                cave_amount +=1

    def generate_random_traders(self, amount):
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)

        Best and worst case complexity: O(T) + A * T1)
        """
        for trader in self.traders:
            self.trader_check.add(trader.name)
        
        trader_amount = 0
        while trader_amount < amount: 
            trader = Trader.random_trader()
            trader.set_all_materials(self.materials)

            if trader.name not in self.trader_check:
                self.trader_check.add(trader.name)
                self.traders.append(trader)
                trader_amount += 1


    def finish_day(self):
        """
        DO NOT CHANGE
        Affects test results.
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)

class SoloGame(Game):
    """
    SoloGame runs the game intended for a single player. During a day, the player will choose the food to eat, cave to mine and the repesctive trader to trade with.
    """

    def initialise_game(self) -> None:
        """
        Initialise all game objects: Materials, Caves, Traders with random inputs.
        Best and Worst case complexity: O(1)
        """
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        """
        Initialise all game objects: Materials, Caves, Traders with GIVEN inputs.
        Best and Worst case complexity: O(1)
        """
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def simulate_day(self):
        """
        Simulates a full day of the game. 
        Best and Worst case complexity: O(T + F + O(select_food_and_caves) + C * T), select_food_and_caves = O(T * log(t) + F * (log(t) * log(C) * C1)))
        """
        # 1. Traders make deals
        for trader in self.traders:
            trader.generate_deal()
        # raise NotImplementedError()
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD)
        foods = []
        for _ in range(food_num):
            foods.append(Food.random_food())
        print("\nFoods:\n\t", end="")
        print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)
        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()      # O(T * log(t) + F * (log(t) * log(C) * C))
        print(food, balance, caves)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)

    def verify_output_and_update_quantities(self, food: Food | None, balance: float, caves: list[tuple[Cave, float]]) -> None:
        '''
        This method ehcks if the resulyts of select_food_and_caves that is passed in is accurate and achievable first.
        Then the quantities within each cave is updated and the final playerr emerald balance is updated. 
        Best and Worst case complexity: (O(C*T)) where C is the number of Caves and T is teh number of Traders.
        '''
        player = self.player
        check_balance = player.balance - food.price
        buying_price = 0
        if food in player.foods:
            for item in caves:
                cave = item[0]
                quantity = item[1]
                if cave.material.mining_rate in player.caves:
                    if quantity <= cave.quantity: 
                        for trader in player.traders:
                            if trader.material.name == cave.material.name:
                                if trader.buying_price > buying_price:
                                    buying_price = trader.buying_price
                        if buying_price == 0:
                            raise ValueError('No Trader buying Mined Material')
                        check_balance += quantity * buying_price
                        buying_price = 0   
                        continue
                    else:
                        raise ValueError('Incorrect Cave Quantity Mined')
                else:
                    raise ValueError("Cave Mined not part of Player's Caves")
        else:
            raise ValueError('Food not available to Player.')

        if abs(balance - check_balance) <= EPSILON:
            player.balance = balance  
            for item in caves:
                cave = item[0]
                quantity = item[1]

                cave.remove_quantity(quantity)
                print(f'Quantity within {cave.name} is updated.')
        else:
            raise ValueError('Balance returned is incorrect')




class MultiplayerGame(Game):
    """
    MultiplayerGame is a game intended to have multiple players. 
    Each day, only 1 food choice will be offered. Cave, traders and materials will all have multiple options that the player can chosoe from
    """

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        super().__init__()
        self.players = []

    def initialise_game(self) -> None:
        """
        Initialise all game objects: Materials, Caves, Traders with random inputs.
        Best and worst case complexity: O(P)
        """
        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players:
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def generate_random_players(self, amount) -> None:
        """
        Generate <amount> random players. Don't need anything unique, but you can do so if you'd like.
        Best and worst case complexity: O(1)
        """

        for _ in range(amount):
            self.players.append(Player.random_player())
       


    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        """
        Initialise all game objects: Materials, Caves, Traders with GIVEN inputs.
        Best and worst case complexity: O(P)
        """
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def simulate_day(self):
        """
        Simulates a full day for the multiplayer version of the game.
        Best and worst case complexity: O(T + O(select_for_players)), O(select_for_players) = O(T + C + P * log(C))
        COMPLEXITY NOT RIGHT. NEED TO DO VERIFY_OUTPUT COMPLEXITY
        """
        # 1. Traders make deals
        for trader in self.traders:
            trader.generate_deal()
        # raise NotImplementedError()
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        offered_food = Food.random_food()
        print(f"\nFoods:\n\t{offered_food}")
        # 3. Each player selects a cave - The game does this instead.
        foods, balances, caves = self.select_for_players(offered_food)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)

    def select_for_players(self, food: Food) -> tuple[list[Food|None], list[float], list[tuple[Cave, float]|None]]:
        """
                                              ---- PROCESS EXPLANATION -----
        select_for_players' overall process idea was that the player would visit the cave that would yield the most emerald value. 
        Emerald value being calculated as "No. materials mined * Trader's buying price of material". Note that we could not have 
        gone with a comparison between the ratios of efficiency (how much hunger needed to use for 1 emerald) between the caves 
        as the amount of remaining mateiral needed to be accounted for. Such as if the most efficient cave only had 1 material left 
        vs. less efficient cave with full materials and we had a large amount of hunger, would would rather visit the less efficient 
        cave to achieve more overall emeralds. Hence for each cave, we would need to access the material that was in the cave 
        (to find the trader buying price), the quantity in the cave (to ensure we are not mining more than available) and the buying 
        price of the trader offering to buy the material (to calculate the cave value). After we've calculated the value of each cave, 
        we can just have the players visit the caves in the order of highest emerald value to lowest, ensuring that AFTER materials 
        are mined that the emerald value of the cave is UPDATED. This ensures that the cave is always in order of highest value to lowest 
        value. 
        
        To accomplish this our code process was: 
              (-) Sort the traders by material to search up the price of the material.
              (-) Calculate the emerald value for the caves that hold materials that traders are willing to buy.
              (-) Loop through all of the players with the following processes: 
                       (-) Have the player buy food if possible, if not append the relevant information to the return tuple and go back to 
                           start of loop.
                       (-) Have the current player to visit the cave with the highest emerald value and mine as much as possible. Ensuring 
                           that the quantity minded > quantity in cave.
                       (-) Append the relevant information (food purchased, emeralds, caves and mateirals) to the return tuple 
                       (-) Update the material quantity in the cave



                                                     ---- EXAMPLE ----
        MATERIALS (HUNGER/EMERALDS):
        Apple (10)             Banana (7)         Chocolate (4)        Donuts (12)       Eggplant (2)

        CAVES
        Amazon                 Blueski            Chocothunder         Dukenuts          Eggstra
        15 Apples              9 Bananas          6 Chocolates         12 Donuts         20 Eggplants

        TRADERS (BUYING PRICE)
        Astra                  Bicker             Charles              Daniel            Ella 
        Apple (4)              Banana (5)         Chocolate (6)        Donuts (5)        Eggplant (2)

        FOOD
        Raw chicken, 15 emeralds for 60 hunger 

        PLAYERS (Order: left to right)                    
        Ziheng: $40          Anuk: $13         Harshath: $37        Vincent: $39
            
        
                                               ---- EXPLANATION OF EXAMPLE ----
        Firstly Ziheng, Vincent and Harshath will buy food as they are able to buy food so they will do so. Anuk is unable to purchase food. His return tuple will 
        be None with food and caves and materials, but his emeralds will be his current balance of $13, not $0. This means that only Ziheng and Harshath 
        will continue to go mining. To know where Ziheng will choose to go, we will now calculate the emerald value of each cave taking into account how
        much hunger there is to be used up:

                                                                  "Cave name" 
                                 "Quantity can mine with hunger, quantity can mine in cave, calculated cave value"

                 Amazon                       Blueski                         Chocothunder                  Dukenuts                         Eggstra
         Q=60/10=6, 6, 6*4=$24   Q=60/7=8.57, 8.57, 8.57*5=$42.86        Q=60/4=15, 6, 6*6=$36        Q=60/12=5, 5, 5*5=$25          Q=60/2=30, 20, 20*4=$40   

        Now we can see that the Blueski has the highest cave value and hence the first player, Ziheng will travel to Blueski and mine as much as possible with 
        his 60 hunger. He is able to mine 8.57143... Bananas. Each Banana can be sold for $5 and hence his emerald balance would be 8.574143*5+(40-15) = 67.86. 
        Calculated by Emerald balance = Quantity minded*selling price + (intial emerald balance - cost of food). We would now need to update the quantity and 
        thus the emerald value in that cave before the next palyer.

                 Amazon                       Blueski                         Chocothunder                  Dukenuts                         Eggstra
         Q=60/10=6, 6, 6*4=$24        Q=60/7=8.57, 0, 0*5=$0              Q=60/4=15, 6, 6*6=$36       Q=60/12=5, 5, 5*5=$25           Q=60/2=30, 20, 20*2=$40  

        Next Harshath will go to the cave with the now highest value (after the quantity for Blueski has been updated after Ziheng, it is no longer the most valuable).
        Harshath will travel to Eggstra and mine 20 Eggplants even though he has the hunger to mine 30, as the cave only contains 20 eggplants. He is able to sell these 
        at $2 an eggplant yielding him $40. His balance would be 20*2+(37-15) = $62. Update the quantity in Eggstra.

                 Amazon                       Blueski                        Chocothunder                  Dukenuts                         Eggstra
         Q=60/10=6, 6, 6*4=$24        Q=60/7=8.57, 0, 0*5=$0           Q=60/4=15, 6, 6*6=$36         Q=60/12=5, 5, 5*5=$25           Q=60/2=30, 10, 10*2=$20

        Vincent will go to the cave that yields the most emeralds. It is no longer Eggstra after Harshath has been to it. Vincent will travel to Chocothunder. There he will 
        mine 6 Chocolates will a selling price of $9 each. Thus his balance would be 6*6+(39-15) = $60. Update the quantity in Chocothunder.

        Thus at the end of the day, the players balances will now be: 
        Ziheng: 67.86... emeralds
        Harshath: 62 emeralds
        Anuk: 13 emeralds
        Vincent: 60 emeralds 


        worst case: O(T + C * log(C) + P * 2 log(C))
        best case: O(T + C * log(C) + P), when everyone cant afford food 
        
        """
        food_purchased_list = []
        caves_and_materials_list = []
        emerald_balance_list = []
        default_hunger = food.hunger_bars

        #Sorting traders by material to access later + price 
        trader_info = LinearProbeTable(len(self.traders))   
        for trader in self.traders:                         #O(T)
            if trader.material.name in trader_info:           # O(1)
                if trader.buying_price > trader_info[trader.material.name]:     #O(1)
                    trader_info[trader.material.name] = trader.buying_price     #O(1)
            else:
                trader_info[trader.material.name] = trader.buying_price            #O(1)
        self.trader_table = trader_info
        #Sorting cave by material, sorting by emerald value 
        cave_avl = AVLTreeCave()
        for cave in self.caves:         #O(C)
            try:
                if cave.material.name in trader_info:           #O(1)

                    selling_price = trader_info[cave.material.name]     #O(1)
                    cave_emerald_value = selling_price * (default_hunger/cave.material.mining_rate) * cave.quantity     #O(1)
                    cave_avl[cave_emerald_value] = cave         #O(log(C))
            except ZeroDivisionError:
                continue
            
        #Loop through all the players
        for i in range(len(self.players)):              #O(P)
            current_player = self.players[i]            #O(1)
            if current_player.balance >= food.price:        #O(1)
                #Buys food item
                current_player.balance -= food.price        #O(1)
                food_purchased_list.append(food)            #O(1)
                current_hunger = food.hunger_bars           #O(1)

                #Visit cave of maximum
                current_cave = cave_avl.get_maximum(cave_avl.root)      #O(log(C))
                #Find material
                if type(current_cave.item) == list:  
                    for cave in current_cave.item:               #O(1) because it breaks after 1 iteration
                        current_material = cave.material           #O(1)
                        #Find how much materials mined 
                        quantity_mined = (float(current_hunger) / current_material.mining_rate)      #O(1)

                        if quantity_mined > cave.quantity:          #O(1)
                            quantity_mined = cave.quantity          #O(1)

                        #Append to return
                        caves_and_materials_list.append([cave, quantity_mined])            #O(1)

                        #Append to return
                        selling_price = trader_info[current_material.name]          #O(1)
                        emerald_balance_list.append(current_player.balance + selling_price * quantity_mined)           #O(1)

                        #Update items in current_cave 
                        cave.quantity -= quantity_mined #For next player to know if the cave has like 20% of its mats left = bad choice 
                        
                        current_cave.item.pop(0)    #O(1) because always popping at the first position
                        if len(current_cave.item) == 0:
                            del cave_avl[current_cave.key]

                        cave_emerald_value = selling_price * (default_hunger/cave.material.mining_rate) * cave.quantity     #O(1)
                        cave_avl[cave_emerald_value] = cave 
                        
                        break
                    continue
                else:
                    current_material = current_cave.item.material       #O(1)

                    #Find how much materials mined 
                    quantity_mined = current_hunger / current_cave.item.material.mining_rate        #O(1)
                    if quantity_mined > current_cave.item.quantity:         #O(1)
                        quantity_mined = current_cave.item.quantity         #O(1)

                    #Append to return
                    caves_and_materials_list.append([current_cave.item, quantity_mined])       #O(1)

                    #Append to return
                    selling_price = trader_info[current_material.name]          #O(1)
                    emerald_balance_list.append(current_player.balance + selling_price * quantity_mined)           #O(1)

                    #Update items in current_cave 
                    current_cave.item.quantity -= quantity_mined #For next player to know if the cave has like 20% of its mats left = bad choice 
                    del cave_avl[current_cave.key]
                    cave_emerald_value = selling_price * (default_hunger/current_cave.item.material.mining_rate) * current_cave.item.quantity     #O(1)
                    cave_avl[cave_emerald_value] = current_cave.item 
            else: #Cannot buy food item, no cave, no increase in emeralds 
                food_purchased_list.append(None)            #O(1)       
                emerald_balance_list.append(current_player.balance)         #O(1)
                caves_and_materials_list.append([(None, 0)])                #O(1)

        return (food_purchased_list, emerald_balance_list, caves_and_materials_list)

    def verify_output_and_update_quantities(self, foods: list[Food | None], balances: list[float], caves: list[tuple[Cave, float]|None]) -> None:
        """
        Verifies that the result of select_food_and_caves holds valid results. That is, the quantities are in line with what the player provided, 
        the food is purchaseable and that the remaining balance is correct.
        best and worst case is O(P) where P is the amount of players
        """

        for i in range(len(self.players)):  # iterating thru each person
            if foods[i] is not None:
                if type(foods[i]) != Food:
                    raise TypeError ("food isn't a food class")
                quantity_mined = caves[i][1]
                material_mined = caves[i][0].material    # the test case has the cave as a string

                trader_buying_price = self.trader_table[material_mined.name]
                money_earned = quantity_mined * trader_buying_price
                if abs(self.players[i].balance - (balances[i] - money_earned)) > EPSILON:
                    raise ValueError ("their initial balance should equal final balance - money earned")
                else:
                    self.players[i].balance += money_earned




                

            



if __name__ == "__main__":

    r = RandomGen.seed # Change this to set a fixed seed.
    r= 1234567
    RandomGen.set_seed(r)
    print(r)

    g = SoloGame()
    g.initialise_game()

    g.simulate_day()
    g.finish_day()

    g.simulate_day()
    g.finish_day()
