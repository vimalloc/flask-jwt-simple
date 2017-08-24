API Documentation
=================
In here you will find the API for everything exposed in this extension.

Configuring JWT Options
~~~~~~~~~~~~~~~~~~~~~~~
.. currentmodule:: flask_jwt_simple

.. module:: flask_jwt_simple

.. autoclass:: JWTManager

  .. automethod:: __init__
  .. automethod:: init_app
  .. automethod:: expired_token_loader
  .. automethod:: invalid_token_loader
  .. automethod:: unauthorized_loader
  .. automethod:: jwt_data_loader


Protected endpoint decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: jwt_required
.. autofunction:: jwt_optional


Utilities
~~~~~~~~~
.. autofunction:: get_jwt
.. autofunction:: get_jwt_identity
.. autofunction:: create_jwt
.. autofunction:: decode_jwt
