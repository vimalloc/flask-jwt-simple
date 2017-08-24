Installation
==============



The easiest way to start working with this extension with pip:

.. code-block:: bash

  $ pip install flask-jwt-simple

If you want to use asymmetric (public/private key) key signing algorithms, include
the ``asymmetric_crypto`` extra requirements.

.. code-block:: bash

  $ pip install flask-jwt-simple[asymmetric_crypto]

Note that if you are using ZSH (possibly other shells too), you will need to escape the brackets

.. code-block:: bash

  $ pip install flask-jwt-simple\[asymmetric_crypto\]


If you prefer to install from source, you can clone this repo and run

.. code-block:: bash

  $ python setup.py install
