import json
from models.role import Role
from models.user import User
from models.category import Category
from models.equipment import Equipment

class Database:
    def __init__(self, file_path="data.json"):
        self.file_path = file_path
        self.data = {"roles": [], "users": [], "categories": [], "equipments": []}

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {"roles": [], "users": [], "categories": [], "equipments": []}

    def add_role(self, role: Role):
        self.data["roles"].append(role.to_dict())
        self.save()

    def add_user(self, user: User):
        self.data["users"].append(user.to_dict())
        self.save()

    def add_category(self, category: Category):
        self.data["categories"].append(category.to_dict())
        self.save()

    def add_equipment(self, equipment: Equipment):
        self.data["equipments"].append(equipment.to_dict())
        self.save()

    def get_roles(self):
        return [Role.from_dict(r) for r in self.data["roles"]]

    def get_users(self):
        return [User.from_dict(u) for u in self.data["users"]]

    def get_categories(self):
        return [Category.from_dict(c) for c in self.data["categories"]]

    def get_equipments(self):
        return [Equipment.from_dict(e) for e in self.data["equipments"]]
