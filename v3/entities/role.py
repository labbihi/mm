class Role:
    def __init__(self, role_id, name):
        self.id = role_id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
