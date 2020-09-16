class MoneyBox:
    # Конструктор и деструктор, если нужны
    def __init__(self):
        self.Coins = []

    # Добавить монетку достоинством value
    def add_coin(self, value):
        self.Coins.append(value)

    # Получить текущее количество монеток в копилке
    def get_coins_number(self):
        return len(self.Coins)

    # Получить текущее общее достоинство всех монеток
    def get_coins_value(self):
        return sum(self.Coins)