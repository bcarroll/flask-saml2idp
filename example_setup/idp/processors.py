from flasksaml2idp.processors import BaseProcessor
from flask_login import current_user


class GroupProcessor(BaseProcessor):
    """
        Example implementation of access control for users:
        - they have to belong to a certain group
    """

    def has_access(self):
        return current_user.can_use_saml()
