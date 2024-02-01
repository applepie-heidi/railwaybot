import json

'''
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

'''


class Railway:
    def __init__(self, city1, city2, length, color):
        self.city1 = city1
        self.city2 = city2
        self.length = length
        self.color = color
        self.claimed = False

    def __str__(self):
        return self.city1 + " - " + self.city2 + " (" + str(self.length) + ", " + self.color + ")"


class Board:
    def __init__(self, path):
        self.cities = []
        self.all_railways = []
        self.__make(path)

    def __str__(self):
        board_str = ""
        for city in self.cities:
            board_str += city + "\n"
        return board_str

    def __make(self, path):
        with open(path, "r") as f:
            data = json.load(f)
            for city_data in data["cities"]:
                name = city_data["name"]
                self.add_city(name)
            for railway_data in data["railways"]:
                city1 = railway_data["city1"]
                city2 = railway_data["city2"]
                length = railway_data["length"]
                color = railway_data["color"]
                railway = Railway(city1, city2, length, color)
                self.all_railways.append(railway)

    def add_city(self, name):
        self.cities.append(name)

    def get_railways(self, city1, city2):
        temp = [city1, city2]
        temp.sort()
        railways = []
        for railway in self.all_railways:
            if railway.city1 == temp[0] and railway.city2 == temp[1]:
                railways.append(railway)
        return railways

    def get_unclaimed_railway(self, city1, city2, color):
        temp = [city1, city2]
        temp.sort()
        for railway in self.all_railways:
            if (railway.city1 == temp[0] and railway.city2 == temp[1]
                    and railway.color == color and not railway.claimed):
                return railway
        return None


if __name__ == '__main__':
    board = Board("data/jsons/board.json")
    print(board)
