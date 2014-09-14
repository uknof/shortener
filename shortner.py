#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, flash, url_for, g
from forms import AddForm
import sqlite3
import random
import string
import ipaddr

VERSION = "0.0.1"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'development key'

DATABASE = "urls.db"

#@app.before_request
#def before_request():


def generate_short():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(5))


def unique_short():
    matches = 1
    while matches == 1:
        short = generate_short()
    	matches = query_db("select * from urls where short='%s'" % (short))
    return short


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        short = unique_short()
        get_db().execute('insert into urls (short,dest) values (?,?)', [short, form.dest.data])
	get_db().commit()
        flash("URL %s generated" % (short))
        return redirect(url_for('list_urls'))
    return render_template('add.html', form=form)


@app.route("/list")
def list_urls():
    urls = query_db('select *,(select sum(hits4) from hits where hits.short=urls.short) as hits4,(select sum(hits6) from hits where hits.short=urls.short) as hits6 from urls')
    return render_template('list.html', urls=urls)


def urlmatch(url):
    short = url.lower()
    match = query_db("select dest from urls where short='%s'" % (short))
    if len(match) == 0:
        # no match found
        return "No match found"
    destination = match[0]['dest']
    # work out src ip version
    srcip = request.remote_addr
    ip = ipaddr.IPAddress(srcip)
    hittoday = query_db("select * from hits where short='%s' and hitdate=date('now')" % (short))
    hitfield = "hits%s" % (ip.version)
    # update hit counters
    if len(hittoday) == 0:
        get_db().execute("insert into hits (short,hitdate,%s) values (?,date('now'),1)" % (hitfield), [short])
    else:
        get_db().execute("update hits set %s=%s+1 where short=?" % (hitfield,hitfield), [short])
    get_db().commit()
    # finally redirect
    return redirect(destination,code=302)


@app.route("/<url>")
def urlcheck(url):
    return urlmatch(url)


@app.route("/<url>/")
def urlchecktrailing(url):
    return urlmatch(url)


@app.route("/")
def index():
    return "wah"


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

# python
# from shortner import init_db
# init_db()


if __name__ == '__main__':
    app.debug = True
    app.run()
