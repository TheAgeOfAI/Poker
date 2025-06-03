import random
from typing import Dict, List


class Player:
    def __init__(self, name: str, money: int) -> None:
        self.name: str = name
        self.amount: int = money

    def add_amount(self, money: int) -> None:
        self.amount += money

    def remove_amount(self, money: int) -> None:
        self.amount -= money


class PlayerClass:
    def __init__(self, noof_players):
        self.noof_players: int = noof_players
        self.players: Dict[int, Player] = {}

    def initialize_players(self) -> None:
        for i in range(self.noof_players):
            self.players[i] = self.get_player_details(i)

    @staticmethod
    def get_player_details(player_number: int) -> Player:
        name: str = input(f"Enter Player - {player_number + 1} name : ")
        amount: int = random.randint(100,150)
        return Player(name, amount)
    
    def add_player(self):
        self.players[self.noof_players] = self.get_player_details(self.noof_players)
        self.noof_players += 1

    def del_player(self, player_id: int):
        if player_id in self.players:
            for i in range(player_id, self.noof_players - 1):
                self.players[i] = self.players[i + 1]
            del self.players[self.noof_players - 1]
            self.noof_players -= 1

    def display_players(self):
        for i in range(self.noof_players):
            print(f"{i+1}. {self.players[i].name} - {self.players[i].amount}", end="\t|\t")
        print()

    def return_players(self):
        return [self.players[i] for i in range(self.noof_players)]

# class Round:
#     def __init__(self, dealer: int):
#         self.highest_bid = 0
#         self.active_players: Dict[int, List] = {}
#         # this dictionary contains player bid, and player visited status
#         self.current_dealer: int = dealer
#
#     def next_current_dealer(self) -> None:
#         while True:
#             self.current_dealer = (self.current_dealer + 1) % len(self.active_players.keys())
#             if self.current_dealer in self.active_players:
#                 break
#
#             if len(self.active_players.keys()) == 1:
#                 self.current_dealer = next(iter(self.active_players.keys()))
#                 break

class RoundPlayer:
    def __init__(self, idx, name, amount):
        self.player_id = idx
        self.player_name = name
        self.available_amount = amount
        self.bid_amount = 0
        self.is_active = True
        self.visited = False

    def set_active_status(self, status):
        self.is_active = status

    def set_visited_status(self, status):
        self.visited = status

    def set_bid_amount(self, amount):
        self.bid_amount += amount

    def reset_bid(self):
        self.bid_amount = 0

    def set_amount(self, amount):
        self.available_amount += amount

class Street:

    def __init__(self, dealer):
        self.round_number = 1
        self.current_highest_bid = 0
        self.game_players = []
        self.dealer = dealer
        self.current_hand = dealer
        self.is_all_done = False
        self.pot_amount = 0

    def get_game_players(self, players):
        for i in range(len(players)):
            self.game_players.append(RoundPlayer(i, players[i].name,  players[i].amount))

    def print_players(self):
        for i in self.game_players:
            print(i.player_id + 1, i.player_name, i.available_amount)

    def river(self):
        self.round_one()
        self.reset_round_data()
        self.print_players()

        for i in range(3):
            if not self.is_all_done:
                self.round_all(i+2)
                self.reset_round_data()
                self.print_players()
        self.update_score()

    def round_one(self):
        self.current_hand = (self.dealer + 2) % len(self.game_players)
        for i in range(len(self.game_players)):
            print(f" Round 1 Player {self.current_hand + 1}  |")
            option = self.get_choice(self.game_players[self.current_hand].bid_amount > self.current_highest_bid)
            if option == 1:
                self.game_players[self.current_hand].set_active_status(False)
            elif option == 2:
                self.game_players[self.current_hand].set_bid_amount(self.current_highest_bid)
            else:
                raise_amount = int(input(f"Enter raise amount for player {self.current_hand + 1}: "))
                # raise_amount checks will be introduced later
                self.current_highest_bid = raise_amount
                self.game_players[self.current_hand].set_bid_amount(self.current_highest_bid)
            self.game_players[self.current_hand].set_visited_status(True)
            self.current_hand = (self.current_hand + 1) % len(self.game_players)

    def reset_round_data(self):
        temp = 0
        for i in self.game_players:
            temp += i.bid_amount
            i.set_amount(-i.bid_amount)
            i.reset_bid()
            i.set_visited_status(False)
        self.pot_amount += temp


    def round_all(self, round_number):
        self.current_hand = self.dealer
        for i in range(len(self.game_players)):
            print(f"Round {round_number} Player {self.current_hand + 1} ---|")
            option = self.get_choice(self.game_players[self.current_hand].bid_amount > self.current_highest_bid)
            if option == 1:
                self.game_players[self.current_hand].set_active_status(False)
            elif option == 2:
                self.game_players[self.current_hand].set_bid_amount(self.current_highest_bid)
            else:
                raise_amount = int(input(f"Enter raise amount for player {self.current_hand + 1}: "))
                # raise_amount checks will be introduced later
                self.current_highest_bid = raise_amount
                self.game_players[self.current_hand].set_bid_amount(self.current_highest_bid)
            self.game_players[self.current_hand].set_visited_status(True)
            self.current_hand = (self.current_hand + 1) % len(self.game_players)

        bids = [i.bid_amount for i in self.game_players]
        if len(set(bids)) > 1:
            self.round_all(round_number)

    def update_score(self):
        winner = int(input("Enter winner id: "))
        if winner in range(len(self.game_players)):
            self.game_players[winner].set_amount(self.pot_amount)

    @staticmethod
    def get_choice(has_raise):
        if has_raise:
            print(f"1. Fold | 2. Call | 3. Raise ")
        else:
            print(f"1. Fold | 2. Check | 3. Raise ")
        
        return int(input("Enter your choice : "))




class Game:

    @staticmethod
    def start_game():
        print("Do you want to start a new game with new players(Something(YES)/Nothing(NO)):")
        if input():
            n = int(input("Enter number of players you wanna play with : "))
            poker = PlayerClass(n)
            poker.initialize_players()
            poker.display_players()
            while True:
                print("Do you wanna modify players Y/N", end="")
                modification_choice = input()
                if modification_choice.upper() == "Y":
                    print("Do you wanna Add(A) or Delete(D) player: ", end="")
                    choice = input()
                    if choice.upper() == "A":
                        poker.add_player()
                    else:
                        print(f"Enter the player number you wanna delete: ", end="")
                        player_to_delete = int(input())
                        poker.del_player(player_to_delete - 1)
                        print(f"PLayer {player_to_delete} deleted successfully...")
                    poker.display_players()
                    continue

                street = Street(0)
                street.get_game_players(poker.return_players())
                # street.print_players()
                street.river()
                print("Round Done. Enter to continue playing or something else to exit.")
                if not input():
                    return
                break


if __name__ == "__main__":
    game = Game()
