Configuration Options
=====================

You can change many options for how this extension works via

.. code-block:: python

  app.config['OPTION_NAME'] = new_option_value

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================= =========================================
``JWT_HEADER_NAME``               What header to look for the JWT in a request. Defaults to ``'Authorization'``
``JWT_HEADER_TYPE``               What type of header the JWT is in. Defaults to ``'Bearer'``. This can be
                                  an empty string, in which case the header contains only the JWT
                                  (instead of something like ``Authorization: Bearer <JWT>``)
``JWT_EXPIRES``                   How long a JWT created with `create_jwt()` should live before it expires. This
                                  takes a ``datetime.timedelta``, and defaults to 1 hour
``JWT_ALGORITHM``                 Which algorithm to sign the JWT with. `See here <https://pyjwt.readthedocs.io/en/latest/algorithms.html>`_
                                  for the options. Defaults to ``'HS256'``.
``JWT_SECRET_KEY``                The secret key needed for symmetric based signing algorithms,
                                  such as ``HS*``.
``JWT_PUBLIC_KEY``                The public key needed for asymmetric based signing algorithms,
                                  such as ``RS*`` or ``ES*``. PEM format expected.
``JWT_PRIVATE_KEY``               The private key needed for asymmetric based signing algorithms,
                                  such as ``RS*`` or ``ES*``. PEM format expected.
``JWT_IDENTITY_CLAIM``            Which claim the `get_jwt_identity()` function will use to get
                                  the identity out of a JWT. Defaults to ``'sub'``.
``JWT_DECODE_AUDIENCE``           The audience you expect in a JWT when decoding it. Defaults
                                  to ``None``. If this option differs from the 'aud' claim
                                  in a JWT, the ``invalid_token_callback`` is invoked.
================================= =========================================
