

class Product:
    products = dict()
    regional_sale = dict()
    # monthly_regional_sells = dict()

    def __init__(self, product_id, product_name, price):
        self.id = product_id
        self.name = product_name
        self.price = price
        self.sold = 0
        self.dates = dict()
        self.monthly_sale = dict()
        self.monthly_regional_sells = dict()

        Product.products[self.id] = Product.products.get(self.id, self)

    def sell(self, quantity: int, date, region):
        self.sold += quantity
        self.dates[date] = self.dates.get(date, 0) + quantity
        my = date.split("/")[0]+"/"+date.split("/")[2]
        self.monthly_sale[my] = self.dates.get(my, 0) + quantity

        Product.regional_sale[region] = Product.regional_sale.get(region, dict({self.name: 0}))
        Product.regional_sale[region][self.name] = Product.regional_sale[region].get(self.name, 0) + quantity

        self.monthly_regional_sells[region] = self.monthly_regional_sells.get(region, dict({my: {self.name: 0}}))
        self.monthly_regional_sells[region][my] = self.monthly_regional_sells[region].get(my, dict({self.name: 0}))
        self.monthly_regional_sells[region][my][self.name] = self.monthly_regional_sells[region][my].get(self.name, 0) + quantity

        # Product.regional_sale[region].update({self.name: Product.regional_sale[region].get(self.name, dict({self.name: 0}))+quantity})




