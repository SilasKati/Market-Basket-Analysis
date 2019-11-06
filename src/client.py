class Client:
    def __init__(self, identifier, orders):
        self.identifier = identifier
        self.orders = orders
        self.norders = len(orders)
