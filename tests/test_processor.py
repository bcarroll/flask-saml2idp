from flasksaml2idp.processors import BaseProcessor
from .models import User


class TestBaseProcessor:

    def test_extract_user_id_configure_by_user_class(self, app):

        # with app.app_context():
        user = User()
        user.USERNAME_FIELD = 'email'
        user.email = 'test_email'

        assert BaseProcessor('entity-id').get_user_id(user) == 'test_email'

    def test_extract_user_id_configure_by_settings(self, app):
        """Should use `settings.SAML_IDP_FLASK_USERNAME_FIELD` to determine the user id field"""

        app.config['SAML_IDP_FLASK_USERNAME_FIELD'] = 'first_name'

        # with app.app_context():
        user = User()
        user.first_name = 'test_first_name'

        assert BaseProcessor('entity-id').get_user_id(user) == 'test_first_name'
