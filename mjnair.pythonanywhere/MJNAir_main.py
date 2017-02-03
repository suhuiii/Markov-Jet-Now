
import random
import os, sys
import sqlite3

from flask import Flask, render_template, jsonify, g, request, session, redirect, url_for
import uuid
from markov_MJN import markov_MJN

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'MJN.db'),
	SECRET_KEY = 'dev_key',
	# USERNAME = 'admin',
	# PASSWORD = '',
	SERVER_NAME = '127.0.0.1:5000'))

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode = 'r') as f:
		db.cursor().executescript(f.read())
	db.commit()
	

@app.cli.command('initdb')
def initdb_command():
	init_db()

def insert_db(values):
	cur = get_db()
	cur.row_factory = sqlite3.Row
	cur.execute('insert into entries (text, author, uuid) values(?,?,?)', values)
	get_db().commit()
	cur.close()
	return 

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

characters = ["Arthur","Martin","Douglas","Carolyn","Arthur","Martin","Douglas","Carolyn","Herc", "Mr. Birling"]
mkn_bot = markov_MJN(characters)

def get_quote_from_random_character():
	current_character = random.choice(characters)
	text = mkn_bot.getModel(current_character).generate_sentence()
	return (current_character, text)

@app.route("/")
def main_page():
	(current_character, text) = get_quote_from_random_character()
	return render_template("MarkovJetNow.html", text = text, name = current_character, modal = "none" )

@app.route("/more")
def more_quote():
	(current_character, text) = get_quote_from_random_character()
	return jsonify(text = text, name = current_character )

@app.route("/save", methods = ['GET','POST'])
def save_entry():
	request_data = request.get_json()
	random_uuid = str(uuid.uuid4())
	insert_db([request_data.get('text'), request_data.get('name'), random_uuid])
	return jsonify(url = url_for('get_id', id = random_uuid, _external=True))

@app.route("/<uuid:id>")
def get_id(id):
	result = query_db('select * from entries where uuid = ?',[str(id)], one = True)
	if result is None:
		return redirect(url_for('page_not_found'))
	return render_template("MarkovJetNow.html", text = result['text'], name = result['author'], modal = "none" )

@app.errorhandler(404)
def page_not_found(e):
    return url_for("main_page"), 404

if __name__ == '__main__':
	app.debug = True
	app.run()