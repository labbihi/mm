#from role import Role

class User:
    def __init__(self, id: int, name: str, email: str, login: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.login = login
        self.password = password
        self.roles = []
        self.categories = []

    def add_role(self, role):
        if role not in self.roles:
            self.roles.append(role)

    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'login': self.login,
            'password': self.password,
            'roles': [role.to_dict() for role in self.roles],
            'categories': [category.to_dict() for category in self.categories],
        }

    @staticmethod
    def save(users):
        with open('data.json', 'w') as f:
            json.dump({'users': [user.to_dict() for user in users]}, f)
