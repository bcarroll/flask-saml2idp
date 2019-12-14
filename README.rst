flasksaml2idp
===============


.. image:: https://img.shields.io/pypi/v/flasksaml2idp.svg
    :scale: 100%
    :target: https://pypi.python.org/pypi/flasksaml2idp
    :alt: PyPi

.. image:: https://readthedocs.org/projects/flasksaml2idp/badge/?version=latest
    :scale: 100%
    :target: https://djangosaml2idp.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :scale: 100%
    :target: https://www.apache.org/licenses/LICENSE-2.0
    :alt: Apache 2.0 License


flaskosaml2idp implements the Identity Provider side of the SAML2 protocol for Flask.
It is based upon a similar project for django: `djangosaml2idp <https://github.com/OTA-Insight/djangosaml2idp>`.
It builds on top of `PySAML2 <https://github.com/IdentityPython/pysaml2>`_.

This package is currently in development and should NOT be used in a production environment.

Any contributions, feature requests, proposals, ideas ... are welcome! See the `CONTRIBUTING document <https://github.com/verenigingcampuskabel/djangosaml2idp/blob/master/CONTRIBUTING.md>`_ for some info.

Installation
============

PySAML2 uses `XML Security Library <http://www.aleksey.com/xmlsec/>`_ binary to sign SAML assertions, so you need to install
it either through your operating system package or by compiling the source code. It doesn't matter where the final executable is installed because
you will need to set the full path to it in the configuration stage. XmlSec is available (at least) for Debian, OSX and Alpine Linux.

Now you can install the flasksaml2idp package using pip. This will also install PySAML2 and its dependencies automatically::

    pip install flasksaml2idp


Configuration & Usage
=====================

TODO

Further optional configuration options
======================================

In the ``SAML_IDP_SPCONFIG`` setting you can define a ``processor``, its value being a string with dotted path to a class.
This is a hook to customize some access control checks. By default, the included `BaseProcessor` is used, which allows every user to login on the IdP.
You can customize this behaviour by subclassing the `BaseProcessor` and overriding its `has_access(self, request)` method. This method should return true or false, depending if the user has permission to log in for the SP / IdP.
The processor has the SP entity ID available as `self._entity_id`, and received the request (with an authenticated request.user on it) as parameter to the `has_access` function.
This way, you should have the necessary flexibility to perform whatever checks you need.
An example `processor subclass <https://github.com/OTA-Insight/djangosaml2idp/blob/master/example_setup/idp/idp/processors.py>`_ can be found in the IdP of the included example.

Without custom setting, users will be identified by the ``USERNAME_FIELD`` property on the user Model you use. By Django defaults this will be the username.
You can customize which field is used for the identifier by adding ``SAML_IDP_DJANGO_USERNAME_FIELD`` to your settings with as value the attribute to use on your user instance.

Customizing error handling
==========================

djangosaml2idp renders a very basic error page if it encounters an error, indicating an error occured, which error, and possibly an extra message.
The HTTP status code is also set if possible depending on which error occured.
You can customize this by using the ``SAML_IDP_ERROR_VIEW_CLASS`` setting. Set this to a dotted import path to your custom (class based) view in order to use that one.
If you subclass the provided `djangosaml2idp.error_views.SamlIDPErrorView`, you have the following variables available for use in the template:

exception_type
  the class of the exception that occurred

exception_msg
  the message from the exception (by doing `str(exception)`)

extra_message
  if no specific exception given, a message indicating something went wrong, or an additional message next to the `exception_msg`

The simplest override is to subclass the `SamlIDPErrorView` and only using your own error template.
You can use any Class-Based-View for this; it's not necessary to subclass the builtin error view.
The example project contains a ready to use example of this; uncomment the `SAML_IDP_ERROR_VIEW_CLASS` setting and it will use a custom view with custom template.


Multi Factor Authentication support
===================================

There are three main components to adding multiple factor support.


1. Subclass flasksaml2idp.processors.BaseProcessor as outlined above. You will need to override the `enable_multifactor()` method to check whether or not multifactor should be enabled for a user. (If it should allways be enabled for all users simply hard code to True). By default it unconditionally returns False and no multifactor is enforced.

2. Sublass the `flasksaml2idp.views.ProcessMultiFactorView` view to make the appropriate calls for your environment. Implement your custom verification logic in the `multifactor_is_valid` method: this could call a helper script, an internal SMS triggering service, a data source only the IdP can access or an external second factor provider (e.g. Symantec VIP). By default this view will log that it was called then redirect.

3. Update your urls.py and add an override for name='saml_multi_factor' - ensure it comes before importing the flasksaml2idp urls file so your custom view is used instead of the built-in one.


Running the test suite
======================
Install the dev dependencies in ``requirements-dev.txt``::

  pip install -r requirements-dev.txt

Run ``py.test`` from the project root::

  py.test



Example project
---------------
The directory ``example_project`` contains a barebone demo setup to demonstrate the login-logout functionality.
It consists of a Service Provider implemented with `djangosaml2 <https://github.com/knaperek/djangosaml2/>`_ and an Identity Provider using ``djangosaml2idp``.
The readme in that folder contains more information on how to run it.
