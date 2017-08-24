# Flask-JWT-Simple
[![Build Status](https://travis-ci.org/vimalloc/flask-jwt-simple.svg?branch=master)](https://travis-ci.org/vimalloc/flask-jwt-simple)
[![Coverage Status](https://coveralls.io/repos/github/vimalloc/flask-jwt-simple/badge.svg)](https://coveralls.io/github/vimalloc/flask-jwt-simple)
[![PyPI version](https://badge.fury.io/py/Flask-JWT-Simple.svg)](https://badge.fury.io/py/Flask-JWT-Simple)
[![Documentation Status](https://readthedocs.org/projects/flask-jwt-simple/badge/)](http://flask-jwt-simple.readthedocs.io/en/latest/)


### When to use Flask-JWT-Simple?

Flask-JWT-Simple adds barebones support for protecting flask endpoints
with JSON Web Tokens. It is particularly good for fast prototyping or
consuming/producing JWTs that work with other providers and consumers.


### When *not* to use Flask-JWT-Simple?

If you are using JWTs with just your flask application, it may make more
sense to use the sister extension [Flask-JWT-Extended](https://github.com/vimalloc/flask-jwt-extended).
It provides several built in features to make working with JSON Web Tokens
easier. These include refresh tokens, fresh/unfresh tokens, tokens in cookies,
csrf protection when using cookies, and token revoking. The drawback is that 
extension is a more opinionated on what needs to be in the JWT in order
to get all those extra features to work.


### Installation
[View Installation Instructions](http://flask-jwt-simple.readthedocs.io/en/latest/installation.html)


### Usage
[View the documentation online](http://flask-jwt-simple.readthedocs.io/en/latest/)


### Chatting
We are on irc! You can come chat with us in the ```#flask-jwt-extended``` channel on ```freenode```.


### Testing and Code Coverage
We require 100% code coverage in our unit tests. You can run the tests locally
with `tox` which will print out a code coverage report. Creating a pull request
will run the tests against python 2.7, 3.3, 3,4, 3,5, 3,6, and PyPy.
```
$ tox
```

### Generating Documentation
You can generate a local copy of the documentation. After installing the requirements,
go to the `docs` directory and run:
```
$ make clean && make html
```
