#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, flash, url_for, g
from forms import AddForm
import sqlite3
import random
import string
import ipaddr
import os

VERSION = "0.0.1"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'development key'

DATABASE = "urls.db"

#@app.before_request
#def before_request():


def unique_short():
    matches = 1
    while matches == 1:
        short = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    	matches = query_db("select * from urls where short=?", [short])
    return short


@app.route('/admin/')
@app.route('/admin')
def admin_index():
    total4 = 0
    total6 = 0
    totalhits = query_db('select sum(hits4) as total4, sum(hits6) as total6 from hits')
    if len(totalhits) > 0:
        total4 = totalhits[0]["total4"]
        total6 = totalhits[0]["total6"]

    items = []
    items.append({"Hits": total4 + total6 })
    items.append({"Hit IPv4": total4 })
    items.append({"Hit IPv6": total6 })

    urlcount = query_db('select count(*) as urls from urls')[0]["urls"]
    items.append({"URLs": urlcount })

    return render_template('admin_index.html', totals=items)


@app.route('/admin/urls/add', methods=['GET', 'POST'])
def admin_urls_add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        short = unique_short()
        get_db().execute('insert into urls (short,dest) values (?,?)', [short, form.dest.data])
	get_db().commit()
        flash("URL %s generated" % (short))
        return redirect(url_for('admin_urls_list'))
    return render_template('admin_urls_add.html', form=form)


@app.route("/admin/urls")
def admin_urls_list():
    urls = query_db('select *,(select sum(hits4) from hits where hits.short=urls.short) as hits4,(select sum(hits6) from hits where hits.short=urls.short) as hits6 from urls')
    return render_template('admin_urls_list.html', urls=urls)


@app.route("/admin/urls/<short>")
def admin_urls_detail(short):
    match = query_db("select dest from urls where short=?", [short])
    if len(match) == 0:
        return redirect(url_for('admin_urls_list'))
    hits = query_db("select * from hits where short=? order by hitdate desc", [short])
    return render_template('admin_urls_detail.html', url=match, hits=hits)


def urlmatch(url):
    short = url.lower()
    match = query_db("select dest from urls where short=?", [short])
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
        get_db().execute("insert into hits (short,hitdate,%s) values (?,date('now'),1)" % (hitfield) ,[short])
    else:
        get_db().execute("update hits set %s=%s+1 where short=? and hitdate=date('now')" % (hitfield,hitfield) ,[short])
    get_db().commit()
    # finally redirect
    return redirect(destination,code=302)


@app.route("/<short>/")
@app.route("/<short>")
def urlcheck(short):
    return urlmatch(short)


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

    if os.path.isfile(DATABASE) is False:
        print ""
        print "ERROR: sqlite db does not exist: %s" % (DATABASE)
        print ""
        exit(1)

    app.debug = True
    app.run()
