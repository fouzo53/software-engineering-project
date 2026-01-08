class OrderItem:
    def __init__(self, product_id, quantity, unit_price):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def total_price(self):
        return self.quantity * self.unit_price
