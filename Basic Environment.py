import random, math


class Device:
    def travel(self, loc): pass
    def detect(self, loc): pass
    x, y = 0, 0


class Drone(Device):
    efficiency = 50                                             # miles per hour
    accuracy = .751                                             # percent CV analysis accuracy
    GSD = 0                                                     # Smallest Visible Object (cm^2)
    x, y = 0, 0                                                 # miles

    def _init_(self):
        pass

    def set_height(self, height):
        table = {150: 1.25 * 1.25, 200: 1.67 * 1.67,
                 250: 2.09 * 2.09, 300: 2.51 * 2.51,
                 350: 2.93 * 2.93, 400: 3.34 * 3.34}        # feet(altitude): minimum object visible(cm^2)

        self.GSD = table[height]

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def travel(self, loc):
        return math.sqrt(math.pow(loc.x - self.x, 2) + math.pow(loc.y - self.y, 2)) / self.efficiency

    def detect(self, loc):
        if loc.size < self.GSD:
            if random.random() < self.accuracy:
                return loc.isEmpty()
        return False


class Rover(Device):
    efficiency = (28.06/1094) / (1/24)                           # miles per hour
    accuracy = .929                                              # percent CV analysis accuracy
    x, y = 0, 0                                                  # miles

    def _init_(self):
        pass

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def travel(self, loc):
        return math.sqrt( math.pow(loc.x-self.x, 2) + math.pow(loc.y-self.y, 2) ) / self.efficiency

    def detect(self, loc):
        if random.random() < self.accuracy:
            return loc.isEmpty()
        return False


class Location:
    size = 50
    abundance = 85 / 1065
    anomaly = False
    x, y = 0, 0

    def _init_(self, x, y):
        if random.random() < self.abundance:
            anomaly = True

    def isEmpty(self):
        return self.anomaly


class DRCS:
    d = Drone()
    r = Rover()

    def _init_(self, height):
        self.d.set_height(height)

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def travel(self, loc):
        return math.sqrt( math.pow(loc.x-self.x, 2) + math.pow(loc.y-self.y, 2) ) / self.efficiency
