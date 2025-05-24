import pandas


class Database:
    def __init__(self, file):
        self.df = pandas.read_csv(file)
        # try:
        #     self.df.drop('')

    def is_same_format(self):
        if list(self.df.columns.values) == ['Transaction ID', 'CustomerID', 'ProductID', 'ProductName', 'Quantity', 'PriceperUnit', 'Date', 'TotalPrice', 'Region']:
            return 1
        return 0

