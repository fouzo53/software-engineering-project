class Customer:
    def __init__(self, id, store_id, full_name, phone=None, current_debt=0):
        self.id = id
        self.store_id = store_id
        self.full_name = full_name
        self.phone = phone
        self.current_debt = current_debt

    def increase_debt(self, amount):
        self.current_debt += amount

    def decrease_debt(self, amount):
        self.current_debt -= amount
