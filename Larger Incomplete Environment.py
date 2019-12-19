import random, math


class Device:
    def travel(self): pass
    def detect(self): pass
    x, y = 0, 0


class Drone(Device):
    efficiency = 1200000                                        # cm per day (Assuming half-day to recharge)
    accuracy = .751                                             # percent CV analysis accuracy
    GSD = 0                                                     # Smallest Visible Object (cm^2)
    x, y = 0, 0                                                 # centimeters
    visible_radius = 9144                                       # centimeters

    destination = None
    delta_x, delta_y = 0.0, 0.0

    def __init__(self, height, target):
        self.set_destination(target)
        self.set_height(height)

    def set_height(self, height):
        table = {150: 1.25 * 1.25, 200: 1.67 * 1.67,
                 250: 2.09 * 2.09, 300: 2.51 * 2.51,
                 350: 2.93 * 2.93, 400: 3.34 * 3.34}        # feet(altitude): minimum object visible(cm^2)

        self.GSD = table[height]

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def set_destination(self, loc):
        self.destination = loc
        self.delta_x, self.delta_y = self.destination.x - self.x, self.destination.y - self.y

    def travel(self):                                 # Travel one Day
        self.x += self.efficiency * math.cos(math.atan(self.delta_y / self.delta_x))
        self.y += self.efficiency * math.sin(math.atan(self.delta_y / self.delta_x))

        location, anomaly_found = self.detect()
        if anomaly_found:
            print("Found Anomaly at (" + location.x + ", " + location.y + ")")

    def detect(self):
        for r in range(0, self.visible_radius):
            for c in range(0, self.visible_radius):
                if positions[self.x + r][self.x + c].size < self.GSD:
                    if random.random() < self.accuracy:
                        return positions[r][c], positions[r][c].isEmpty()
                if positions[self.x - r][self.x - c].size < self.GSD:
                    if random.random() < self.accuracy:
                        return positions[r][c], positions[r][c].isEmpty()
        return None, False


class Rover(Device):
    efficiency = 3600                                           # cm per day (Assuming a generous 1 hr movement per day)
    accuracy = .929                                             # percent CV analysis accuracy
    x, y = 0, 0                                                 # cm
    visible_radius = 9144                                       # centimeters

    destination = None
    delta_x, delta_y = 0.0, 0.0

    def __init__(self, target):
        self.set_destination(target)

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def set_destination(self, loc):
        self.destination = loc
        self.delta_x, self.delta_y = self.destination.x - self.x, self.destination.y - self.y

    def travel(self):                                 # Travel one Day
        self.x += self.efficiency * math.cos(math.atan(self.delta_y / self.delta_x))
        self.y += self.efficiency * math.sin(math.atan(self.delta_y / self.delta_x))

        location, anomaly_found = self.detect()
        if anomaly_found:
            print("Found Anomaly at (" + location.x + ", " + location.y + ")")

    def detect(self):
        for r in range(0, self.visible_radius):
            for c in range(0, self.visible_radius):
                if random.random() < self.accuracy:
                    return positions[r][c], positions[r][c].isEmpty()
                if random.random() < self.accuracy:
                    return positions[r][c], positions[r][c].isEmpty()
        return None, False


class Location:
    size = 26*26                                            # square cm
    # Note: Table of rock's size : distributions would be useful
    abundance = 85 / 1065
    anomaly = False
    x, y = 0, 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        if random.random() < self.abundance:
            anomaly = True

    def isEmpty(self):
        return self.anomaly


w, h = 14912.88, 14912.88                                                                    # meters by meters
actual_anomalies = 0
positions = [[Location(a, b) for a in range(0, w)] for b in range(0, h)]

loc = Location(w, h)
d = Drone(300, loc)
simulation_t = 31 * 60                                           # 1 month in days
for a in range(0, simulation_t):
    d.travel()

r = Rover(loc)
for a in range(0, simulation_t):
    r.travel()

