#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, flash, url_for, g, session
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from forms import AddForm, LoginForm
import random
import string
import os
import json
from shortobjs import User, Url, Totals

#from user import User

VERSION = "0.0.1"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'abcd'
#app.secret_key = ''.join(random.choice(string.lowercase) for i in range(16))

DATABASE = "urls.db"
DATABASEREQ = 0.1

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


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html', form=form)
    registered_user = User.authenticate(form.username.data, form.password.data)
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('admin_index'))


@app.route('/admin/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin/')
@app.route('/admin')
@login_required
def admin_index():
    return render_template('admin_index.html')

# API

@app.route('/admin/api/login')
def admin_api_login():
    return json.dumps({"success": False})

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

@app.route("/admin/users/add")
@login_required
def admin_users_add():
    return "not yet"

@app.route("/admin/users/<username>")
@login_required
def admin_users_edit(username):
    user = User(username)
    return "edit %s" % (user.username)


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


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
    db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print "Empty database %s created" % (DATABASE)
        username = "admin"
        password =  ''.join(random.choice(string.lowercase) for i in range(8))
        newuser = User.create(username, password)
        print "New user '%s' created with password '%s'" % (username, password)
        

if __name__ == '__main__':

    if os.path.isfile(DATABASE) is False:
        print ""
        print "ERROR: sqlite db does not exist: %s" % (DATABASE)
        print "    $ python"
        print "    >>> from shortner import init_db"
        print "    >>> init_db()"
        print "    >>> exit()"
        print ""
        exit(1)

    app.debug = True
    app.run()

