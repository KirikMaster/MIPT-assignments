class Car:
    def __init__(self, capacity, speed, number):
        self.capacity = capacity
        self.speed = speed
        self.number = number
    def print(self):
        print(self.capacity, self.speed, self.number)