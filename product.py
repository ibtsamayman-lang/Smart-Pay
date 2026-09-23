class Product:

    def __init__(
        self,
        name,
        price=None,
        website="",
        link="",
        description=""
    ):
        self.name = name
        self.price = price
        self.website = website
        self.link = link
        self.description = description

    def display(self):
        print(f"Product: {self.name}")
        print(f"Price: {self.price}")
        print(f"Website: {self.website}")
        print(f"Link: {self.link}")


class PriceResult:

    def __init__(self, product, prices):
        self.product = product
        self.prices = prices

    def get_lowest_price(self):
        if not self.prices:
            return None

        return min(self.prices)

    def get_average_price(self):
        if not self.prices:
            return None

        return sum(self.prices) / len(self.prices)

class Deal:

    def __init__(self, store, price, link, source_type):
        self.store = store
        self.price = price
        self.link = link
        self.source_type = source_type

    def display(self):
        print(f"Store: {self.store}")
        print(f"Price: {self.price:,.2f} EGP")
        print(f"Type: {self.source_type}")
        print(f"Link: {self.link}")