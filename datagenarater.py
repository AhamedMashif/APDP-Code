from faker import Faker
import random
import pandas as pd

products = {
    109: "Cereal",
    100: "Apple",
    104: "Beef",
    102: "Cheese",
    108: "Yogurt",
    103: "Bread",
    105: "Chicken",
    101: "Banana",
    106: "Fish",
    107: "Milk"
}

fake = Faker()
n_rows = 1000

data = {
    "Transaction ID": [_ for _ in range(n_rows)],
    "CustomerID": [random.randint(100, 999) for _ in range(n_rows)],
    "ProductID": [random.choice(list(products.keys())) for _ in range(n_rows)],
    "ProductName": [_ for _ in range(n_rows)],
    "Quantity": [random.randint(1, 14) for _ in range(n_rows)],
    "PriceperUnit": [round(random.uniform(1.0, 15.0), 2) for _ in range(n_rows)],
    "Date": [fake.date_between(start_date='-1y', end_date='today').strftime("%m/%d/%Y") for _ in range(n_rows)],
    "TotalPrice": [_ for _ in range(n_rows)],
    "Region": [random.choice(["Colombo", "Kalutara", "Galle", "Matara"]) for _ in range(n_rows)]
}

print(data)

df = pd.DataFrame(data)
df["TotalPrice"] = df["Quantity"] * df["PriceperUnit"]
df["ProductName"] = [products[i] for i in df["ProductID"]]


# Save to CSV (optional)
# df.to_csv("generated_sales.csv", index=False)

print(df.to_csv("sample.csv", index=False))
