from _decimal import Decimal

from product_app.models import Product
from cart_app.models import Coupon

CART_SESSION_ID = "cart"  # We can use this variable except of 'cart' in paramets


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CART_SESSION_ID)  # age az ghabl dasht

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}  # age nadasht yeki dorost mikonim
        self.cart = cart

        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = Product.objects.get(id=int(item["id"]))
            item["product"] = product
            item['total_price'] = int(item['quantity']) * int(item['price'])
            item['unique_id'] = self.unique_id_generator(product.id, item['color'], item['size'])
            yield item

    def unique_id_generator(self, id, color, size):
        result = f"{id}-{color}-{size}"
        return result

    def add(self, product, quantity, color, size, override_quantity):
        unique = self.unique_id_generator(product.id, color, size)
        if unique not in self.cart:
            self.cart[unique] = {"quantity": 1, "price": str(product.price), "color": color, "size": size,
                                 "id": str(product.id)}
        else:
            self.cart[unique]['quantity'] += int(quantity)

        if override_quantity:
            self.cart[unique]['quantity'] = int(quantity)

        self.save()

    def len(self):
        """
        Count all items in the cart.
        """
        return sum(int(item['quantity']) for item in self.cart.values())

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()
        else:
            print("This id is unavailable in cart! cart_function")

    def total(self):
        cart = self.cart.values()
        total = 0
        for item in cart:  # Total of each price!
            total += int(item['price']) * int(item['quantity'])
        return total

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            first_price = self.coupon.discount / Decimal(100) * self.total()
            second_price = self.total() - first_price
            return second_price
        return Decimal(0)

    def save(self):
        self.session.modified = True

    def remove_cart(self):
        del self.session[CART_SESSION_ID]
