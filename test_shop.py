"""
Тестируем классы из модуля models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def multiple_products():
    return [
        Product("book", 100, "This is a book", 1000),
        Product("pen", 10, "This is a pen", 500),
        Product("notebook", 50, "This is a notebook", 200)
    ]

@pytest.fixture()
def cart_with_all_prods(multiple_products):
    crt = Cart()
    for prod in multiple_products:
        crt.add_product(prod,1)
    return crt

@pytest.fixture()
def empty_cart(multiple_products):
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, multiple_products):

        assert multiple_products[0].quantity == 1000

    def test_product_buy(self, multiple_products):

        need_to_buy = 800
        multiple_products[0].buy(need_to_buy)
        assert multiple_products[0].quantity == 200

    def test_product_buy_more_than_available(self, multiple_products):

        need_to_buy = 1001
        with pytest.raises(ValueError):
            multiple_products[0].buy(need_to_buy)


class TestCart:

    def test_add_product_to_empty_cart(self, empty_cart, multiple_products):
        empty_cart.add_product(multiple_products[1],2)
        assert empty_cart.products[multiple_products[1]] == 2

    def test_add_product_to_cart_with_prod(self, cart_with_all_prods, multiple_products):

        cart_with_all_prods.add_product(multiple_products[2],2)
        assert cart_with_all_prods.products[multiple_products[2]] == 3

    def test_remove_product_remove_count_none(self, cart_with_all_prods, multiple_products):

        cart_with_all_prods.remove_product(multiple_products[2])
        assert len(cart_with_all_prods.products) == 2
        assert multiple_products[2] not in cart_with_all_prods.products
        cart_with_all_prods.remove_product(multiple_products[1])
        assert len(cart_with_all_prods.products) == 1
        assert multiple_products[1] not in cart_with_all_prods.products

    def test_remove_product_remove_count_more_than_in_cart(self, cart_with_all_prods, multiple_products):

        cart_with_all_prods.remove_product(multiple_products[0],7)
        assert len(cart_with_all_prods.products) == 2
        assert multiple_products[0] not in cart_with_all_prods.products
        cart_with_all_prods.remove_product(multiple_products[1],9)
        assert len(cart_with_all_prods.products) == 1
        assert multiple_products[1] not in cart_with_all_prods.products

    def test_remove_product_remove_count_exact_in_cart(self, cart_with_all_prods, multiple_products):

        cart_with_all_prods.add_product(multiple_products[2], 5)
        cart_with_all_prods.remove_product(multiple_products[2],6)
        assert len(cart_with_all_prods.products) == 2
        cart_with_all_prods.add_product(multiple_products[0], 2)
        cart_with_all_prods.add_product(multiple_products[1], 3)
        cart_with_all_prods.remove_product(multiple_products[0],3)
        assert multiple_products[1] in cart_with_all_prods.products
        assert multiple_products[0] not in cart_with_all_prods.products

    def test_clear(self, cart_with_all_prods,multiple_products):
        cart_with_all_prods.clear()
        assert len(cart_with_all_prods.products) == 0
        cart_with_all_prods.add_product(multiple_products[2], 4)
        assert len(cart_with_all_prods.products) == 1

    def test_get_total_price(self, cart_with_all_prods, multiple_products):
        cart_with_all_prods.add_product(multiple_products[0], 2)
        cart_with_all_prods.add_product(multiple_products[2], 4)
        assert cart_with_all_prods.get_total_price() == 560

    def test_buy_more_than_quantity(self, cart_with_all_prods, multiple_products):
        cart_with_all_prods.add_product(multiple_products[1], 500)
        with pytest.raises(ValueError):
            cart_with_all_prods.buy()

    def test_buy(self, cart_with_all_prods, multiple_products):
        cart_with_all_prods.buy()
        assert multiple_products[0].quantity == 999
        assert multiple_products[1].quantity == 499
        assert multiple_products[2].quantity == 199

