
class physics:
    def __init__(self):
        self.g = 9.8
        self.timespeed = 0.001
        self.time = 0 #сделать время для кадого объекта уникальным
    def setGravConst(self, g):
        self.g = g
    def setTimeSpeed(self, speed):
        self.timespeed = speed
    def timeReset(self):
        self.time = 0
    def gravity(self, points):
        self.v0 = 0
        #v = v0 + g*t
        # s = v0t + g*t^2/2
        points2 = []
        for point in points:
            if (point[1] + self.v0 * self.time + (self.g*self.time**2)/2) < 1000:
                self.time += 1 * self.timespeed
                points2.append((point[0], point[1] + self.v0 * self.time + (self.g*self.time**2)/2))
            else:
                points2.append((point[0], point[1] + self.v0 * self.time + (self.g*self.time**2)/2))
        self.v0 += self.g*self.time
        return points2
    