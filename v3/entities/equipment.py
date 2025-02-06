#from entities.category import Category

class Equipment:
    def __init__(self, id: int, name: str, quantity: int, condition: str, available_to_use: bool, category):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.condition = condition
        self.available_to_use = available_to_use
        self.category = category

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'condition': self.condition,
            'available_to_use': self.available_to_use,
            'category': self.category.id,
        }