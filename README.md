# UKNOF URL Shortner

## Overview

This app provides a simple URL shortening service, other similar projects already exist, but did not meet all of our requirements.

It is built using Python (see [requirements.txt](requirements.txt)):

* Python3
* Flask
* Flask-Login
* sqlite3
* passlib
* ipaddr
* rfc3987
* unittest

HTML / JS / CSS:

* Bootstrap
* Bootbox.js
* Bootstrap-table
* BootstrapValidator
* jQuery


## URLs

* `/admin/login` - Admin login page
* `/admin/` - Admin panel
* `/admin/about` - License, contributors, change log
* `/admin/urls` - List of existing short URLs, add/edit/delete URLs here
* `/admin/users` - List of users, add/edit/delete users here
* `/admin/logout`

## Settings

Global settings are stored in [.env](.env).

## Running

Start up the docker container:

```shell
docker-compose up -d
```

Now point your web browser to http://127.0.0.1:5000/admin

## Development

The list of contributors and the change log is in the [about page](templates/about.html) (viewable when running the app).

### Testing

Run tox inside the container

```shell
docker-compose exec shortner tox
```

Fix linting issues with:

```shell
docker-compose exec shortner tox -e fixlint
```
