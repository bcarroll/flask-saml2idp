import os
from flask import Blueprint
from . import views

blueprint = Blueprint('flasksaml2idp', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

blueprint.add_url_rule('/sso/post', 'saml_login_post', views.sso_entry, methods=['GET', 'POST'])
blueprint.add_url_rule('/sso/redirect', 'saml_login_redirect', views.sso_entry)
blueprint.add_url_rule('/sso/init', 'saml_idp_init', views.SSOInitView.as_view('saml_idp_init'))
blueprint.add_url_rule('/login/process/', 'saml_login_process', views.LoginProcessView.as_view('saml_login_process'))
blueprint.add_url_rule('/login/process_multi_factor/', 'saml_multi_factor',
                       views.ProcessMultiFactorView.as_view('saml_multi_factor'), methods=['GET'])
blueprint.add_url_rule('/metadata/', 'saml2_idp_metadata', views.metadata)


@blueprint.after_request
def disable_cache(response):
    """
    Post processor that adds headers to a response so that it will never be cached.
    """

    response.headers['Cache-Control'] = 'max-age=0, no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
