Changing JWT Claims
===================

You may want to change the claims that are stored in the created JWTs.
This can be done with the `@jwt.jwt_data_loader` decorator, and the
jwt can be accessed in your protected endpoints with the `get_jwt()` function.

.. literalinclude:: ../examples/change_token_data.py

Note: be careful of what you what data you put in the JWT. Any data in the
JWT can be easily viewed with anyone who has access to the token.
Make sure you don't put any sensitive information in them!
