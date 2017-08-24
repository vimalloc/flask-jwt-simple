Basic Usage
===========

In its simplest form, there is not much to using flask_jwt_simple.

.. literalinclude:: ../examples/simple.py

To access a jwt_required protected view, all we have to do is send in the
JWT with the request. By default, this is done with an authorization header
that looks like:

.. code-block :: bash

  Authorization: Bearer <access_token>


We can see this in action using CURL:

.. code-block :: bash

  $ curl http://localhost:5000/protected
  {
    "msg": "Missing Authorization Header"
  }

  $ curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"test","password":"test"}' http://localhost:5000/login
  {
      "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDM1OTk3MTgsImlhdCI6MTUwMzU5NjExOCwibmJmIjoxNTAzNTk2MTE4LCJzdWIiOiJ0ZXN0In0.G2GnN9NgvvmSKgRDGok0OjAyDWkG_qCn4FTxSfPUXDY"
  }

  $ export ACCESS="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDM1OTk3MTgsImlhdCI6MTUwMzU5NjExOCwibmJmIjoxNTAzNTk2MTE4LCJzdWIiOiJ0ZXN0In0.G2GnN9NgvvmSKgRDGok0OjAyDWkG_qCn4FTxSfPUXDY"

  $ curl -H "Authorization: Bearer $ACCESS" http://localhost:5000/protected
  {
    "hello_from": "test"
  }

NOTE: Remember to change the JWT_SECRET_KEY on your application, and insure that no
one is able to view it. The json web tokens are signed with the secret key, so
if someone gets that, they can create arbitrary tokens, and in essence log in
as any user.
