from product import Product


class Customer:
    customers = dict()

    def __init__(self, customer_id):
        self.id = customer_id
        self.products: dict[Product] = {}
        Customer.customers[self.id] = self
        self.day_purchase = dict()

    def buy(self, product: Product, quantity: int, day):
        self.products[product] = [self.products.get(product, 0) + quantity,
                                  self.products.get(product, 0) + (product.price * quantity)]
        self.day_purchase[day] = self.day_purchase.get(day, []) + [product]

