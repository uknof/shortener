# UKNOF URL Shortner

## Overview

This app provides a simple URL shortening service, other similar projects already exist, but did not meet all of our requirements.

It is built using:

* Python
* Flask
* Flask-WTF, Flask-Login
* sqlite3

## Production deployment

TODO

## Development

### Setting up your environment

Clone the repo, then install the required Python modules:

```
$ git clone git@github.com:uknof/shortner.git
$ cd shortner
$ sudo pip install -r requirements.txt
```

Create an empty database:

```
$ python
Python 2.7.5 (default, Mar  9 2014, 22:15:05)
>>> from shortner import init_db
>>> init_db()
>>> exit()
```

Running the local web server:

```
$ ./shortner.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader

```

Point your web browser at http://127.0.0.1:5000
