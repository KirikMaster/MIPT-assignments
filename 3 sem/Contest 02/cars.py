class Car:
    def __init__(self, capacity, speed, number):
        self.capacity = capacity
        self.speed = speed
        self.number = number

class RaceCar(Car):
    def __init__(self, speed):
        super().__init__(0, speed, None)