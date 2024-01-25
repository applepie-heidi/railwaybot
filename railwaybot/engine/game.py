import json
import random

from .board import Board, Railway

CARDS_DRAW_INITIAL = 4
CARDS_DRAW = 2
DESTINATION_CARDS_DRAW = 3
CARDS_FACE_UP = 5
ANY_COLOR = "any"


class DestinationCard:
    def __init__(self, city1, city2, points):
        self.city1 = city1
        self.city2 = city2
        self.points = points

    def __str__(self):
        return self.city1 + " - " + self.city2 + " (" + str(self.points) + ")"


class Player:
    def __init__(self, color, trains):
        self.color = color
        self.cards = []
        self.destination_cards = []
        self.trains = trains
        self.claimed_railways = []
        self.points = 0
        self.won = False

    def __str__(self):
        player_str = self.color + "\n"
        player_str += "  Cards: " + str(self.cards) + "\n"
        player_str += "  Destination Cards: " + str(self.destination_cards) + "\n"
        player_str += "  Trains: " + str(self.trains) + "\n"
        player_str += "  Points: " + str(self.points) + "\n"
        return player_str

    def __repr__(self):
        player_str = self.color + "\n"
        player_str += "  Cards: " + str(self.cards) + "\n"
        player_str += "  Destination Cards: " + str(self.destination_cards) + "\n"
        player_str += "  Trains: " + str(self.trains) + "\n"
        player_str += "  Points: " + str(self.points) + "\n"
        return player_str

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def add_destination_card(self, card):
        self.destination_cards.append(card)

    def remove_destination_card(self, card):
        self.destination_cards.remove(card)

    def add_railway(self, railway):
        self.claimed_railways.append(railway)

    def add_points(self, points):
        self.points += points

    def remove_points(self, points):
        self.points -= points

    def remove_trains(self, trains):
        self.trains -= trains

    def route_exists(self, destination_card):
        city1 = destination_card.city1
        city2 = destination_card.city2

        visited = set()

        def dfs(current_city):
            if current_city == city2:
                return True
            visited.add(current_city)
            for railway in self.claimed_railways:
                if railway.city1 == current_city and railway.city2 not in visited:
                    if dfs(railway.city2):
                        return True
                elif railway.city2 == current_city and railway.city1 not in visited:
                    if dfs(railway.city1):
                        return True
            return False

        return dfs(city1)


class Game:
    def __init__(self, board_path, destination_cards_path, train_cards_path, scoring_path):
        self.started = False
        self.over = False
        self.board = Board(board_path)
        self.players = []
        self.turn = 0
        self.round = 0
        self.destination_cards = []
        self.cards = []
        self.face_up_cards = []
        self.discarded_cards = []
        self.scoring = {}
        self.longest_continuous_path_points = 0
        self.__make(destination_cards_path, train_cards_path, scoring_path)

    def __str__(self):
        game_str = "Turn: " + str(self.turn) + "\n"
        game_str += "Round: " + str(self.round) + "\n"
        game_str += "Players:\n"
        for player in self.players:
            game_str += str(player) + "\n"
        return game_str

    def __make(self, destination_cards_path, train_cards_path, scoring_path):
        with open(destination_cards_path, "r") as f:
            data = json.load(f)
            for card in data:
                destination_card = DestinationCard(card["city1"], card["city2"], card["points"])
                self.destination_cards.append(destination_card)
            random.shuffle(self.destination_cards)

        with open(train_cards_path, "r") as f:
            data = json.load(f)
            for card in data:
                for i in range(card["quantity"]):
                    self.cards.append(card["color"])
            random.shuffle(self.cards)

        with open(scoring_path, "r") as f:
            data = json.load(f)
            self.longest_continuous_path_points = data["longest_continuous_path"]
            for score in data["route_scoring"]:
                self.scoring[score["length"]] = score["points"]

    def add_player(self, player):
        self.players.append(player)

    def draw_destination_cards(self):
        cards = []
        for i in range(DESTINATION_CARDS_DRAW):
            cards.append(self.destination_cards.pop())
        return cards

    def discard_destination_cards(self, player, cards):
        for card in cards:
            player.remove_destination_card(card)
            self.destination_cards.insert(0, card)

    def draw_card(self, face_up_id=None):
        if len(self.cards) > 0:
            if face_up_id:
                card = self.face_up_cards.pop(face_up_id)
                self.turn_cards_face_up()
                return card
            else:
                return self.cards.pop()

    def turn_cards_face_up(self):
        while len(self.face_up_cards) < CARDS_FACE_UP:
            if len(self.cards) == 0:
                if len(self.discarded_cards) == 0:
                    return
                self.cards = self.discarded_cards
                self.discarded_cards = []
                random.shuffle(self.cards)
            self.face_up_cards.append(self.cards.pop())
        cards_dict = {i: self.face_up_cards.count(i) for i in self.face_up_cards}
        if ANY_COLOR in cards_dict:
            if cards_dict[ANY_COLOR] >= 3:
                self.face_up_cards.remove(ANY_COLOR)
                self.cards.append(ANY_COLOR)

    def claim_railway(self, player, city1, city2, color, cards):
        railway = self.board.get_city(city1).get_unclaimed_railway(city1, city2, color)
        player.remove_trains(railway.length)
        player.add_points(self.scoring[railway.length])
        player.add_railway(railway)
        railway.claimed = True
        for card in cards:
            player.remove_card(card)
            self.discarded_cards.append(card)
        if len(self.players) <= 3:
            railway = self.board.get_city(city1).get_unclaimed_railway(city1, city2)
            railway.claimed = True

    def final_scoring(self):
        for player in self.players:
            for destination_card in player.destination_cards:
                if player.route_exists(destination_card):
                    player.add_points(destination_card.points)
                else:
                    player.remove_points(destination_card.points)

    def play(self, player_path, num_players):
        self.set_up_game(player_path, num_players)
        self.started = True

    def set_up_game(self, player_colors, trains_per_player, num_players):
        for i in range(num_players):
            player = Player(player_colors[i], trains_per_player)
            self.add_player(player)
            for j in range(CARDS_DRAW_INITIAL):
                card = self.draw_card()
                player.add_card(card)
            destination_cards = self.draw_destination_cards()


if __name__ == '__main__':
    dc = DestinationCard("Vancouver", "Salt Lake City", 27)
    p = Player("red", 45)

    p.add_railway(Railway("Calgary", "Vancouver", 3, "red"))
    p.add_railway(Railway("Calgary", "Helena", 4, "red"))
    p.add_railway(Railway("Calgary", "Seattle", 4, "red"))
    p.add_railway(Railway("Seattle", "Vancouver", 1, "red"))
    p.add_railway(Railway("Portland", "Seattle", 1, "red"))
    p.add_railway(Railway("Salt Lake City", "San Francisco", 5, "red"))
    p.add_railway(Railway("Portland", "San Francisco", 5, "red"))

    print(p.route_exists(dc))
