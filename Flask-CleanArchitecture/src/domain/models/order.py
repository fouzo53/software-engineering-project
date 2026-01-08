class Order:
    def __init__(self, id, store_id, customer_id, creator_user_id, status):
        self.id = id
        self.store_id = store_id
        self.customer_id = customer_id
        self.creator_user_id = creator_user_id
        self.status = status
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def total_amount(self):
        return sum(item.total_price() for item in self.items)
