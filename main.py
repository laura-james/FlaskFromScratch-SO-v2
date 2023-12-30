from flask import Flask, render_template, request,redirect
from random import choice
#from werkzeug.utils import secure_filename
import sqlite3
from flask_cors import CORS
from datetime import datetime
web_site = Flask(__name__)
CORS(web_site)

@web_site.route('/')
def index():
  print("Home page - index")
  return render_template("search_item.html")
  
@web_site.route('/runonce')
def createDBandTable():
  con = sqlite3.connect('lostproperty.db')
  sql = """
  CREATE TABLE Items (id INTEGER,
  name TEXT,
  colour TEXT,
  room TEXT,
  date TEXT,
  status TEXT,
  PRIMARY KEY(id AUTOINCREMENT))
  """
  cursor = con.cursor()
  cursor.execute(sql)
  con.commit()
  return "database and table created"

@web_site.route('/report_item',methods = ['GET', 'POST'])
def itemsadd():
  msg = ""
  if request.method == 'POST':
    name = request.form["name"]
    room = request.form["room"]
    colour = request.form["colour"]
    date = request.form["date"]
    status = request.form["status"]
    con = sqlite3.connect('lostproperty.db')
    sql = "INSERT INTO Items(name,colour,room,date,status) VALUES(?,?,?,?,?)"
    cursor = con.cursor()
    cursor.execute(sql,(name,colour,room,date,status))
    con.commit()
    msg = name + " added to the Items table"
    
  allstatuses = ["LOST","FOUND","ARCHIVED"]
  today = datetime.today().strftime('%Y-%m-%d')
  return render_template("report_item.html",msg = msg,allstatuses=allstatuses,date=today)


@web_site.route('/search_item',methods = ['GET', 'POST'])
def search():
  print("search_item")  
  msg = ""
  con = sqlite3.connect('lostproperty.db') #LAJ moved out of IF
  cursor = con.cursor() #LAJ moved out of IF
  if request.method == 'POST':
    print("posting")
    name = request.form["name"]
    print(name)
    room = request.form["room"]
    print(room)
    colour = request.form["colour"]
    print(colour)
    #mydate = request.form["date"]
    #print(mydate)
    #status = request.form["status"]  #LAJ you dont seem to have a status field anymore?
    #print(status)
    print(name,room,colour)
   #sql = "SELECT * FROM Items(name,colour,room,date) VALUES(?,?,?,?)"  LAJ Your SQL IS WRONG
    sql = "SELECT * FROM Items WHERE name LIKE '%?%' OR colour LIKE '%?%' OR room LIKE '%?%'"
    print("SQL",sql)
    cursor.execute(sql,(name,colour,room,date))
    con.commit()
    msg = name + "returned from the Items table"
    rows = cursor.fetchall() #LAJ indented inside IF
    return render_template("list_of_items.html",rows = rows)
  sql = "SELECT * FROM Items"
  print("sql)
  cursor.execute(sql)
  con.commit()
  rows = cursor.fetchall() #LAJ indented inside IF
  return render_template("search_item.html",rows = rows)

@web_site.route('/items_list')
def listall():
  con = sqlite3.connect('lostproperty.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  sql = 'SELECT * FROM items ORDER BY date DESC'
  cursor.execute(sql)
  con.commit()
  rows = cursor.fetchall()
  return render_template("list_of_items.html",rows = rows)

@web_site.route('/delete_item')
def delete_item():
  id = request.args.get('id')
  print("delete item")
  msg = ""
  con = sqlite3.connect('lostproperty.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  sql = "DELETE FROM Items WHERE id = ?"
  #sql ="SELECT * FROM Items WHERE id = ?"
  cursor.execute(sql,(id))
  con.commit()
  return redirect("/search_item")


@web_site.route('/edit_item',methods = ['GET', 'POST'])
def edit_item():
  id = request.args.get('id')
  msg  = "" #initialise this for later
  if request.method == 'POST':
    name = request.form["name"]
    colour = request.form["colour"]
    room = request.form["room"]
    date = request.form["date"]
    status = request.form["status"]
    con = sqlite3.connect('lostproperty.db')
    sql = "UPDATE Items SET name=?,colour=?,room=?,date=?,status =? WHERE id = ?" #using parameters
    cursor = con.cursor()
    cursor.execute(sql,(name,colour,room,date,status,id))
    con.commit()
    msg = name + " was successfully edited"
    
  con = sqlite3.connect('lostproperty.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  #sql = 'DELETE FROM Items WHERE id = '+id
  sql ="SELECT * FROM Items WHERE id="+id
  cursor.execute(sql)
  con.commit()
  rows = cursor.fetchall()
  print(rows)
  allstatuses = ["LOST","FOUND","ARCHIVED"]
  for row in rows:
    return render_template("report_item.html",name=row["name"],colour=row["colour"],room=row["room"],status=row["status"],msg=msg,allstatuses=allstatuses)
#this is the last line!






@web_site.route('/ajaxsearchmovies/<search>')
def ajaxsearchmovies(search):
  con = sqlite3.connect('movies.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  sql = 'SELECT * FROM movies where name like "%'+search+'%"';
  cursor.execute(sql)
  con.commit()
  rows = cursor.fetchall() 
  output = []
  for row in rows:
    link = "<a href='../editmovie?id="+str(row["id"])+"'>"+row["name"]+"</a>"
    output.append(link)
  #import json
  return "<br>".join(output)
web_site.run(host='0.0.0.0', port=8080)



#https://apps.caspio.com/demo9/lf/public/index.html#