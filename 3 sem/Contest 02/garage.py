class Garage:
    # Конструктор и деструктор, если нужны
    def __init__(self):
        self.Cars = []
        self.SelCars = []
        self.speed = 0
        self.number = None
    # Запарковать машину v
    def park(self, v):
        self.Cars.append(v)

    # Пересчитать машины заданного типа t.
    # Вернуть количество.
    def count(self, t):
        self.k = 0
        for i in self.Cars:
            if isinstance(i, t):
                self.k += 1
        return self.k
    # Получить самую быструю машину заданного типа t.
    # Вернуть экземпляр.
    def get_fastest_of_type(self, t):
        self.SelCars = []
        self.speed = 0
        for i in self.Cars:
            if isinstance(i, t):
                self.SelCars.append(i)
        for i in range(len(self.SelCars)):
            if self.SelCars[i].speed > self.speed:
                self.speed = self.SelCars[i].speed
                self.number = i
        return self.SelCars[self.number]