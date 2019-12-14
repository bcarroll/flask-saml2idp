# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from flasksaml2idp import __version__

setup(
    name='flasksaml2idp',
    version=__version__,
    description='SAML 2.0 Identity Provider for Flask',
    keywords="flask,pysaml2,sso,saml2,federated authentication,authentication,idp",
    author='Yoeri Otten, Mathieu Hinderyckx',
    author_email='yoeri@vck.utwente.nl, mathieu.hinderyckx@gmail.com',
    maintainer="Yoeri Otten",
    long_description="\n\n".join([
        open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    ]),
    install_requires=[
        'Flask>=1.0',
        'Flask-Login',
        'pysaml2>=4.5.0'
        ],
    license='Apache Software License 2.0',
    packages=find_packages(exclude=["tests*", "docs", "example_setup"]),
    url='https://github.com/verenigingcampuskabel/flask-saml2idp/',
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
