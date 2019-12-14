from flask import Blueprint

from . import views

blueprint = Blueprint('flasksaml2idp', __name__, template_folder='templates')

blueprint.add_url_rule('sso/post', 'saml_login_post', views.sso_entry, methods=['GET', 'POST'])
blueprint.add_url_rule('sso/redirect', 'saml_login_redirect', views.sso_entry)
blueprint.add_url_rule('sso/init', 'saml_idp_init', views.SSOInitView)
blueprint.add_url_rule('login/process/', 'saml_login_process', views.LoginProcessView)
blueprint.add_url_rule('login/process_multi_factor/', 'saml_multi_factor', views.ProcessMultiFactorView,
                       methods=['GET'])
blueprint.add_url_rule('metadata/', 'saml2_idp_metadata', views.metadata)
