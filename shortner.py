#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, flash, url_for, g, session
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from forms import AddForm, LoginForm
import sqlite3
import random
import string
import ipaddr
import os
from passlib.hash import pbkdf2_sha256
import rfc3987
#from user import User

VERSION = "0.0.1"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = ''.join(random.choice(string.lowercase) for i in range(16))

DATABASE = "urls.db"
DATABASEREQ = 0.1

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User():

    # def __init__(self , username ,password , email):
    #    self.username = username
    #    self.password = password
    #    self.email = email
    #    self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User %r>' % (self.username)

    @staticmethod
    def processlogin(g, username, password):
        userdb = query_db("select * from users where username = ?", [username])
        if len(userdb) == 1:       
            # user exists, check the hash
            hash = userdb[0]["password"]
            if pbkdf2_sha256.verify(password, hash):
                return User.get(username)
        return None

    @staticmethod
    def get(username):
        u = User()
        u.username = "nat"
        return u

    @staticmethod
    def create(username, password):
        username = username.lower().strip()
        hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        get_db().execute('insert into users (username,password) values (?,?)', [username, hash])
        get_db().commit()        
        u = User.get(username) 
        return u


@login_manager.user_loader
def load_user(username):
    return User.get(username)


@app.before_request
def before_request():
    g.user = current_user
    print g.user


def unique_short():
    matches = 1
    while matches == 1:
        short = ''.join(random.choice(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']) for i in range(5))
        matches = query_db("select * from urls where short=?", [short])
    return short


def db_totals():
    total4 = 0
    total6 = 0
    totalhits = query_db('select sum(hits4) as total4, sum(hits6) as total6 from hits')
    if len(totalhits) > 0:
        total4 = totalhits[0]["total4"]
        total6 = totalhits[0]["total6"]
        if total4 is None:
            total4 = 0
        if total6 is None:
            total6 = 0

    items = {}
    items["Hits"] = total4 + total6
    items["Hit IPv4"] = total4
    items["Hit IPv6"] = total6

    items["URLs"] = query_db('select count(*) as urls from urls')[0]["urls"]
    items["Users"] = query_db('select count(*) as users from users')[0]["users"]

    return items

@app.route('/admin/about')
def about():
    return render_template('about.html',version=VERSION)


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html', form=form)
    registered_user = User.processlogin(g,form.username.data, form.password.data)
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
    totals = db_totals()
    return render_template('admin_index.html', totals=totals)


def url_dest_valid(dest):
    if rfc3987.match(dest, rule='URI'):
        return True
    return False


@app.route('/admin/urls/add', methods=['GET', 'POST'])
@login_required
def admin_urls_add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        if url_dest_valid(form.dest.data) is True:
            short = unique_short()
            createdby = g.user.username
            get_db().execute("insert into urls (short,dest,createdon,createdby) values (?,?,date('now'),?)", [short, form.dest.data,createdby])
            get_db().commit()
            flash("URL %s generated" % (short))
            return redirect(url_for('admin_urls_list'))
        else:
            flash("URL destination is not valid")
    return render_template('admin_urls_add.html', form=form)


@app.route("/admin/urls")
@login_required
def admin_urls_list():
    urls = query_db('select *,(select sum(hits4) from hits where hits.short=urls.short) as hits4,(select sum(hits6) from hits where hits.short=urls.short) as hits6 from urls')
    return render_template('admin_urls_list.html', urls=urls)


@app.route("/admin/urls/<short>")
@login_required
def admin_urls_detail(short):
    match = query_db("select * from urls where short=?", [short])
    if len(match) == 0:
        return redirect(url_for('admin_urls_list'))
    hits = query_db("select * from hits where short=? order by hitdate desc", [short])
    return render_template('admin_urls_detail.html', url=match[0], hits=hits)


def urlmatch(url):
    short = url.lower()
    match = query_db("select dest from urls where (short=? or custom=?)", [short, short])
    if len(match) == 0:
        # no match found
        return "No match found"
    destination = match[0]['dest']
    # work out src ip version
    srcip = request.remote_addr
    ip = ipaddr.IPAddress(srcip)
    hittoday = query_db("select * from hits where short=? and hitdate=date('now')", [short])
    hitfield = "hits%s" % (ip.version)
    # update hit counters
    if len(hittoday) == 0:
        get_db().execute("insert into hits (short,hitdate,%s) values (?,date('now'),1)" % (hitfield), [short])
    else:
        get_db().execute("update hits set %s=%s+1 where short=? and hitdate=date('now')" % (hitfield,hitfield), [short])
    get_db().commit()
    # finally redirect
    return redirect(destination, code=302)


@app.route("/<short>/<short1>/<short2>/")
@app.route("/<short>/<short1>/<short2>")
@app.route("/<short>/<short1>/")
@app.route("/<short>/<short1>")
@app.route("/<short>/")
@app.route("/<short>")
def urlcheck(short, short1=None, short2=None):
        if short1 is not None:
            short = short + "/" + short1
        if short2 is not None:
            short = short + "/" + short2
        return urlmatch(short)


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

