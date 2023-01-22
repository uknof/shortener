#!/usr/bin/env python3

import json
import os
from typing import Dict, List

import flask_login  # type: ignore
from flask import Flask
from flask import Response as flask_Response
from flask import (
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.wrappers import Response as werkzeug_Response  # type: ignore

from shortlib import Database, Totals, Url, User

VERSION: str = "0.0.5"

app: Flask = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = User.gen_password()

login_manager: LoginManager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Login


@login_manager.user_loader
def load_user(username: str) -> User:
    return User.get(username)


@app.before_request
def before_request() -> None:
    g.user = current_user


@app.route("/admin/about")
def about() -> str:
    return render_template("about.html", version=VERSION)


@app.route("/admin/login")
def login() -> str:
    return render_template("login.html")


@app.route("/admin/logout", methods=["GET", "POST"])
def logout() -> werkzeug_Response:
    logout_user()
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin/")
@app.route("/admin")
@login_required
def admin_index() -> str:
    return render_template("admin_index.html")


# API


@app.route("/admin/api/login", methods=["POST"])
def admin_api_login() -> flask_Response:
    parsed_json = request.json
    if type(parsed_json) != dict:
        return jsonify(success=False)
    if "login" not in parsed_json:
        return jsonify(success=False)
    login: Dict = parsed_json["login"]
    if "username" not in login or "password" not in login:
        return jsonify(success=False)
    username: str = login["username"]
    password: str = login["password"]
    registered_user: None | User = User.authenticate(username, password)
    if registered_user is None:
        return jsonify(success=False)
    login_user(registered_user)
    return jsonify(success=True)


@app.route("/admin/api/users")
@login_required
def admin_api_users() -> str:
    users: List = User.get_all()
    return json.dumps([dict(user.__dict__) for user in users])


@app.route("/admin/api/urls")
@login_required
def admin_api_urls() -> str:
    urls: List = Url.get_all()
    return json.dumps([dict(url.__dict__) for url in urls])


@app.route("/admin/api/urls/create", methods=["POST"])
@login_required
def admin_api_urls_create() -> flask_Response:
    parsed_json = request.json
    if type(parsed_json) != dict:
        return jsonify(success=False)
    if "url" not in parsed_json:
        return jsonify(success=False)
    newurl: Dict = parsed_json["url"]
    if "dest" not in newurl:
        return jsonify(success=False)
    dest: str = newurl["dest"]
    custom: str = newurl["custom"]
    notes: str = newurl["notes"]
    short: str = Url.unique_short()
    u: Url = Url.create(
        short, dest, g.user.username, custom=custom, notes=notes
    )
    return jsonify(success=True, short=u.short)


@app.route("/admin/api/urls/delete", methods=["POST"])
@login_required
def admin_api_urls_delete() -> flask_Response:
    parsed_json = request.json
    if type(parsed_json) != dict:
        return jsonify(success=False)
    if "short" not in parsed_json:
        return jsonify(success=False)
    shortcode: str = parsed_json["short"]
    Url.delete(shortcode)
    return jsonify(success=True, short=shortcode)


@app.route("/admin/api/totals")
@login_required
def admin_api_totals() -> str:
    t = Totals()
    return json.dumps(t.get_all_rows())


# URLS


@app.route("/admin/urls")
@login_required
def admin_urls_list() -> str:
    return render_template("admin_urls_list.html")


@app.route("/admin/urls/<short>")
@login_required
def admin_urls_detail(short: str) -> str | werkzeug_Response:
    url: Url | None = Url(short)
    if url == None:
        return redirect(url_for("admin_urls_list"))
    assert url
    return render_template("admin_urls_detail.html", url=url, hits=url.hits())


# * Users


@app.route("/admin/users")
@login_required
def admin_users_list() -> str:
    return render_template("admin_users_list.html")


# @app.route("/<short>/<short1>/<short2>/")
# @app.route("/<short>/<short1>/<short2>")
# @app.route("/<short>/<short1>/")
# @app.route("/<short>/<short1>")
@app.route("/<short>/")
@app.route("/<short>")
def urlcheck(
    short: str, short1: str = "", short2: str = ""
) -> str | werkzeug_Response:
    if short1:
        short = short + "/" + short1
    if short2:
        short = short + "/" + short2

    match: Url | None = Url.match(short.lower())
    if match is None:
        return "No match found"

    if request.remote_addr:
        match.hits_record(request.remote_addr)

    return redirect(match.dest, code=302)


@app.route("/")
def index() -> werkzeug_Response:
    return redirect(os.environ["HOMEPAGE"], code=302)


if __name__ == "__main__":
    if not Database.exists():
        Database.setup()
        User.setup()

    if bool(os.environ["FLASK_DEBUG"]):
        app.debug = True
    app.run(host=os.environ["LISTEN_HOST"], port=int(os.environ["LISTEN_PORT"]))
