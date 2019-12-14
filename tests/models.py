from flask_login import UserMixin


class User(UserMixin):
    id = 1
    first_name = "Test"
    last_name = "User"
    email = "test@example.com"
    username = "tester"
