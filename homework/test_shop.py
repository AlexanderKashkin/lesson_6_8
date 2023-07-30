"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product_book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_notebook():
    return Product("notebook", 500, "This is a notebook", 2500)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize('quantity, result', [(-10, ValueError),
                                                  (0, ValueError),
                                                  (100, True),
                                                  (1000, True),
                                                  (1500, False)])
    def test_product_check_quantity(self, product_book: Product, quantity: int, result: bool or ValueError):
        assert product_book.check_quantity(quantity) == result

    @pytest.mark.parametrize('quantity, result', [(100, 900),
                                                  (500, 500),
                                                  (1000, 0)])
    def test_product_buy(self, product_book: Product, quantity: int, result: int):
        product_book.buy(quantity)
        assert product_book.quantity == result

    @pytest.mark.parametrize('quantity, result', [(1500, 'ValueError'),
                                                  (20000, 'ValueError'),
                                                  (850123, 'ValueError')])
    def test_product_buy_more_than_available(self, product_book: Product, quantity: int, result: ValueError):
        with pytest.raises(ValueError) as exception:
            product_book.buy(quantity)
        assert exception.typename == result


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    @pytest.mark.parametrize('buy_count, result', [(150, 150),
                                                   (250, 250),
                                                   (800, 800)])
    def test_add_product(self, product_book: Product, buy_count, result):
        cart = Cart()
        cart.add_product(product_book, buy_count=buy_count)
        assert cart.products[product_book] == result, f'{cart.products[product_book]} must be {result}'

    def test_add_product_twice(self, product_book: Product):
        cart = Cart()
        cart.add_product(product_book, buy_count=150)
        cart.add_product(product_book, buy_count=150)
        assert cart.products[product_book] == 300, f'{cart.products[product_book]=} must be 300'

    def test_add_different_product(self, product_book: Product, product_notebook: Product):
        cart = Cart()
        cart.add_product(product_book)
        cart.add_product(product_notebook)
        assert len(cart.products) == 2
        assert cart.products[product_book] == 1
        assert cart.products[product_notebook] == 1

    @pytest.mark.parametrize('buy_count, remove_count, result',
                             [(150, 140, 10),
                              (150, 130, 20),
                              (150, 120, 30),
                              (150, 150, 0)])
    def test_remove_product_positive(self, product_book: Product, buy_count: int, remove_count: int,
                                     result: int):
        cart = Cart()
        cart.add_product(product_book, buy_count=buy_count)
        cart.remove_product(product_book, remove_count=remove_count)
        assert cart.products[product_book] == result

    @pytest.mark.parametrize('buy_count, remove_count',
                             [(150, 160),
                              (150, None)])
    def test_remove_product_negative(self, product_book: Product, buy_count: int, remove_count: None):
        cart = Cart()
        cart.add_product(product_book, buy_count=buy_count)
        cart.remove_product(product_book, remove_count=remove_count)
        assert cart.products == {}

    def test_clear(self, product_book: Product):
        cart = Cart()
        cart.add_product(product_book)
        cart.clear()
        assert not cart.products, f'{cart.products=} must be empty'

    @pytest.mark.parametrize('quantity_book, quantity_notebook', [(2, 5),
                                                                  (1, 4),
                                                                  (6, 8),
                                                                  (0, 0)])
    def test_total_price(self, product_book: Product, product_notebook: Product, quantity_book: int,
                         quantity_notebook: int):
        cart = Cart()
        cart.add_product(product_book, buy_count=quantity_book)
        cart.add_product(product_notebook, buy_count=quantity_notebook)
        assert cart.get_total_price() == product_book.price * quantity_book + product_notebook.price * quantity_notebook

    def test_buy_positive(self, product_book: Product):
        cart = Cart()
        cart.add_product(product_book)
        cart.buy()
        assert product_book.quantity == 999

    def test_buy_negative(self, product_book: Product):
        cart = Cart()
        cart.add_product(product_book, buy_count=10100)
        assert cart.buy() == ValueError
