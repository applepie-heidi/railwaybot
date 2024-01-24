import json


class City:
    def __init__(self, name):
        self.name = name
        self.railways = []

    def __str__(self):
        city_str = self.name + "\n"
        for railway in self.railways:
            city_str += "  " + str(railway) + "\n"
        return city_str

    def add_railway(self, railway):
        self.railways.append(railway)

    def get_unclaimed_railway(self, destination, color=None):
        temp = [self.name, destination]
        temp.sort()

        if color:
            for railway in self.railways:
                if (railway.city1 == temp[0] and railway.city2 == temp[1]
                        and railway.color == color and not railway.claimed):
                    return railway
        else:
            for railway in self.railways:
                if railway.city1 == temp[0] and railway.city2 == temp[1] and not railway.claimed:
                    return railway


class Railway:
    def __init__(self, city1, city2, length, color):
        self.city1 = city1
        self.city2 = city2
        self.length = length
        self.color = color
        self.claimed = False

    def __str__(self):
        return self.city1.name + " - " + self.city2.name + " (" + str(self.length) + ", " + self.color + ")"


class Board:
    def __init__(self, filename):
        self.board = {}
        self.__make(filename)

    def __str__(self):
        board_str = ""
        for city in self.board:
            board_str += str(self.board[city]) + "\n"
        return board_str

    def __make(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            for city_data in data["cities"]:
                name = city_data["name"]
                self.add_city(name)
            for railway_data in data["railways"]:
                city1 = self.get_city(railway_data["city1"])
                city2 = self.get_city(railway_data["city2"])
                railway = Railway(city1, city2, railway_data["length"], railway_data["color"])
                city1.add_railway(railway)
                city2.add_railway(railway)

    def add_city(self, name):
        city = City(name)
        self.board[name] = city

    def get_city(self, name):
        return self.board[name]


if __name__ == '__main__':
    board = Board("data/jsons/board.json")
    print(board)
