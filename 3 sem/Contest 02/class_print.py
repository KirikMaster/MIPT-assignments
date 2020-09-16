class Car:
    def __init__(self, capacity, speed, number):
        self.capacity = capacity
        self.speed = speed
        self.number = number

    def __repr__(self):
        return ("<Car capacity:" + str(self.capacity) + " speed:" + str(self.speed) + " number:" + str(self.number) + ">")