from flask import Flask
import pytest


@pytest.fixture
def app():
    app = Flask(__name__)

    app.config['SAML_IDP_SPCONFIG'] = {
        'test_idp_1': {
            'attribute_mapping': {}
        }
    }

    app.secret_key = 'q+0vb%)c7c%&kl&jcca^6n7$3q4ktle9i28t(fd&qh28%l-%58'

    return app
