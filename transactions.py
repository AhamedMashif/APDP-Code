from product import Product
from customer import Customer


class Transaction:
    transactions = dict()
    regions = dict()

    def __init__(self, transaction_id, customer_id, product_id, product_name, quantity, price_per_unit, date, totalPrice, region):
        self.id = transaction_id
        self.customer = Customer.customers.get(customer_id, Customer(customer_id))
        self.product = Product.products.get(product_id, Product(product_id, product_name, price_per_unit))
        self.quantity = quantity
        self.date = date
        self.region = region
        self.total = totalPrice
        self.product.sell(self.quantity, self.date, self.region)
        self.customer.buy(self.product, self.quantity, self.date)

        Transaction.transactions[transaction_id] = self
        Transaction.regions[self.region] = Transaction.regions.get(self.region, []) + [self.id]




