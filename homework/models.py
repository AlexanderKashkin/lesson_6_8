from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity) -> None:
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool or ValueError:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        if quantity <= 0:
            return ValueError
        return self.quantity >= quantity

    def buy(self, quantity: int) -> None or ValueError:
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            self.quantity = self.quantity - quantity
        else:
            return ValueError

    def __hash__(self) -> hash:
        return hash(self.name + self.description)


@dataclass
class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self) -> None:
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count: int = 1) -> None:
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products.keys():
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if remove_count is None or remove_count > self.products[product]:
            del self.products[product]
        else:
            self.products[product] = self.products[product] - remove_count

    def clear(self):
        """
        Метод очищения корзины
        """
        self.products.clear()

    def get_total_price(self) -> float:
        """
        Метод получения общей стоимости корзины (заказа)
        """
        total = 0
        for product, quantity in self.products.items():
            total = total + product.price * quantity
        return total

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product in self.products.keys():
            if product.check_quantity(self.products[product]):
                product.buy(self.products[product])
            else:
                return ValueError
        self.clear()
