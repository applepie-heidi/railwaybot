import json
import random

from board import Board

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

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def add_destination_card(self, card):
        self.destination_cards.append(card)

    def remove_destination_card(self, card):
        self.destination_cards.remove(card)

    def add_points(self, points):
        self.points += points

    def remove_points(self, points):
        self.points -= points

    def remove_trains(self, trains):
        self.trains -= trains


class Game:
    def __init__(self, board_filename, destination_cards_filename, train_cards_filename, scoring_filename):
        self.game_started = False
        self.game_over = False
        self.board = Board(board_filename)
        self.players = []
        self.turn = 0
        self.round = 0
        self.destination_cards = []
        self.cards = []
        self.face_up_cards = []
        self.discarded_cards = []
        self.scoring = {}
        self.longest_continuous_path_points = 0
        self.__make(destination_cards_filename, train_cards_filename, scoring_filename)

    def __str__(self):
        game_str = "Turn: " + str(self.turn) + "\n"
        game_str += "Round: " + str(self.round) + "\n"
        game_str += "Players:\n"
        for player in self.players:
            game_str += str(player) + "\n"
        return game_str

    def __make(self, destination_cards_filename, train_cards_filename):
        with open(destination_cards_filename, "r") as f:
            data = json.load(f)
            for card in data:
                destination_card = DestinationCard(card["city1"], card["city2"], card["points"])
                self.destination_cards.append(destination_card)
            random.shuffle(self.destination_cards)

        with open(train_cards_filename, "r") as f:
            data = json.load(f)
            for card in data:
                for i in range(card["quantity"]):
                    self.cards.append(card["color"])
            random.shuffle(self.cards)

        with open("scoring.json", "r") as f:
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
        player.claimed_railways.append(railway)
        railway.claimed = True
        for card in cards:
            player.remove_card(card)
            self.discarded_cards.append(card)
        if len(self.players) <= 3:
            railway = self.board.get_city(city1).get_unclaimed_railway(city1, city2)
            railway.claimed = True

