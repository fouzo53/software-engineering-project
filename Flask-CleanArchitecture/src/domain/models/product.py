class Product:
    def __init__(self, id, store_id, category_id, name, image_url=None):
        self.id = id
        self.store_id = store_id
        self.category_id = category_id
        self.name = name
        self.image_url = image_url
