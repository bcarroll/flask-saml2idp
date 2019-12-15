#!/usr/bin/env python
import os
from urllib import parse

from flask_login import LoginManager, login_user, current_user, logout_user
from flask import Flask, request, render_template, session, redirect, url_for
from models import users

from flasksaml2idp.urls import blueprint

import saml2  # noqa
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED  # noqa
from saml2.sigver import get_xmlsec_binary  # noqa

app = Flask(__name__)
app.secret_key = 'ar249h_c(@5#x)ha_vou=4%plz*#!*l=+4c^jbo6wi%8z222hg'

BASE_URL = 'http://localhost:9000/idp'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config['SAML_IDP_CONFIG'] = {
    'debug': True,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': '%s/metadata' % BASE_URL,
    'description': 'Example IdP setup',

    'service': {
        'idp': {
            'name': 'Flask localhost IdP',
            'endpoints': {
                'single_sign_on_service': [
                    ('%s/sso/post' % BASE_URL, saml2.BINDING_HTTP_POST),
                    ('%s/sso/redirect' % BASE_URL, saml2.BINDING_HTTP_REDIRECT),
                ],
            },
            'name_id_format': [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
            'sign_response': True,
            'sign_assertion': True,
        },
    },

    'metadata': {
        'local': [os.path.join(BASE_DIR, 'certificates', 'sp_metadata.xml')],
    },
    # Signing
    'key_file': BASE_DIR + '/certificates/private.key',
    'cert_file': BASE_DIR + '/certificates/public.cert',
    # Encryption
    'encryption_keypairs': [{
        'key_file': BASE_DIR + '/certificates/private.key',
        'cert_file': BASE_DIR + '/certificates/public.cert',
    }],
    'valid_for': 365 * 24,
}


app.config['SAML_IDP_SPCONFIG'] = {
    'http://localhost:8000/saml2/metadata/': {
        'processor': 'processors.GroupProcessor',
        'attribute_mapping': {
            'email': 'email',
        }
    }
}

app.register_blueprint(blueprint, url_prefix='/idp')


def load_user(user_id):
    print(user_id)
    filtered = [user for user in users if user.get_id() == user_id]
    print(filtered)
    return filtered[0]


def handle_unauthorized():
    session['redirect'] = request.url
    return redirect(url_for('login'), code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    context = {}

    if request.method == 'POST':
        username = request.form['username'] if 'username' in request.form else None
        password = request.form['password'] if 'password' in request.form else None

        user = [user for user in users if user.username == username and user.password == password]

        if user:
            login_user(user[0])

            if 'redirect' in session:
                url = session['redirect']
                del session['redirect']

                return redirect(url)

            return redirect(url_for('index'))
        else:
            context['error'] = 'User not found.'

    return render_template('idp/login.html', **context)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/', methods=['GET'])
def index():
    context = {}

    if current_user.is_authenticated:
        context.update({
            # "user_attrs": sorted([(field.name, getattr(current_user, field.name))
            #                       for field in current_user._meta.get_fields() if field.concrete]),

            "known_sp_ids": [x for x in app.config['SAML_IDP_SPCONFIG']],
            "current_user": current_user
        })

    return render_template('idp/index.html', **context)


@app.template_filter('urlencode')
def urlencode(uri, **query):
    parts = list(parse.urlparse(uri))
    q = parse.parse_qs(parts[4])
    q.update(query)
    parts[4] = parse.urlencode(q)
    return parse.urlunparse(parts)


app.jinja_env.globals['urlencode'] = urlencode

login_manager = LoginManager()
login_manager.user_loader(load_user)
login_manager.unauthorized_handler(handle_unauthorized)
login_manager.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9000')
