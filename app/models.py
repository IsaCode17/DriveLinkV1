from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        # Aquí puedes agregar lógica para obtener usuarios de una base de datos
        # Por ahora usamos un ejemplo simple
        return User(id_=user_id, name="Test User", email="test@example.com")
