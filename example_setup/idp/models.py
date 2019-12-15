from flask_login import UserMixin


class Group():
    name = ""
    can_use_saml = False

    def __init__(self, name, can_use_saml=False):
        self.name = name
        self.can_use_saml = can_use_saml


class User(UserMixin):

    user_id = 0
    username = ""
    password = ""
    email = ""
    groups = []

    def __init__(self, user_id, username, password, email, groups=[]):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.groups = groups

    def can_use_saml(self):
        return any(group.can_use_saml for group in self.groups)

    def get_id(self):
        return self.user_id


groups = [
    Group('normal users'),
    Group('admins', True)
]

users = [
    User(1, 'example', 'password', 'example@exampl.com', [groups[0]]),
    User(2, 'admin', 'password', 'admin@example.com', [groups[0], groups[1]])
]
