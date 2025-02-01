class Category:
    def __init__(self, name):
        self.name = name
        self.equipment_list = []

    def add_equipment(self, equipment):
        self.equipment_list.append(equipment)

    def remove_equipment(self, equipment):
        self.equipment_list.remove(equipment)

    def get_equipment(self):
        return self.equipment_list