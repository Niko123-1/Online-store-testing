class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """Вернет True если количество продукта больше или равно запрашиваемому и False в обратном случае"""

        return self.quantity >= quantity

    def buy(self, quantity):
        """Метод покупки: проверяем количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбрасываем исключение ValueError """

        if self.check_quantity(quantity):
            self.quantity -= quantity
        else: raise ValueError

    def __hash__(self):

        return hash(self.name + self.description)


class Cart:
    """Класс корзины. В нем хранятся продукты, которые пользователь хочет купить."""

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """

        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]

        else: self.products[product] -= remove_count

    def clear(self):

        self.products = {}

    def get_total_price(self) -> float:

        cart_total_price = 0
        for prod in self.products:
            cart_total_price+=prod.price*self.products[prod]
        return cart_total_price

    def buy(self):
        """
        Метод покупки.
        Товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for prod in self.products:
            if self.products[prod]>prod.quantity:
                raise ValueError
            else:
                prod.buy(self.products[prod])