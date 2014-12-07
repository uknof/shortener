#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, flash, url_for, g, session, jsonify
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import random
import os
import json
from shortlib import Database, User, Url, Totals

VERSION = "0.0.2"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = ''.join(random.choice(string.lowercase) for i in range(16))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
    return User.get(username)


@app.before_request
def before_request():
    g.user = current_user
    print g.user

@app.route('/admin/about')
def about():
    return render_template('about.html',version=VERSION)


@app.route('/admin/login')
def login():
    return render_template('login.html')


@app.route('/admin/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin/')
@app.route('/admin')
@login_required
def admin_index():
    return render_template('admin_index.html')

# API

@app.route('/admin/api/login', methods=['POST'])
def admin_api_login():
    if "login" not in request.json:
        return jsonify(success=False)
    login = request.json["login"]
    if "username" not in login or "password" not in login:
        return jsonify(success=False)
    username = login["username"]
    password = login["password"]
    registered_user = User.authenticate(username, password)
    if registered_user is None:
        return jsonify(success=False)
    login_user(registered_user)
    return jsonify(success=True)

@app.route('/admin/api/users')
@login_required
def admin_api_users():
    users = User.get_all()
    return json.dumps([dict(user.__dict__) for user in users])

@app.route('/admin/api/urls')
@login_required
def admin_api_urls():
    urls = Url.get_all()
    return json.dumps([dict(url.__dict__) for url in urls])

@app.route('/admin/api/urls/create', methods=['POST'])
@login_required
def admin_api_urls_create():
    if "url" not in request.json:
        return jsonify(success=False)
    newurl = request.json["url"]
    if "dest" not in newurl:
        return jsonify(success=False)
    dest = newurl["dest"]
    custom = newurl["custom"]
    notes = newurl["notes"]
    short = Url.unique_short()
    u = Url.create(short, dest, g.user.username, custom=custom, notes=notes)
    return jsonify(success=True, short=u.short)

@app.route('/admin/api/totals')
@login_required
def admin_api_totals():
    t = Totals()
    return json.dumps(t.get_all_rows())

# URLS

@app.route('/admin/urls/add', methods=['GET', 'POST'])
@login_required
def admin_urls_add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        if Url.url_valid(form.dest.data) is True:
            short = Url.unique_short()
            createdby = g.user.username
            Url.create(short,form.dest.data,createdby)
            flash("URL %s generated" % (short))
            return redirect(url_for('admin_urls_list'))
        else:
            flash("URL destination is not valid")
    return render_template('admin_urls_add.html', form=form)


@app.route("/admin/urls")
@login_required
def admin_urls_list():
    return render_template('admin_urls_list.html')


@app.route("/admin/urls/<short>")
@login_required
def admin_urls_detail(short):
    url = Url(short)
    if url == None:
        return redirect(url_for('admin_urls_list'))
    return render_template('admin_urls_detail.html', url=url, hits=url.hits())

# * Users

@app.route("/admin/users")
@login_required
def admin_users_list():
    return render_template('admin_users_list.html')


#@app.route("/<short>/<short1>/<short2>/")
#@app.route("/<short>/<short1>/<short2>")
#@app.route("/<short>/<short1>/")
#@app.route("/<short>/<short1>")
@app.route("/<short>/")
@app.route("/<short>")
def urlcheck(short, short1=None, short2=None):
        if short1 is not None:
            short = short + "/" + short1
        if short2 is not None:
            short = short + "/" + short2

        match = Url.match(short.lower())
        if match is None:
            return "No match found"

        match.hits_record(request.remote_addr)

        # finally redirect
        return redirect(match.dest, code=302)


@app.route("/")
def index():
    return "URL Shortner v%s" % (VERSION)

if __name__ == '__main__':

    if Database.exists() is False:
        print ""
        print "Please run dbsetup.py"
        print ""
        exit(1)

    app.debug = True
    app.run()

