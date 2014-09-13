#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, flash, url_for, g
from forms import ContactForm, AddForm
import sqlite3

VERSION = "0.0.1"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'development key'

DATABASE = "urls.db"

#@app.before_request
#def before_request():

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        get_db().execute('insert into urls (dest) values (?)', [form.dest.data])
	get_db().commit()
        flash('URL added')
        return redirect(url_for('list_urls'))
    return render_template('add.html', form=form)
#  if request.method == 'POST':
#    if form.validate() == False:
#      flash('Required field missing')
#      return render_template('add.html', form=form)
#    else:
#      return 'Form posted.' 
#  elif request.method == 'GET':
#    return render_template('add.html', form=form)

@app.route("/list")
def list_urls():
    urls = query_db('select * from urls')
    return render_template('list.html',urls=urls)


@app.route("/<url>")
def urlcheck(url):
    return "test %s" % (url)
 
@app.route("/")
def index():
    return "wah"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
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

