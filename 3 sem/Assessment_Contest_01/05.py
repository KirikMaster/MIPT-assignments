class GasStation:
    # Конструктор, принимающий один параметр - ёмкость резервуара колонки
    # Резервуар создаётся пустой
    def __init__(self, capacity):
        self.capacity = capacity
        self.current = 0

    # Залить в резервуар колонки n литров топлива
    # Если столько не влезает в резервуар - не заливать ничего, выбросить exception
    def fill(self, n):
        if n <= self.capacity - self.current: self.current += n
        else: raise BaseException

    # Заправиться, забрав при этом из резервура n литров топлива
    # Если столько нет в резервуаре - не забирать из резервуара ничего, выбросить exception
    def tank(self, n):
        if n <= self.current: self.current -= n
        else: raise BaseException

    # Запросить остаток топлива в резервуаре
    def get_limit(self):
        return self.current