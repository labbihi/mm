#from user import User
from entities.equipment import Equipment
import json


class Category:
    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name
        self.equipments = []

    def add_equipment(self, equipment):
        if equipment not in self.equipments:
            self.equipments.append(equipment)


    def remove_equipment(self, equipment):
        self.equipments.remove(equipment)

    def get_equipment(self):
        return self.equipments

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipments': [equipment.to_dict() for equipment in self.equipments],
        }

    def add_equipment(self, equipment):
        if equipment not in self.equipments:
            self.equipments.append(equipment)

    def remove_equipment(self, equipment_id):
        self.equipments = [eq for eq in self.equipments if eq.id != equipment_id]

    def get_equipment(self):
        return self.equipments

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipments': [equipment.to_dict() for equipment in self.equipments]
        }

class InventoryManager:
    def __init__(self, filename):
        self.filename = filename
        self.categories = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.categories = [Category(cat['id'], cat['name']) for cat in data.get('categories', [])]                
                for cat, cat_data in zip(self.categories, data.get('categories', [])):

                    for eq_data in cat_data.get('equipments', []):
                        eq = Equipment(eq_data['id'], eq_data['name'], eq_data['quantity'], eq_data['condition'], eq_data['available_to_use'], cat)
                        cat.add_equipment(eq)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"An error occurred while loading data: {e}")
            self.categories = []

    def save_data(self):
        try:
            data = {'categories': [category.to_dict() for category in self.categories]}
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
        except TypeError as e:
            print(f"JSON serialization error: {e}")

    def add_category(self, category_id, name):
        if not any(cat.id == category_id for cat in self.categories):
            self.categories.append(Category(category_id, name))

            print([category.id for category in self.categories])
            self.save_data()

    def remove_category(self, category_id):
        self.categories = [cat for cat in self.categories if cat.id != category_id]
        self.save_data()

    def add_equipment_to_category(self, category_id, equipment_id, name, quantity, condition, available_to_use):
        category = next((cat for cat in self.categories if cat.id == category_id), None)
        if category:
            new_equipment = Equipment(equipment_id, name, quantity, condition, available_to_use, category)
            category.add_equipment(new_equipment)
            self.save_data()

    def remove_equipment_from_category(self, category_id, equipment_id):
        category = next((cat for cat in self.categories if cat.id == category_id), None)
        if category:
            category.remove_equipment(equipment_id)
            self.save_data()

    
 
    def get_category(self, category_name):
        return next((cat for cat in self.categories if cat.name == category_name), None)
    

    def newId(self):
        return max([cat.id for cat in self.categories], default=0) + 1
    
    def get_category_for_statistique(self, category_name):
        category = self.get_category(category_name)
        
        if not category:
            print(f"Category {category_name} not found!")
            return None
        
        # Initialisation des listes vides pour chaque type de donnée
        equipments = []
        quantities = []
        conditions = []
        condition_counts = {"New": 0, "Good": 0, "Fair": 0, "Worn": 0, "Damaged": 0}
        availability_labels = ["Disponible", "Indisponible"]
        availability_counts = [0, 0]  # [count_disponible, count_indisponible]

        # Remplir les données pour chaque équipement de la catégorie
        for equipment in category.get_equipment():
            equipments.append(equipment.name)
            quantities.append(equipment.quantity)
            conditions.append(equipment.condition)
            
            # Gestion des conditions inconnues
            if equipment.condition in condition_counts:
                condition_counts[equipment.condition] += 1
            else:
                print(f"Alerte : Condition '{equipment.condition}' inconnue pour l'équipement '{equipment.name}'.")
            
            if equipment.available_to_use:
                availability_counts[0] += 1  # Disponible
            else:
                availability_counts[1] += 1  # Indisponible

        # Formater les données dans le format souhaité
        category_data = {
            category_name: {
                "equipments": equipments,
                "quantities": quantities,
                "conditions": conditions,
                "condition_counts":[condition_counts["New"], condition_counts["Good"], condition_counts["Fair"], condition_counts["Worn"], condition_counts["Damaged"]],
                "availability_labels": availability_labels,
                "availability_counts": availability_counts
            }
        }

        return category_data

