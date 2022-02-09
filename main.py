from flask import Flask, render_template, request, flash,redirect,url_for
from random import choice
from werkzeug.utils import secure_filename
import sqlite3

web_site = Flask(__name__)

@web_site.route('/')
def index():
  print("Hello World")
  #return "Hello world!"
  return render_template("index.html")
  

@web_site.route('/user/', defaults={'username': None})
@web_site.route('/user/<username>')
def welcome_user(username):
  if not username:
   return 'Error: no user name given'
  return "welcome back "+ username +"! <a href='/'>Home</a>"
  
@web_site.route('/pets')
def favepet():
  pets=["cat","dog","mouse","hamster"]
  #return choice(pets) #returns a random pet
  return render_template("pets.html",something=choice(pets))

@web_site.route('/login',methods = ['GET', 'POST'])
def login():
  msg = ""
  if request.method == 'POST':
    print(request.form["username"])
    print(request.form["password"])
    if request.form["username"] == "bob" and request.form["password"]=="cake":
      #return redirect(url_for("index"))
      return redirect('/') # This works in the main window not the preview one

 
    else:
      print("incorrect password")
      msg = "incorrect password"
  return render_template("login.html",msg = msg)

@web_site.route('/runonce')
def createDBandTable():
  con = sqlite3.connect('movies.db')
  sql = """
  CREATE TABLE Movies(id INTEGER,
  name TEXT,
  description TEXT,
  year INTEGER,
  PRIMARY KEY(id AUTOINCREMENT))

  """
  cursor = con.cursor()
  cursor.execute(sql)
  con.commit()
  return "database and table created"

@web_site.route('/moviesadd',methods = ['GET', 'POST'])
def moviesadd():
  msg = ""
  if request.method == 'POST':
    name = request.form["name"]
    desc = request.form["descr"]
    year = request.form["year"]
    con = sqlite3.connect('movies.db')
    sql = "INSERT INTO Movies(name,description,year) VALUES(?,?,?)"
    cursor = con.cursor()
    cursor.execute(sql,(name,desc,year))
    con.commit()
    msg = name + " added to the Movies table"
  return render_template("addmovie.html",msg = msg)

@web_site.route('/movieslist')
def listall():
  con = sqlite3.connect('movies.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  sql = 'SELECT * FROM movies'
  cursor.execute(sql)
  con.commit()
  rows = cursor.fetchall() 
  return render_template("movielist.html",rows = rows)
  
#this is the last line!
web_site.run(host='0.0.0.0', port=8080)