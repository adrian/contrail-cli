=====================
contrail-cli
=====================

Introduction
------------
contrail-cli is a commandline tool for interacting with the Contrail API.


Development
-----------
To prepare your development environment,

::

  virtualenv .venv
  source .venv/bin/activate
  python setup.py develop

Deploy the Contrail vnc_api library into your virtual env. This package ships with contrail.

To generate README.html,

::

  rst2html README.rst > README.html

To package the app,

::

  python setup.py bdist_wheel --universal

For more info see `Packaging - Universal Wheels <https://packaging.python.org/en/latest/distributing.html#universal-wheels>`_.
